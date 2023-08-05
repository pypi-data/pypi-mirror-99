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

from neutron_lib.api.definitions import subnet as subnet_def
from neutron_lib import constants


ALIAS = 'subnet-service-types'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = 'Subnet service types'
API_PREFIX = ''
DESCRIPTION = "Provides ability to set the subnet service_types field"
UPDATED_TIMESTAMP = "2016-03-15T18:00:00-00:00"
RESOURCE_NAME = 'service_type'
COLLECTION_NAME = 'service_types'

RESOURCE_ATTRIBUTE_MAP = {
    subnet_def.COLLECTION_NAME: {
        COLLECTION_NAME: {
            'allow_post': True,
            'allow_put': True,
            'default': constants.ATTR_NOT_SPECIFIED,
            'validate': {'type:list_of_subnet_service_types': None},
            'is_visible': True
        }
    }
}

SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
ACTION_STATUS = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
