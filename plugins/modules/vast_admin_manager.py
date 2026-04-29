# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data administrator manager settings."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_admin_manager
short_description: Manage VAST Data administrator manager settings
description:
    - Create, update, and delete administrator manager settings on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the administrator manager.
        type: str
        required: true
    admin_role_id:
        description:
            - ID of the administrator role to assign.
        type: int
        required: false
    realm_id:
        description:
            - ID of the realm to associate with this manager.
        type: int
        required: false
    is_enabled:
        description:
            - Whether the administrator manager is enabled.
        type: bool
        required: false
    state:
        description:
            - The desired state of the administrator manager.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - vastdata.cluster.vast_common
"""

EXAMPLES = r"""
- name: Create an administrator manager
  vastdata.cluster.vast_admin_manager:
    vms_host: "vms.example.com"
    vms_user: "admin"
    vms_password: "secret"
    name: "ldap-manager"
    admin_role_id: 5
    realm_id: 3
    is_enabled: true
    state: present

- name: Update an administrator manager
  vastdata.cluster.vast_admin_manager:
    vms_host: "vms.example.com"
    api_token: "my-token"
    name: "ldap-manager"
    admin_role_id: 6
    is_enabled: false
    state: present

- name: Delete an administrator manager
  vastdata.cluster.vast_admin_manager:
    vms_host: "vms.example.com"
    api_token: "my-token"
    name: "ldap-manager"
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the administrator manager.
    returned: on success
    type: dict
    sample:
        id: 1
        name: "ldap-manager"
        admin_role_id: 5
        realm_id: 3
        is_enabled: true
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource import VastResourceBase


class VastAdminManager(VastResourceBase):
    resource_path = "/api/managers/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in ["name", "admin_role_id", "realm_id", "is_enabled"] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["admin_role_id", "realm_id", "is_enabled"]

def main():
    module_args = dict(
        name=dict(type="str", required=True),
        admin_role_id=dict(type="int", required=False),
        realm_id=dict(type="int", required=False),
        is_enabled=dict(type="bool", required=False),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastAdminManager(module).run()

if __name__ == "__main__":
    main()
