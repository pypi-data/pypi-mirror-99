#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import contextlib
import copy
import functools
import weakref

from oslo_concurrency import lockutils
from oslo_config import cfg
from oslo_db import api as oslo_db_api
from oslo_db import exception as db_exc
from oslo_db.sqlalchemy import enginefacade
from oslo_log import log as logging
from oslo_utils import excutils
from osprofiler import opts as profiler_opts
import osprofiler.sqlalchemy
from pecan import util as p_util
import sqlalchemy
from sqlalchemy import event  # noqa
from sqlalchemy import exc as sql_exc
from sqlalchemy import orm
from sqlalchemy.orm import exc

from neutron_lib._i18n import _
from neutron_lib.db import model_base
from neutron_lib import exceptions
from neutron_lib.objects import exceptions as obj_exc


MAX_RETRIES = 20
LOG = logging.getLogger(__name__)
_synchronized = lockutils.synchronized_with_prefix("neutron-")
_CTX_MANAGER = None


@_synchronized("context-manager")
def _create_context_manager():
    global _CTX_MANAGER
    if _CTX_MANAGER is None:
        _CTX_MANAGER = enginefacade.transaction_context()
        _CTX_MANAGER.configure(sqlite_fk=True, flush_on_subtransaction=True)

    return _CTX_MANAGER


def get_context_manager():
    """Transaction Context Manager accessor.

    :returns: The transaction context manager.
    """
    if _CTX_MANAGER is None:
        return _create_context_manager()

    return _CTX_MANAGER


def _set_hook(engine):
    if (profiler_opts.is_trace_enabled() and
            profiler_opts.is_db_trace_enabled()):
        osprofiler.sqlalchemy.add_tracing(
            sqlalchemy, engine, "neutron.db")


# TODO(ihrachys) the hook assumes options defined by osprofiler, and the only
# public function that is provided by osprofiler that will register them is
# set_defaults, that's why we call it here even though we don't need to change
# defaults
profiler_opts.set_defaults(cfg.CONF)
get_context_manager().append_on_engine_create(_set_hook)


def get_reader_session():
    """Helper to get reader session.

    :returns: The reader session.
    """
    return get_context_manager().reader.get_sessionmaker()()


def get_writer_session():
    """Helper to get writer session.

    :returns: The writer session.
    """
    return get_context_manager().writer.get_sessionmaker()()


def _is_nested_instance(e, etypes):
    """Check if exception or its inner excepts are an instance of etypes."""
    if isinstance(e, etypes):
        return True
    if isinstance(e, exceptions.MultipleExceptions):
        return any(_is_nested_instance(i, etypes) for i in e.inner_exceptions)
    if isinstance(e, db_exc.DBError):
        return _is_nested_instance(e.inner_exception, etypes)
    return False


def is_retriable(e):
    """Determine if the exception is retriable.

    :param e: The exception to check.
    :returns: True if e is retriable and False otherwise.
    """
    if getattr(e, '_RETRY_EXCEEDED', False):
        return False
    if _is_nested_instance(e, (db_exc.DBDeadlock, exc.StaleDataError,
                               db_exc.DBConnectionError,
                               db_exc.DBDuplicateEntry, db_exc.RetryRequest,
                               obj_exc.NeutronDbObjectDuplicateEntry)):
        return True
    # looking savepoints mangled by deadlocks. see bug/1590298 for details.
    return _is_nested_instance(e, db_exc.DBError) and '1305' in str(e)


def _tag_retriables_as_unretriable(f):
    """Puts a flag on retriable exceptions so is_retriable returns False.

    This decorator can be used outside of a retry decorator to prevent
    decorators higher up from retrying again.
    """
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            with excutils.save_and_reraise_exception():
                if is_retriable(e):
                    setattr(e, '_RETRY_EXCEEDED', True)
    return wrapped


def _copy_if_lds(item):
    """Deepcopy lists/dicts/sets, leave everything else alone."""
    return copy.deepcopy(item) if isinstance(item, (list, dict, set)) else item


_retry_db_errors = oslo_db_api.wrap_db_retry(
    max_retries=MAX_RETRIES,
    retry_interval=0.5,
    inc_retry_interval=True,
    exception_checker=is_retriable,
    jitter=True
)


def retry_db_errors(f):
    """Nesting-safe retry decorator with auto-arg-copy and logging.

    Retry decorator for all functions which do not accept a context as an
    argument. If the function accepts a context, use
    'retry_if_session_inactive' below.

    If retriable errors are retried and exceed the count, they will be tagged
    with a flag so is_retriable will no longer recognize them as retriable.
    This prevents multiple applications of this decorator (and/or the one
    below) from retrying the same exception.
    """

    @_tag_retriables_as_unretriable
    @_retry_db_errors
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        try:
            # copy mutable args and kwargs to make retries safe. this doesn't
            # prevent mutations of complex objects like the context or 'self'
            dup_args = [_copy_if_lds(a) for a in args]
            dup_kwargs = {k: _copy_if_lds(v) for k, v in kwargs.items()}
            return f(*dup_args, **dup_kwargs)
        except Exception as e:
            with excutils.save_and_reraise_exception():
                if is_retriable(e):
                    LOG.debug("Retry wrapper got retriable exception: %s", e)
    return wrapped


def retry_if_session_inactive(context_var_name='context'):
    """Retries only if the session in the context is inactive.

    Calls a retry_db_errors wrapped version of the function if the context's
    session passed in is inactive, otherwise it just calls the function
    directly. This is useful to avoid retrying things inside of a transaction
    which is ineffective for DB races/errors.

    This should be used in all cases where retries are desired and the method
    accepts a context.
    """
    def decorator(f):
        try:
            # NOTE(kevinbenton): we use pecan's util function here because it
            # deals with the horrors of finding args of already decorated
            # functions
            ctx_arg_index = p_util.getargspec(f).args.index(context_var_name)
        except ValueError as e:
            msg = _("Could not find position of var %s") % context_var_name
            raise RuntimeError(msg) from e
        f_with_retry = retry_db_errors(f)

        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            # only use retry wrapper if we aren't nested in an active
            # transaction
            context = kwargs.get(context_var_name)
            if context is None:
                context = args[ctx_arg_index]
            method = f if context.session.is_active else f_with_retry
            return method(*args, **kwargs)
        return wrapped
    return decorator


@contextlib.contextmanager
def exc_to_retry(etypes):
    """Contextually reraise Exceptions as a RetryRequests.

    :param etypes: The class type to check the exception for.
    :returns: None
    :raises: A RetryRequest if any exception is caught in the context
        is a nested instance of etypes.
    """
    try:
        yield
    except Exception as e:
        with excutils.save_and_reraise_exception() as ctx:
            if _is_nested_instance(e, etypes):
                ctx.reraise = False
                raise db_exc.RetryRequest(e)


# for convenient access as decorators
CONTEXT_READER = get_context_manager().reader
CONTEXT_WRITER = get_context_manager().writer

_REGISTERED_SQLA_EVENTS = []


def sqla_listen(*args):
    """Wrapper to track subscribers for test teardowns.

    SQLAlchemy has no "unsubscribe all" option for its event listener
    framework so we need to keep track of the subscribers by having
    them call through here for test teardowns.

    :param args: The arguments to pass onto the listen call.
    :returns: None
    """
    event.listen(*args)
    _REGISTERED_SQLA_EVENTS.append(args)


def sqla_remove(*args):
    """Remove SQLA listeners.

    :param args: The args to pass onto remove.
    :returns: None.
    """
    event.remove(*args)
    _REGISTERED_SQLA_EVENTS.remove(args)


def sqla_remove_all():
    """Removes all SQLA listeners.

    :returns: None.
    """
    for args in _REGISTERED_SQLA_EVENTS:
        try:
            event.remove(*args)
        except sql_exc.InvalidRequestError:
            # already removed
            pass
    del _REGISTERED_SQLA_EVENTS[:]


@event.listens_for(orm.session.Session, "after_flush")
def _add_to_rel_load_list(session, flush_context=None):
    # keep track of new items to load relationships on during commit
    session.info.setdefault('_load_rels', weakref.WeakSet()).update(
        session.new)


@event.listens_for(orm.session.Session, "before_commit")
def _load_one_to_manys(session):
    # TODO(kevinbenton): we should be able to remove this after we
    # have eliminated all places where related objects are constructed
    # using a key rather than a relationship.

    # capture any new objects
    if session.new:
        session.flush()

    if session.transaction.nested:
        # wait until final commit
        return

    for new_object in session.info.pop('_load_rels', []):
        if new_object not in session:
            # don't load detached objects because that brings them back into
            # session
            continue
        state = sqlalchemy.inspect(new_object)

        # set up relationship loading so that we can call lazy
        # loaders on the object even though the ".key" is not set up yet
        # (normally happens by in after_flush_postexec, but we're trying
        # to do this more succinctly).  in this context this is only
        # setting a simple flag on the object's state.
        session.enable_relationship_loading(new_object)

        # look for eager relationships and do normal load.
        # For relationships where the related object is also
        # in the session these lazy loads will pull from the
        # identity map and not emit SELECT.  Otherwise, we are still
        # local in the transaction so a normal SELECT load will work fine.
        for relationship_attr in state.mapper.relationships:
            if relationship_attr.lazy not in ('joined', 'subquery'):
                # we only want to automatically load relationships that would
                # automatically load during a lookup operation
                continue
            if relationship_attr.key not in state.dict:
                getattr(new_object, relationship_attr.key)
                if relationship_attr.key not in state.dict:
                    msg = ("Relationship %s attributes must be loaded in db "
                           "object %s" % (relationship_attr.key, state.dict))
                    raise AssertionError(msg)


# Expire relationships when foreign key changes.
#
# NOTE(ihrachys) Arguably, it's a sqlalchemy anti-pattern to access child
# models directly and through parent relationships in the same session. But
# since OVO mechanism is built around synthetic fields that assume this mixed
# access is possible, we keep it here until we find a way to migrate OVO
# synthetic fields to better mechanism that would update child models via
# parents. Even with that, there are multiple places in plugin code where we
# mix access when using models directly; those occurrences would need to be
# fixed too to be able to remove this hook and explicit expire() calls.
#
# Adopted from the following recipe:
# https://bitbucket.org/zzzeek/sqlalchemy/wiki/UsageRecipes
# /ExpireRelationshipOnFKChange
#
# ...then massively changed to actually work for all neutron backref cases.
#
# TODO(ihrachys) at some point these event handlers should be extended to also
# automatically refresh values for expired attributes
def _expire_for_fk_change(target, fk_value, relationship_prop, column_attr):
    """Expire relationship attributes when a many-to-one column changes."""

    sess = orm.object_session(target)

    # subnets and network's many-to-one relationship is used as example in the
    # comments in this function
    if sess is not None:
        # optional behavior #1 - expire the "Network.subnets"
        # collection on the existing "network" object
        if relationship_prop.back_populates and \
                relationship_prop.key in target.__dict__:
            obj = getattr(target, relationship_prop.key)
            if obj is not None and sqlalchemy.inspect(obj).persistent:
                sess.expire(obj, [relationship_prop.back_populates])

        # optional behavior #2 - expire the "Subnet.network"
        if sqlalchemy.inspect(target).persistent:
            sess.expire(target, [relationship_prop.key])

        # optional behavior #3 - "trick" the ORM by actually
        # setting the value ahead of time, then emitting a load
        # for the attribute so that the *new* Subnet.network
        # is loaded.  Then, expire Network.subnets on *that*.
        # Other techniques here including looking in the identity
        # map for "value", if this is a simple many-to-one get.
        if relationship_prop.back_populates:
            target.__dict__[column_attr] = fk_value
            new = getattr(target, relationship_prop.key)
            if new is not None:
                if sqlalchemy.inspect(new).persistent:
                    sess.expire(new, [relationship_prop.back_populates])
    else:
        # no Session yet, do it later. This path is reached from the 'expire'
        # listener setup by '_expire_prop_on_col' below, when a foreign key
        # is directly assigned to in the many to one side of a relationship.
        # i.e. assigning directly to Subnet.network_id before Subnet is added
        # to the session
        if target not in _emit_on_pending:
            _emit_on_pending[target] = []
        _emit_on_pending[target].append(
            (fk_value, relationship_prop, column_attr))


_emit_on_pending = weakref.WeakKeyDictionary()


@event.listens_for(orm.session.Session, "pending_to_persistent")
def _pending_callables(session, obj):
    """Expire relationships when a new object w/ a FK becomes persistent"""
    if obj is None:
        return
    args = _emit_on_pending.pop(obj, [])
    for a in args:
        if a is not None:
            _expire_for_fk_change(obj, *a)


@event.listens_for(orm.session.Session, "persistent_to_deleted")
def _persistent_to_deleted(session, obj):
    """Expire relationships when an object w/ a foreign key becomes deleted"""
    mapper = sqlalchemy.inspect(obj).mapper
    for prop in mapper.relationships:
        if prop.direction is orm.interfaces.MANYTOONE:
            for col in prop.local_columns:
                colkey = mapper.get_property_by_column(col).key
                _expire_for_fk_change(obj, None, prop, colkey)


@event.listens_for(model_base.BASEV2, "attribute_instrument", propagate=True)
def _listen_for_changes(cls, key, inst):
    mapper = sqlalchemy.inspect(cls)
    if key not in mapper.relationships:
        return
    prop = inst.property

    if prop.direction is orm.interfaces.MANYTOONE:
        for col in prop.local_columns:
            colkey = mapper.get_property_by_column(col).key
            _expire_prop_on_col(cls, prop, colkey)
    elif prop.direction is orm.interfaces.ONETOMANY:
        remote_mapper = prop.mapper
        # the collection *has* to have a MANYTOONE backref so we
        # can look up the parent.  so here we make one if it doesn't
        # have it already, as is the case in this example
        if not prop.back_populates:
            name = "_%s_backref" % prop.key
            backref_prop = orm.relationship(
                prop.parent, back_populates=prop.key)

            remote_mapper.add_property(name, backref_prop)
            prop.back_populates = name


def _expire_prop_on_col(cls, prop, colkey):
    @event.listens_for(getattr(cls, colkey), "set")
    def expire(target, value, oldvalue, initiator):
        """Expire relationships when FK attribute on an object changes"""
        _expire_for_fk_change(target, value, prop, colkey)
