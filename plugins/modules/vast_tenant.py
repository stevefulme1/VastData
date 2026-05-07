# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data tenants."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_tenant
short_description: Manage VAST Data tenants
description:
    - Create, update, and delete tenants on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - The name of the tenant.
        type: str
        required: true
    smb_privileged_user_name:
        description:
            - SMB privileged user name.
        type: str
    smb_administrator_name:
        description:
            - SMB administrator name.
        type: str
    default_others_share_level:
        description:
            - Default share level for others.
        type: str
        choices: [NONE, READ, CHANGE, FULL]
    trash_gid:
        description:
            - Trash group ID.
        type: int
    client_ip_ranges:
        description:
            - List of client IP ranges.
        type: list
        elements: dict
        suboptions:
            start_ip:
                description: Start IP address of the range.
                type: str
                required: true
            end_ip:
                description: End IP address of the range.
                type: str
                required: true
    posix_primary_provider:
        description:
            - Primary POSIX provider.
        type: str
        choices: [LDAP, AD, NIS, LOCAL]
    state:
        description:
            - The desired state of the tenant.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Create a new tenant
  stevefulme1.vastdata.vast_tenant:
    name: production
    smb_privileged_user_name: admin
    default_others_share_level: READ
    posix_primary_provider: LDAP
    client_ip_ranges:
      - start_ip: 10.0.0.1
        end_ip: 10.0.0.255
    state: present

- name: Update tenant settings
  stevefulme1.vastdata.vast_tenant:
    name: production
    default_others_share_level: CHANGE
    trash_gid: 1000
    state: present

- name: Delete a tenant
  stevefulme1.vastdata.vast_tenant:
    name: production
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the tenant.
    returned: on success
    type: dict
    sample:
        id: 1
        name: production
        smb_privileged_user_name: admin
        default_others_share_level: READ
        posix_primary_provider: LDAP
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastTenant(VastResourceBase):
    resource_path = "/api/tenants/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "smb_privileged_user_name",
            "smb_administrator_name",
            "default_others_share_level",
            "trash_gid",
            "client_ip_ranges",
            "posix_primary_provider"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return [
            "smb_privileged_user_name",
            "smb_administrator_name",
            "default_others_share_level",
            "trash_gid",
            "client_ip_ranges",
            "posix_primary_provider"
        ]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        smb_privileged_user_name=dict(type="str"),
        smb_administrator_name=dict(type="str"),
        default_others_share_level=dict(type="str", choices=["NONE", "READ", "CHANGE", "FULL"]),
        trash_gid=dict(type="int"),
        client_ip_ranges=dict(type="list", elements="dict"),
        posix_primary_provider=dict(type="str", choices=["LDAP", "AD", "NIS", "LOCAL"]),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastTenant(module).run()


if __name__ == "__main__":
    main()
