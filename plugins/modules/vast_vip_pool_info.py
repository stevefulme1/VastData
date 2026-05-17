# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for querying VAST Data VIP pools."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_vip_pool_info
short_description: Query VAST Data VIP pools
description:
    - Retrieve VIP pool information from a VAST Data cluster.
    - Returns a list of VIP pools with name, subnet, and IP range details.
    - Optionally filter results by VIP pool name.
    - This is a read-only info module; it does not modify any resources.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Filter VIP pools by name. If not specified, all VIP pools are
              returned.
        type: str
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
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
"""

EXAMPLES = r"""
- name: Get all VIP pools
  stevefulme1.vastdata.vast_vip_pool_info:
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: vip_pool_info

- name: Get a specific VIP pool by name
  stevefulme1.vastdata.vast_vip_pool_info:
    name: data-pool
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: vip_pool_info
"""

RETURN = r"""
vip_pools:
    description: List of VIP pool objects returned by the API.
    returned: on success
    type: list
    elements: dict
    sample: [
        {
            "id": 1,
            "name": "data-pool",
            "subnet": "10.0.1.0/24",
            "ip_ranges": [["10.0.1.100", "10.0.1.200"]],
            "vlan": 100
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
        vip_pools = client.get("/api/vippools/")
        if not isinstance(vip_pools, list):
            vip_pools = [vip_pools] if vip_pools else []
    except Exception as e:
        module.fail_json(msg=f"Failed to query VIP pools: {e}")
        return

    name = module.params.get("name")
    if name:
        vip_pools = [v for v in vip_pools if v.get("name") == name]

    module.exit_json(changed=False, vip_pools=vip_pools)


if __name__ == "__main__":
    main()
