# Copyright 2018 AT&T Corporation.
# All rights reserved.
#
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

import copy

from neutron_lib.api.definitions import segment
from neutron_lib.api.definitions import subnet
from neutron_lib.api.definitions import subnet_segmentid_writable


# The alias of the extension.
ALIAS = 'subnet-segmentid-enforce'

# Whether or not this extension is simply signaling behavior to the user
# or it actively modifies the attribute map.
IS_SHIM_EXTENSION = False

# Whether the extension is marking the adoption of standardattr model for
# legacy resources, or introducing new standardattr attributes. False or
# None if the standardattr model is adopted since the introduction of
# resource extension.
# If this is True, the alias for the extension should be prefixed with
# 'standard-attr-'.
IS_STANDARD_ATTR_EXTENSION = False

# The name of the extension.
NAME = 'Subnet SegmentID (policy enforced)'

# A prefix for API resources. An empty prefix means that the API is going
# to be exposed at the v2/ level as any other core resource.
API_PREFIX = ''

# The description of the extension.
DESCRIPTION = "Enforce segment_id policy rule."

# A timestamp of when the extension was introduced.
UPDATED_TIMESTAMP = "2018-09-04T00:00:00-00:00"

segment_id_attr_info = copy.deepcopy(
    subnet_segmentid_writable.RESOURCE_ATTRIBUTE_MAP[
        subnet.COLLECTION_NAME][segment.SEGMENT_ID])
segment_id_attr_info['enforce_policy'] = True

RESOURCE_ATTRIBUTE_MAP = {
    subnet.COLLECTION_NAME: {
        segment.SEGMENT_ID: segment_id_attr_info
    }
}

# The subresource attribute map for the extension. It adds child resources
# to main extension's resource. The subresource map must have a parent and
# a parameters entry. If an extension does not need such a map, None can
# be specified (mandatory).
SUB_RESOURCE_ATTRIBUTE_MAP = {}

# The action map: it associates verbs with methods to be performed on
# the API resource.
ACTION_MAP = {}

# The action status.
ACTION_STATUS = {}

# The list of required extensions.
REQUIRED_EXTENSIONS = [subnet_segmentid_writable.ALIAS]

# The list of optional extensions.
OPTIONAL_EXTENSIONS = []
