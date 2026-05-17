# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for querying VAST Data CNode information."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_cnode_info
short_description: Query VAST Data CNode information
description:
    - Retrieve CNode (compute node) information from a VAST Data cluster.
    - Returns a list of CNodes with name, IP, state, cores, memory, and
      OS version details.
    - Optionally filter results by CNode name.
    - This is a read-only info module; it does not modify any resources.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Filter CNodes by name. If not specified, all CNodes are returned.
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
- name: Get all CNodes
  stevefulme1.vastdata.vast_cnode_info:
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: cnode_info

- name: Get a specific CNode by name
  stevefulme1.vastdata.vast_cnode_info:
    name: cnode-1
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: cnode_info
"""

RETURN = r"""
cnodes:
    description: List of CNode objects returned by the API.
    returned: on success
    type: list
    elements: dict
    sample: [
        {
            "id": 1,
            "name": "cnode-1",
            "ip": "10.0.0.101",
            "state": "ONLINE",
            "cores": 32,
            "memory": 131072,
            "os_version": "5.15.0-vast"
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
        cnodes = client.get("/api/cnodes/")
        if not isinstance(cnodes, list):
            cnodes = [cnodes] if cnodes else []
    except Exception as e:
        module.fail_json(msg=f"Failed to query CNodes: {e}")
        return

    name = module.params.get("name")
    if name:
        cnodes = [c for c in cnodes if c.get("name") == name]

    module.exit_json(changed=False, cnodes=cnodes)


if __name__ == "__main__":
    main()
