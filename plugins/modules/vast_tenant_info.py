# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for querying VAST Data tenants."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_tenant_info
short_description: Query VAST Data tenants
description:
    - Retrieve tenant information from a VAST Data cluster.
    - Returns a list of tenants with name, ID, and configuration details.
    - Optionally filter results by tenant name.
    - This is a read-only info module; it does not modify any resources.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Filter tenants by name. If not specified, all tenants are
              returned.
        type: str
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
- name: Get all tenants
  stevefulme1.vastdata.vast_tenant_info:
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: tenant_info

- name: Get a specific tenant by name
  stevefulme1.vastdata.vast_tenant_info:
    name: engineering
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: tenant_info
"""

RETURN = r"""
tenants:
    description: List of tenant objects returned by the API.
    returned: on success
    type: list
    elements: dict
    sample: [
        {
            "id": 1,
            "name": "engineering",
            "client_ip_ranges": "10.0.0.0/16"
        }
    ]
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_client import get_vast_client


def main():
    module_args = dict(
        limit=dict(type='int', default=100),
        offset=dict(type='int', default=0),
        name=dict(type="str"),
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    client = get_vast_client(module)

    try:
        tenants = client.get("/api/tenants/")
        if not isinstance(tenants, list):
            tenants = [tenants] if tenants else []
    except Exception as e:
        module.fail_json(msg=f"Failed to query tenants: {e}")
        return

    name = module.params.get("name")
    if name:
        tenants = [t for t in tenants if t.get("name") == name]

    module.exit_json(changed=False, tenants=tenants)


if __name__ == "__main__":
    main()
