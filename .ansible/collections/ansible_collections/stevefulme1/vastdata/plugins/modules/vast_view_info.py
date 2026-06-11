# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for querying VAST Data views."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_view_info
short_description: Query VAST Data views
description:
    - Retrieve view information from a VAST Data cluster.
    - Returns a list of views with path, protocols, and policy details.
    - Optionally filter results by view name.
    - This is a read-only info module; it does not modify any resources.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Filter views by name. If not specified, all views are returned.
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
- name: Get all views
  stevefulme1.vastdata.vast_view_info:
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: view_info

- name: Get a specific view by name
  stevefulme1.vastdata.vast_view_info:
    name: my-view
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: view_info
"""

RETURN = r"""
views:
    description: List of view objects returned by the API.
    returned: on success
    type: list
    elements: dict
    sample: [
        {
            "id": 1,
            "name": "my-view",
            "path": "/data/my-view",
            "protocols": ["NFS", "SMB"],
            "policy_id": 1
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
        views = client.get("/api/views/")
        if not isinstance(views, list):
            views = [views] if views else []
    except Exception as e:
        module.fail_json(msg=f"Failed to query views: {e}")
        return

    name = module.params.get("name")
    if name:
        views = [v for v in views if v.get("name") == name]

    module.exit_json(changed=False, views=views)


if __name__ == "__main__":
    main()
