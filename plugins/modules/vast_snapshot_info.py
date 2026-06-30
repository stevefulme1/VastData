# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for querying VAST Data snapshots."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_snapshot_info
short_description: Query VAST Data snapshots
description:
    - Retrieve snapshot information from a VAST Data cluster.
    - Returns a list of snapshots with name, path, and creation details.
    - Optionally filter results by snapshot name.
    - This is a read-only info module; it does not modify any resources.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Filter snapshots by name. If not specified, all snapshots are
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
- name: Get all snapshots
  stevefulme1.vastdata.vast_snapshot_info:
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: snapshot_info

- name: Get a specific snapshot by name
  stevefulme1.vastdata.vast_snapshot_info:
    name: daily-backup
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: snapshot_info
"""

RETURN = r"""
snapshots:
    description: List of snapshot objects returned by the API.
    returned: on success
    type: list
    elements: dict
    sample: [
        {
            "id": 1,
            "name": "daily-backup",
            "path": "/data/projects",
            "created_at": "2025-01-15T08:00:00Z",
            "size": 1099511627776
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
        snapshots = client.get("/api/snapshots/")
        if not isinstance(snapshots, list):
            snapshots = [snapshots] if snapshots else []
    except Exception as e:
        module.fail_json(msg="Failed to query snapshots: {0}".format(e))
        return

    name = module.params.get("name")
    if name:
        snapshots = [s for s in snapshots if s.get("name") == name]

    module.exit_json(changed=False, snapshots=snapshots)


if __name__ == "__main__":
    main()
