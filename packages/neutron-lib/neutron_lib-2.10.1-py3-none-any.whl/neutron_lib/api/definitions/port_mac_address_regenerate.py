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

from neutron_lib.api import converters
from neutron_lib.api.definitions import port as port_def
from neutron_lib import constants


NAME = 'Neutron Port MAC address regenerate'
ALIAS = 'port-mac-address-regenerate'
DESCRIPTION = "Network port MAC address regenerate"

UPDATED_TIMESTAMP = "2018-05-03T10:00:00-00:00"

RESOURCE_ATTRIBUTE_MAP = {
    port_def.COLLECTION_NAME: {
        port_def.PORT_MAC_ADDRESS: {
            'allow_post': True, 'allow_put': True,
            'default': constants.ATTR_NOT_SPECIFIED,
            'convert_to': converters.convert_to_mac_if_none,
            'validate': {'type:mac_address': None},
            'enforce_policy': True,
            'is_filter': True,
            'is_sort_key': True,
            'is_visible': True},
    }
}

IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
SUB_RESOURCE_ATTRIBUTE_MAP = {}
ACTION_MAP = {}
REQUIRED_EXTENSIONS = []
OPTIONAL_EXTENSIONS = []
ACTION_STATUS = {}
