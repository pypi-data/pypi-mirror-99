# Copyright (c) 2018 Ericsson
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from neutron_lib.api.definitions import agent
from neutron_lib import constants


ALIAS = 'agent-resources-synced'
IS_SHIM_EXTENSION = False
IS_STANDARD_ATTR_EXTENSION = False
NAME = "Agent's Resource View Synced to Placement"
DESCRIPTION = 'Stores success/failure of last sync to Placement'
UPDATED_TIMESTAMP = '2018-12-19T00:00:00-00:00'
RESOURCE_NAME = agent.RESOURCE_NAME
COLLECTION_NAME = agent.COLLECTION_NAME
RESOURCES_SYNCED = 'resources_synced'

RESOURCE_ATTRIBUTE_MAP = {
    COLLECTION_NAME: {
        RESOURCES_SYNCED: {
            'allow_post': False,
            'allow_put': False,
            'default': constants.ATTR_NOT_SPECIFIED,
            'is_visible': True,
        }
    }
}

SUB_RESOURCE_ATTRIBUTE_MAP = None
ACTION_MAP = {}
ACTION_STATUS = {}
REQUIRED_EXTENSIONS = [agent.ALIAS]
OPTIONAL_EXTENSIONS = []
