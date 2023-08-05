# Copyright (c) 2020 Red Hat, Inc.
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

from neutron_lib.api.definitions import port
from neutron_lib import constants


ALIAS = 'port-numa-affinity-policy'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Port NUMA affinity policy'
DESCRIPTION = "Expose the port NUMA affinity policy"
UPDATED_TIMESTAMP = "2020-07-08T10:00:00-00:00"
RESOURCE_NAME = port.RESOURCE_NAME
COLLECTION_NAME = port.COLLECTION_NAME
NUMA_AFFINITY_POLICY = 'numa_affinity_policy'

RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        NUMA_AFFINITY_POLICY: {
            'allow_post': True,
            'allow_put': True,
            'validate': {
                'type:values': constants.PORT_NUMA_POLICIES + (None, )},
            'default': None,
            'is_visible': True}
    },
}

SUB_RESOURCE_ATTRIBUTE_MAP = None
ACTION_MAP = {}
ACTION_STATUS = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
