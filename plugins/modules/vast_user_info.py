# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for querying VAST Data users."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_user_info
short_description: Query VAST Data users
description:
    - Retrieve user information from a VAST Data cluster.
    - Returns a list of users with name, UID, and group membership details.
    - Optionally filter results by user name.
    - This is a read-only info module; it does not modify any resources.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Filter users by name. If not specified, all users are returned.
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
- name: Get all users
  stevefulme1.vastdata.vast_user_info:
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: user_info

- name: Get a specific user by name
  stevefulme1.vastdata.vast_user_info:
    name: admin
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: user_info
"""

RETURN = r"""
users:
    description: List of user objects returned by the API.
    returned: on success
    type: list
    elements: dict
    sample: [
        {
            "id": 1,
            "name": "admin",
            "uid": 0,
            "groups": ["admins"]
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
        users = client.get("/api/users/")
        if not isinstance(users, list):
            users = [users] if users else []
    except Exception as e:
        module.fail_json(msg=f"Failed to query users: {e}")
        return

    name = module.params.get("name")
    if name:
        users = [u for u in users if u.get("name") == name]

    module.exit_json(changed=False, users=users)


if __name__ == "__main__":
    main()
