# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for querying VAST Data NFS exports."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_nfs_export_info
short_description: Query VAST Data NFS exports
description:
    - Retrieve NFS export information from a VAST Data cluster.
    - Returns a list of NFS exports with path, permissions, and access details.
    - Optionally filter results by export name.
    - This is a read-only info module; it does not modify any resources.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Filter NFS exports by name. If not specified, all exports are
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
- name: Get all NFS exports
  stevefulme1.vastdata.vast_nfs_export_info:
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: export_info

- name: Get a specific NFS export by name
  stevefulme1.vastdata.vast_nfs_export_info:
    name: data-export
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: export_info
"""

RETURN = r"""
exports:
    description: List of NFS export objects returned by the API.
    returned: on success
    type: list
    elements: dict
    sample: [
        {
            "id": 1,
            "name": "data-export",
            "path": "/data/shared",
            "permissions": "RW",
            "allowed_hosts": "10.0.0.0/24"
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
        exports = client.get("/api/nfsexports/")
        if not isinstance(exports, list):
            exports = [exports] if exports else []
    except Exception as e:
        module.fail_json(msg=f"Failed to query NFS exports: {e}")
        return

    name = module.params.get("name")
    if name:
        exports = [e for e in exports if e.get("name") == name]

    module.exit_json(changed=False, exports=exports)


if __name__ == "__main__":
    main()
