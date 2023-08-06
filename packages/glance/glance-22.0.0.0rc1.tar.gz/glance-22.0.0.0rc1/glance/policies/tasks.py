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

from oslo_log import versionutils
from oslo_policy import policy


TASK_DESCRIPTION = """
This granular policy controls access to tasks, both from the tasks API as well
as internal locations in Glance that use tasks (like import). Practically this
cannot be more restrictive than the policy that controls import or things will
break, and changing it from the default is almost certainly not what you want.
Access to the external tasks API should be restricted as desired by the
tasks_api_access policy. This may change in the future.
"""

MODIFY_TASK_DEPRECATION = """
This policy check has never been honored by the API. It will be removed in a
future release.
"""

TASK_ACCESS_DESCRIPTION = """
This is a generic blanket policy for protecting all task APIs. It is not
granular and will not allow you to separate writable and readable task
operations into different roles.
"""

task_policies = [
    policy.DocumentedRuleDefault(
        name="get_task",
        # All policies except tasks_api_access are internal policies that are
        # only called by glance as a result of some other operation.
        check_str='rule:default',
        scope_types=['system', 'project'],
        description='Get an image task.\n' + TASK_DESCRIPTION,
        operations=[
            {'path': '/v2/tasks/{task_id}',
             'method': 'GET'}
        ],
    ),
    policy.DocumentedRuleDefault(
        name="get_tasks",
        check_str='rule:default',
        scope_types=['system', 'project'],
        description='List tasks for all images.\n' + TASK_DESCRIPTION,
        operations=[
            {'path': '/v2/tasks',
             'method': 'GET'}
        ],
    ),
    policy.DocumentedRuleDefault(
        name="add_task",
        check_str='rule:default',
        scope_types=['system', 'project'],
        description='List tasks for all images.\n' + TASK_DESCRIPTION,
        operations=[
            {'path': '/v2/tasks',
             'method': 'POST'}
        ],
    ),
    policy.DocumentedRuleDefault(
        name="modify_task",
        check_str='rule:default',
        scope_types=['system', 'project'],
        description="This policy is not used.",
        operations=[
            {'path': '/v2/tasks/{task_id}',
             'method': 'DELETE'}
        ],
        deprecated_for_removal=True,
        deprecated_reason=MODIFY_TASK_DEPRECATION,
        deprecated_since=versionutils.deprecated.WALLABY,
    ),
    policy.DocumentedRuleDefault(
        name="tasks_api_access",
        check_str="role:admin",
        scope_types=['system', 'project'],
        description=TASK_ACCESS_DESCRIPTION,
        operations=[
            {'path': '/v2/tasks/{task_id}',
             'method': 'GET'},
            {'path': '/v2/tasks',
             'method': 'GET'},
            {'path': '/v2/tasks',
             'method': 'POST'},
            {'path': '/v2/tasks/{task_id}',
             'method': 'DELETE'}
        ],
    )
]


def list_rules():
    return task_policies
