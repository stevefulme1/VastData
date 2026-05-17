# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data non-local users."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_nonlocal_user
short_description: Manage VAST Data non-local users
description:
    - Create, update, and delete non-local (directory-sourced) users on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the non-local user.
        type: str
        required: true
    uid:
        description:
            - User ID for the non-local user.
        type: int
        required: false
    provider_name:
        description:
            - Name of the directory provider for the user.
        type: str
        required: false
    state:
        description:
            - The desired state of the non-local user.
        type: str
        default: present
        choices: [present, absent]
    limit:
        description:
            - Maximum number of results to return.
        type: int
        default: 100
    offset:
        description:
            - Number of results to skip for pagination.
        type: int
        default: 0
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Create a non-local user
  stevefulme1.vastdata.vast_nonlocal_user:
    vms_host: "vms.example.com"
    vms_user: "admin"
    vms_password: "{{ vault_vms_password }}"
    validate_certs: true
    name: "jdoe@example.com"
    uid: 7001
    provider_name: "ActiveDirectory"
    state: present

- name: Update a non-local user
  stevefulme1.vastdata.vast_nonlocal_user:
    vms_host: "vms.example.com"
    api_token: "my-token"
    name: "jdoe@example.com"
    provider_name: "LDAP"
    state: present

- name: Delete a non-local user
  stevefulme1.vastdata.vast_nonlocal_user:
    vms_host: "vms.example.com"
    api_token: "my-token"
    name: "jdoe@example.com"
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the non-local user.
    returned: on success
    type: dict
    sample:
        id: 1
        name: "jdoe@example.com"
        uid: 7001
        provider_name: "ActiveDirectory"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastNonlocalUser(VastResourceBase):
    resource_path = "/api/nonlocalusers/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "uid",
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
        uid=dict(type="int", required=False),
        provider_name=dict(type="str", required=False),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastNonlocalUser(module).run()


if __name__ == "__main__":
    main()
