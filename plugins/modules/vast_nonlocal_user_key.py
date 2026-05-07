# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data non-local user access keys."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_nonlocal_user_key
short_description: Manage VAST Data non-local user access keys
description:
    - Create, update, and delete access keys for non-local users on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    user_id:
        description:
            - ID of the non-local user for this access key.
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
            - The desired state of the non-local user access key.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Create a non-local user access key
  stevefulme1.vastdata.vast_nonlocal_user_key:
    vms_host: "vms.example.com"
    vms_user: "admin"
    vms_password: "{{ vault_vms_password }}"
    validate_certs: true
    user_id: 7001
    access_key: "AKIAJEXAMPLEKEY12345"
    enabled: true
    state: present

- name: Update a non-local user access key
  stevefulme1.vastdata.vast_nonlocal_user_key:
    vms_host: "vms.example.com"
    api_token: "my-token"
    user_id: 7001
    access_key: "AKIAJEXAMPLEKEY12345"
    enabled: false
    state: present

- name: Delete a non-local user access key
  stevefulme1.vastdata.vast_nonlocal_user_key:
    vms_host: "vms.example.com"
    api_token: "my-token"
    user_id: 7001
    access_key: "AKIAJEXAMPLEKEY12345"
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the non-local user access key.
    returned: on success
    type: dict
    sample:
        id: 1
        user_id: 7001
        access_key: "AKIAJEXAMPLEKEY12345"
        enabled: true
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastNonlocalUserKey(VastResourceBase):
    resource_path = "/api/nonlocaluserkeys/"

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
        access_key=dict(type="str", required=False, no_log=True),
        enabled=dict(type="bool", required=False),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastNonlocalUserKey(module).run()


if __name__ == "__main__":
    main()
