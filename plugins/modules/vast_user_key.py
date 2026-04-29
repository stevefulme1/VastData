# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data user access keys."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_user_key
short_description: Manage VAST Data user access keys
description:
    - Create, update, and delete user access keys on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    user_id:
        description:
            - ID of the user for this access key.
        type: int
        required: true
    access_key:
        description:
            - The access key identifier.
        type: str
        required: false
    enabled:
        description:
            - Whether the access key is enabled.
        type: bool
        required: false
    state:
        description:
            - The desired state of the user access key.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - vastdata.cluster.vast_common
"""

EXAMPLES = r"""
- name: Create a user access key
  vastdata.cluster.vast_user_key:
    vms_host: "vms.example.com"
    vms_user: "admin"
    vms_password: "secret"
    user_id: 5001
    access_key: "AKIAIOSFODNN7EXAMPLE"
    enabled: true
    state: present

- name: Update a user access key
  vastdata.cluster.vast_user_key:
    vms_host: "vms.example.com"
    api_token: "my-token"
    user_id: 5001
    access_key: "AKIAIOSFODNN7EXAMPLE"
    enabled: false
    state: present

- name: Delete a user access key
  vastdata.cluster.vast_user_key:
    vms_host: "vms.example.com"
    api_token: "my-token"
    user_id: 5001
    access_key: "AKIAIOSFODNN7EXAMPLE"
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the user access key.
    returned: on success
    type: dict
    sample:
        id: 1
        user_id: 5001
        access_key: "AKIAIOSFODNN7EXAMPLE"
        enabled: true
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource import VastResourceBase


class VastUserKey(VastResourceBase):
    resource_path = "/api/userkeys/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "user_id",
            "access_key",
            "enabled"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["enabled"]


def main():
    module_args = dict(
        user_id=dict(type="int", required=True),
        access_key=dict(type="str", required=False),
        enabled=dict(type="bool", required=False),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastUserKey(module).run()


if __name__ == "__main__":
    main()
