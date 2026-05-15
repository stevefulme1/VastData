# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for querying VAST Data quotas."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_quota_info
short_description: Query VAST Data quotas
description:
    - Retrieve quota information from a VAST Data cluster.
    - Returns a list of quotas with name, path, limits, and usage details.
    - Optionally filter results by quota name.
    - This is a read-only info module; it does not modify any resources.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Filter quotas by name. If not specified, all quotas are returned.
        type: str
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Get all quotas
  stevefulme1.vastdata.vast_quota_info:
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: quota_info

- name: Get a specific quota by name
  stevefulme1.vastdata.vast_quota_info:
    name: project-quota
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: quota_info
"""

RETURN = r"""
quotas:
    description: List of quota objects returned by the API.
    returned: on success
    type: list
    elements: dict
    sample: [
        {
            "id": 1,
            "name": "project-quota",
            "path": "/data/projects",
            "hard_limit": 1099511627776,
            "soft_limit": 824633720832,
            "used_capacity": 549755813888
        }
    ]
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_client import get_vast_client


def main():
    module_args = dict(
        name=dict(type="str"),
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    client = get_vast_client(module)

    try:
        quotas = client.get("/api/quotas/")
        if not isinstance(quotas, list):
            quotas = [quotas] if quotas else []
    except Exception as e:
        module.fail_json(msg=f"Failed to query quotas: {e}")
        return

    name = module.params.get("name")
    if name:
        quotas = [q for q in quotas if q.get("name") == name]

    module.exit_json(changed=False, quotas=quotas)


if __name__ == "__main__":
    main()
