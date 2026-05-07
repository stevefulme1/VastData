# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data S3 Policy Attachments."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_s3_policy_attachment
short_description: Manage VAST Data S3 policy attachments
description:
    - Create, update, and delete S3 policy attachments to users/groups on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    policy_id:
        description:
            - ID of the S3 policy to attach.
        type: int
        required: true
    principal_type:
        description:
            - Type of principal (user or group).
        type: str
        required: true
        choices: [user, group]
    principal_id:
        description:
            - ID of the user or group to attach the policy to.
        type: int
        required: true
    state:
        description:
            - The desired state of the S3 policy attachment.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Attach S3 policy to a user
  stevefulme1.vastdata.vast_s3_policy_attachment:
    policy_id: 1
    principal_type: user
    principal_id: 100
    state: present

- name: Attach S3 policy to a group
  stevefulme1.vastdata.vast_s3_policy_attachment:
    policy_id: 1
    principal_type: group
    principal_id: 200
    state: present

- name: Detach S3 policy from a user
  stevefulme1.vastdata.vast_s3_policy_attachment:
    policy_id: 1
    principal_type: user
    principal_id: 100
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the S3 policy attachment.
    returned: on success
    type: dict
    sample:
        id: 1
        policy_id: 1
        principal_type: user
        principal_id: 100
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastS3PolicyAttachment(VastResourceBase):
    resource_path = "/api/s3policyattachments/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "policy_id",
            "principal_type",
            "principal_id"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["policy_id", "principal_type", "principal_id"]


def main():
    module_args = dict(
        policy_id=dict(type="int", required=True),
        principal_type=dict(type="str", required=True, choices=["user", "group"]),
        principal_id=dict(type="int", required=True),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastS3PolicyAttachment(module).run()


if __name__ == "__main__":
    main()
