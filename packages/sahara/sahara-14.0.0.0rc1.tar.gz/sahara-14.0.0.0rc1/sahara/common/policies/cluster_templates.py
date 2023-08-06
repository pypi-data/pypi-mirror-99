# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from oslo_policy import policy

from sahara.common.policies import base


cluster_templates_policies = [
    policy.DocumentedRuleDefault(
        name=base.DATA_PROCESSING_CLUSTER_TEMPLATES % 'create',
        check_str=base.UNPROTECTED,
        description='Create cluster template.',
        operations=[{'path': '/v1.1/{project_id}/cluster-templates',
                     'method': 'POST'}]),
    policy.DocumentedRuleDefault(
        name=base.DATA_PROCESSING_CLUSTER_TEMPLATES % 'delete',
        check_str=base.UNPROTECTED,
        description='Delete a cluster template.',
        operations=[
            {'path': '/v1.1/{project_id}/cluster-templates/{cluster_temp_id}',
             'method': 'DELETE'}]),
    policy.DocumentedRuleDefault(
        name=base.DATA_PROCESSING_CLUSTER_TEMPLATES % 'modify',
        check_str=base.UNPROTECTED,
        description='Update cluster template.',
        operations=[
            {'path': '/v1.1/{project_id}/cluster-templates/{cluster_temp_id}',
             'method': 'PUT'}]),
    policy.DocumentedRuleDefault(
        name=base.DATA_PROCESSING_CLUSTER_TEMPLATES % 'get',
        check_str=base.UNPROTECTED,
        description='Show cluster template details.',
        operations=[
            {'path': '/v1.1/{project_id}/cluster-templates/{cluster_temp_id}',
             'method': 'GET'}]),
    policy.DocumentedRuleDefault(
        name=base.DATA_PROCESSING_CLUSTER_TEMPLATES % 'get_all',
        check_str=base.UNPROTECTED,
        description='List cluster templates.',
        operations=[{'path': '/v1.1/{project_id}/cluster-templates',
                     'method': 'GET'}]),
]


def list_rules():
    return cluster_templates_policies
