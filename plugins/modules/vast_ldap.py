# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data LDAP authentication providers."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_ldap
short_description: Manage VAST Data LDAP authentication providers
description:
    - Create, update, and delete LDAP authentication providers on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the LDAP authentication provider.
        type: str
        required: true
    urls:
        description:
            - List of LDAP server URLs.
        type: list
        elements: str
        required: true
    base_dn:
        description:
            - Base distinguished name for LDAP searches.
        type: str
        required: true
    bind_dn:
        description:
            - Distinguished name for binding to the LDAP server.
        type: str
    bind_password:
        description:
            - Password for binding to the LDAP server.
        type: str
    user_search_base:
        description:
            - Base DN for user searches.
        type: str
    group_search_base:
        description:
            - Base DN for group searches.
        type: str
    use_tls:
        description:
            - Whether to use TLS for LDAP connections.
        type: bool
        default: true
    port:
        description:
            - LDAP server port.
        type: int
        default: 389
    method:
        description:
            - Authentication method.
        type: str
        choices: [simple, sasl]
    state:
        description:
            - The desired state of the LDAP authentication provider.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - vastdata.cluster.vast_common
"""

EXAMPLES = r"""
- name: Create LDAP authentication provider
  vastdata.cluster.vast_ldap:
    name: corporate_ldap
    urls:
      - ldap://ldap1.example.com
      - ldap://ldap2.example.com
    base_dn: dc=example,dc=com
    bind_dn: cn=admin,dc=example,dc=com
    bind_password: "{{ vault_ldap_bind_password }}"
    user_search_base: ou=users,dc=example,dc=com
    group_search_base: ou=groups,dc=example,dc=com
    use_tls: true
    port: 389
    method: simple
    state: present
    vast_host: vast.example.com
    vast_username: admin
    vms_password: "{{ vault_vms_password }}"

- name: Update LDAP authentication provider
  vastdata.cluster.vast_ldap:
    name: corporate_ldap
    urls:
      - ldap://ldap1.example.com
      - ldap://ldap2.example.com
      - ldap://ldap3.example.com
    base_dn: dc=example,dc=com
    use_tls: true
    port: 636
    state: present
    vast_host: vast.example.com
    vast_username: admin
    vms_password: "{{ vault_vms_password }}"

- name: Delete LDAP authentication provider
  vastdata.cluster.vast_ldap:
    name: corporate_ldap
    state: absent
    vast_host: vast.example.com
    vast_username: admin
    vms_password: "{{ vault_vms_password }}"
"""

RETURN = r"""
resource:
    description: Details of the LDAP authentication provider.
    returned: on success
    type: dict
    sample:
        id: 1
        name: corporate_ldap
        urls:
          - ldap://ldap1.example.com
          - ldap://ldap2.example.com
        base_dn: dc=example,dc=com
        bind_dn: cn=admin,dc=example,dc=com
        user_search_base: ou=users,dc=example,dc=com
        group_search_base: ou=groups,dc=example,dc=com
        use_tls: true
        port: 389
        method: simple
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource import VastResourceBase


class VastLdap(VastResourceBase):
    resource_path = "/api/ldaps/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "urls",
            "base_dn",
            "bind_dn",
            "bind_password",
            "user_search_base",
            "group_search_base",
            "use_tls",
            "port",
            "method"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return [
            "urls",
            "base_dn",
            "bind_dn",
            "bind_password",
            "user_search_base",
            "group_search_base",
            "use_tls",
            "port",
            "method"
        ]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        urls=dict(type="list", elements="str", required=True),
        base_dn=dict(type="str", required=True),
        bind_dn=dict(type="str"),
        bind_password=dict(type="str", no_log=True),
        user_search_base=dict(type="str"),
        group_search_base=dict(type="str"),
        use_tls=dict(type="bool", default=True),
        port=dict(type="int", default=389),
        method=dict(type="str", choices=["simple", "sasl"]),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastLdap(module).run()


if __name__ == "__main__":
    main()
