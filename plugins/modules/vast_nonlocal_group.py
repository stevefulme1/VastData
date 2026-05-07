# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data non-local groups."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_nonlocal_group
short_description: Manage VAST Data non-local groups
description:
    - Create, update, and delete non-local (directory-sourced) groups on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the non-local group.
        type: str
        required: true
    gid:
        description:
            - Group ID for the non-local group.
        type: int
        required: false
    provider_name:
        description:
            - Name of the directory provider for the group.
        type: str
        required: false
    state:
        description:
            - The desired state of the non-local group.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Create a non-local group
  stevefulme1.vastdata.vast_nonlocal_group:
    vms_host: "vms.example.com"
    vms_user: "admin"
    vms_password: "{{ vault_vms_password }}"
    name: "domain_admins"
    gid: 8001
    provider_name: "ActiveDirectory"
    state: present

- name: Update a non-local group
  stevefulme1.vastdata.vast_nonlocal_group:
    vms_host: "vms.example.com"
    api_token: "my-token"
    name: "domain_admins"
    provider_name: "LDAP"
    state: present

- name: Delete a non-local group
  stevefulme1.vastdata.vast_nonlocal_group:
    vms_host: "vms.example.com"
    api_token: "my-token"
    name: "domain_admins"
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the non-local group.
    returned: on success
    type: dict
    sample:
        id: 1
        name: "domain_admins"
        gid: 8001
        provider_name: "ActiveDirectory"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastNonlocalGroup(VastResourceBase):
    resource_path = "/api/nonlocalgroups/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "gid",
            "provider_name"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["provider_name"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        gid=dict(type="int", required=False),
        provider_name=dict(type="str", required=False),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastNonlocalGroup(module).run()


if __name__ == "__main__":
    main()
