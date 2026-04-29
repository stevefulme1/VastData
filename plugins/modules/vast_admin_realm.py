# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data administrator realms."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_admin_realm
short_description: Manage VAST Data administrator realms
description:
    - Create, update, and delete administrator realms on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the administrator realm.
        type: str
        required: true
    realm_type:
        description:
            - Type of the realm.
        type: str
        required: false
        choices: [ldap, ad, nis]
    directory_url:
        description:
            - URL of the directory server.
        type: str
        required: false
    base_dn:
        description:
            - Base distinguished name for directory queries.
        type: str
        required: false
    state:
        description:
            - The desired state of the administrator realm.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - vastdata.cluster.vast_common
"""

EXAMPLES = r"""
- name: Create an administrator realm
  vastdata.cluster.vast_admin_realm:
    vms_host: "vms.example.com"
    vms_user: "admin"
    vms_password: "{{ vault_vms_password }}"
    name: "corporate-ldap"
    realm_type: "ldap"
    directory_url: "ldap://ldap.example.com:389"
    base_dn: "dc=example,dc=com"
    state: present

- name: Update an administrator realm
  vastdata.cluster.vast_admin_realm:
    vms_host: "vms.example.com"
    api_token: "my-token"
    name: "corporate-ldap"
    directory_url: "ldaps://ldap.example.com:636"
    state: present

- name: Delete an administrator realm
  vastdata.cluster.vast_admin_realm:
    vms_host: "vms.example.com"
    api_token: "my-token"
    name: "corporate-ldap"
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the administrator realm.
    returned: on success
    type: dict
    sample:
        id: 1
        name: "corporate-ldap"
        realm_type: "ldap"
        directory_url: "ldap://ldap.example.com:389"
        base_dn: "dc=example,dc=com"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource import VastResourceBase


class VastAdminRealm(VastResourceBase):
    resource_path = "/api/realms/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "realm_type",
            "directory_url",
            "base_dn"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["directory_url", "base_dn"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        realm_type=dict(type="str", required=False, choices=["ldap", "ad", "nis"]),
        directory_url=dict(type="str", required=False),
        base_dn=dict(type="str", required=False),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastAdminRealm(module).run()


if __name__ == "__main__":
    main()
