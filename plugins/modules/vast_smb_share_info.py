# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for querying VAST Data SMB shares."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_smb_share_info
short_description: Query VAST Data SMB shares
description:
    - Retrieve SMB share information from a VAST Data cluster.
    - Returns a list of SMB shares with name, path, and access details.
    - Optionally filter results by share name.
    - This is a read-only info module; it does not modify any resources.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Filter SMB shares by name. If not specified, all shares are
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
- name: Get all SMB shares
  stevefulme1.vastdata.vast_smb_share_info:
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: share_info

- name: Get a specific SMB share by name
  stevefulme1.vastdata.vast_smb_share_info:
    name: project-share
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: share_info
"""

RETURN = r"""
shares:
    description: List of SMB share objects returned by the API.
    returned: on success
    type: list
    elements: dict
    sample: [
        {
            "id": 1,
            "name": "project-share",
            "path": "/data/projects",
            "share_acl": "Everyone:FULL"
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
        shares = client.get("/api/smbshares/")
        if not isinstance(shares, list):
            shares = [shares] if shares else []
    except Exception as e:
        module.fail_json(msg="Failed to query SMB shares: {0}".format(e))
        return

    name = module.params.get("name")
    if name:
        shares = [s for s in shares if s.get("name") == name]

    module.exit_json(changed=False, shares=shares)


if __name__ == "__main__":
    main()
