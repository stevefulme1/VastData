# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for querying VAST Data groups."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_group_info
short_description: Query VAST Data groups
description:
    - Retrieve group information from a VAST Data cluster.
    - Returns a list of groups with name, GID, and member details.
    - Optionally filter results by group name.
    - This is a read-only info module; it does not modify any resources.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Filter groups by name. If not specified, all groups are returned.
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
- name: Get all groups
  stevefulme1.vastdata.vast_group_info:
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: group_info

- name: Get a specific group by name
  stevefulme1.vastdata.vast_group_info:
    name: admins
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: group_info
"""

RETURN = r"""
groups:
    description: List of group objects returned by the API.
    returned: on success
    type: list
    elements: dict
    sample: [
        {
            "id": 1,
            "name": "admins",
            "gid": 1000,
            "members": ["admin", "operator"]
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
        groups = client.get("/api/groups/")
        if not isinstance(groups, list):
            groups = [groups] if groups else []
    except Exception as e:
        module.fail_json(msg=f"Failed to query groups: {e}")
        return

    name = module.params.get("name")
    if name:
        groups = [g for g in groups if g.get("name") == name]

    module.exit_json(changed=False, groups=groups)


if __name__ == "__main__":
    main()
