#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from oslo_policy import policy

from networking_sfc.policies import base


rules = [
    policy.DocumentedRuleDefault(
        'create_service_graph',
        base.RULE_ANY,
        'Create a service graph',
        [
            {
                'method': 'POST',
                'path': '/sfc/service_graphs',
            },
        ]
    ),
    policy.DocumentedRuleDefault(
        'update_service_graph',
        base.RULE_ADMIN_OR_OWNER,
        'Update a service graph',
        [
            {
                'method': 'PUT',
                'path': '/sfc/service_graphs/{id}',
            },
        ]
    ),
    policy.DocumentedRuleDefault(
        'delete_service_graph',
        base.RULE_ADMIN_OR_OWNER,
        'Delete a service graph',
        [
            {
                'method': 'DELETE',
                'path': '/sfc/service_graphs/{id}',
            },
        ]
    ),
    policy.DocumentedRuleDefault(
        'get_service_graph',
        base.RULE_ADMIN_OR_OWNER,
        'Get service graphs',
        [
            {
                'method': 'GET',
                'path': '/sfc/service_graphs',
            },
            {
                'method': 'GET',
                'path': '/sfc/service_graphs/{id}',
            },
        ]
    ),
]


def list_rules():
    return rules
