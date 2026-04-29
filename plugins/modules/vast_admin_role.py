# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data administrator roles."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_admin_role
short_description: Manage VAST Data administrator roles
description:
    - Create, update, and delete administrator roles on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the administrator role.
        type: str
        required: true
    permissions:
        description:
            - List of permissions assigned to this role.
        type: list
        elements: str
        required: false
    state:
        description:
            - The desired state of the administrator role.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - vastdata.cluster.vast_common
"""

EXAMPLES = r"""
- name: Create an administrator role
  vastdata.cluster.vast_admin_role:
    vms_host: "vms.example.com"
    vms_user: "admin"
    vms_password: "{{ vault_vms_password }}"
    name: "storage-admin"
    permissions:
      - "view_cluster"
      - "manage_volumes"
      - "manage_quotas"
    state: present

- name: Update an administrator role
  vastdata.cluster.vast_admin_role:
    vms_host: "vms.example.com"
    api_token: "my-token"
    name: "storage-admin"
    permissions:
      - "view_cluster"
      - "manage_volumes"
      - "manage_quotas"
      - "manage_snapshots"
    state: present

- name: Delete an administrator role
  vastdata.cluster.vast_admin_role:
    vms_host: "vms.example.com"
    api_token: "my-token"
    name: "storage-admin"
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the administrator role.
    returned: on success
    type: dict
    sample:
        id: 1
        name: "storage-admin"
        permissions:
          - "view_cluster"
          - "manage_volumes"
          - "manage_quotas"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource import VastResourceBase


class VastAdminRole(VastResourceBase):
    resource_path = "/api/roles/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in ["name", "permissions"] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["permissions"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        permissions=dict(type="list", elements="str", required=False),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastAdminRole(module).run()


if __name__ == "__main__":
    main()
