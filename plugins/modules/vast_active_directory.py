# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data Active Directory integration."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_active_directory
short_description: Manage VAST Data Active Directory integration
description:
    - Create, update, and delete Active Directory integration on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    machine_account_name:
        description:
            - Machine account name for joining the Active Directory domain.
        type: str
        required: true
    domain_name:
        description:
            - Active Directory domain name.
        type: str
        required: true
    organizational_unit:
        description:
            - Organizational unit for the machine account.
        type: str
    preferred_dc_list:
        description:
            - List of preferred domain controllers.
        type: list
        elements: str
    use_ldaps:
        description:
            - Whether to use LDAPS for secure communication.
        type: bool
        default: false
    port:
        description:
            - Port for Active Directory communication.
        type: int
    username:
        description:
            - Username for joining the Active Directory domain.
        type: str
    password:
        description:
            - Password for joining the Active Directory domain.
        type: str
    state:
        description:
            - The desired state of the Active Directory integration.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Create Active Directory integration
  stevefulme1.vastdata.vast_active_directory:
    machine_account_name: vast-cluster01
    domain_name: corp.example.com
    organizational_unit: OU=Storage,DC=corp,DC=example,DC=com
    preferred_dc_list:
      - dc1.corp.example.com
      - dc2.corp.example.com
    use_ldaps: true
    port: 636
    username: admin@corp.example.com
    password: "{{ vault_ad_password }}"
    state: present
    vast_host: vast.example.com
    vast_username: admin
    vms_password: "{{ vault_vms_password }}"

- name: Update Active Directory integration
  stevefulme1.vastdata.vast_active_directory:
    machine_account_name: vast-cluster01
    domain_name: corp.example.com
    preferred_dc_list:
      - dc1.corp.example.com
      - dc2.corp.example.com
      - dc3.corp.example.com
    use_ldaps: true
    state: present
    vast_host: vast.example.com
    vast_username: admin
    vms_password: "{{ vault_vms_password }}"

- name: Delete Active Directory integration
  stevefulme1.vastdata.vast_active_directory:
    machine_account_name: vast-cluster01
    domain_name: corp.example.com
    state: absent
    vast_host: vast.example.com
    vast_username: admin
    vms_password: "{{ vault_vms_password }}"
"""

RETURN = r"""
resource:
    description: Details of the Active Directory integration.
    returned: on success
    type: dict
    sample:
        id: 1
        machine_account_name: vast-cluster01
        domain_name: corp.example.com
        organizational_unit: OU=Storage,DC=corp,DC=example,DC=com
        preferred_dc_list:
          - dc1.corp.example.com
          - dc2.corp.example.com
        use_ldaps: true
        port: 636
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastActiveDirectory(VastResourceBase):
    resource_path = "/api/activedirectory/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "machine_account_name",
            "domain_name",
            "organizational_unit",
            "preferred_dc_list",
            "use_ldaps",
            "port",
            "username",
            "password"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["domain_name", "organizational_unit", "preferred_dc_list", "use_ldaps", "port", "username", "password"]


def main():
    module_args = dict(
        machine_account_name=dict(type="str", required=True),
        domain_name=dict(type="str", required=True),
        organizational_unit=dict(type="str"),
        preferred_dc_list=dict(type="list", elements="str"),
        use_ldaps=dict(type="bool", default=False),
        port=dict(type="int"),
        username=dict(type="str"),
        password=dict(type="str", no_log=True),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastActiveDirectory(module).run()


if __name__ == "__main__":
    main()
