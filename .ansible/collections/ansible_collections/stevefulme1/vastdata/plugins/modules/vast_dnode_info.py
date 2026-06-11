# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for querying VAST Data DNode information."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_dnode_info
short_description: Query VAST Data DNode information
description:
    - Retrieve DNode (data node) information from a VAST Data cluster.
    - Returns a list of DNodes with name, IP, state, NVRAM state, and
      disk count details.
    - Optionally filter results by DNode name.
    - This is a read-only info module; it does not modify any resources.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Filter DNodes by name. If not specified, all DNodes are returned.
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
- name: Get all DNodes
  stevefulme1.vastdata.vast_dnode_info:
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: dnode_info

- name: Get a specific DNode by name
  stevefulme1.vastdata.vast_dnode_info:
    name: dnode-1
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: dnode_info
"""

RETURN = r"""
dnodes:
    description: List of DNode objects returned by the API.
    returned: on success
    type: list
    elements: dict
    sample: [
        {
            "id": 1,
            "name": "dnode-1",
            "ip": "10.0.0.201",
            "state": "ONLINE",
            "nvram_state": "HEALTHY",
            "ssd_count": 24,
            "hdd_count": 60
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
        dnodes = client.get("/api/dnodes/")
        if not isinstance(dnodes, list):
            dnodes = [dnodes] if dnodes else []
    except Exception as e:
        module.fail_json(msg=f"Failed to query DNodes: {e}")
        return

    name = module.params.get("name")
    if name:
        dnodes = [d for d in dnodes if d.get("name") == name]

    module.exit_json(changed=False, dnodes=dnodes)


if __name__ == "__main__":
    main()
