# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for querying VAST Data cluster capacity and usage."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_capacity_info
short_description: Query VAST Data cluster capacity and usage
description:
    - Retrieve capacity and usage information from a VAST Data cluster.
    - Returns total physical, total logical, used physical, used logical,
      free capacity, and data reduction ratio.
    - This is a read-only info module; it does not modify any resources.
version_added: "1.0.0"
author: VAST Data (@vast-data)
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
options:
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
- name: Get cluster capacity
  stevefulme1.vastdata.vast_capacity_info:
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: capacity_info

- name: Display free capacity
  ansible.builtin.debug:
    msg: "Free capacity: {{ capacity_info.capacity.free }}"
"""

RETURN = r"""
capacity:
    description: Capacity and usage information returned by the API.
    returned: on success
    type: dict
    sample: {
        "total_physical": 1099511627776,
        "total_logical": 2199023255552,
        "used_physical": 549755813888,
        "used_logical": 1099511627776,
        "free": 549755813888,
        "data_reduction_ratio": 2.0
    }
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_client import get_vast_client


def main():
    module_args = dict(
        limit=dict(type='int', default=100),
        offset=dict(type='int', default=0),
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    client = get_vast_client(module)

    try:
        capacity = client.get("/api/capacity/")
        if isinstance(capacity, list):
            capacity = capacity[0] if capacity else {}
    except Exception as e:
        module.fail_json(msg="Failed to query capacity information: {0}".format(e))
        return

    module.exit_json(changed=False, capacity=capacity)


if __name__ == "__main__":
    main()
