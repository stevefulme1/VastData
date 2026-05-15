# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for querying VAST Data protection policies."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_protection_policy_info
short_description: Query VAST Data protection policies
description:
    - Retrieve protection policy information from a VAST Data cluster.
    - Returns a list of protection policies with schedule and retention details.
    - Optionally filter results by policy name.
    - This is a read-only info module; it does not modify any resources.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Filter protection policies by name. If not specified, all
              policies are returned.
        type: str
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Get all protection policies
  stevefulme1.vastdata.vast_protection_policy_info:
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: policy_info

- name: Get a specific protection policy by name
  stevefulme1.vastdata.vast_protection_policy_info:
    name: daily-backup-policy
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: policy_info
"""

RETURN = r"""
policies:
    description: List of protection policy objects returned by the API.
    returned: on success
    type: list
    elements: dict
    sample: [
        {
            "id": 1,
            "name": "daily-backup-policy",
            "schedule": "0 2 * * *",
            "retention": 30,
            "enabled": true
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
        policies = client.get("/api/protectionpolicies/")
        if not isinstance(policies, list):
            policies = [policies] if policies else []
    except Exception as e:
        module.fail_json(msg=f"Failed to query protection policies: {e}")
        return

    name = module.params.get("name")
    if name:
        policies = [p for p in policies if p.get("name") == name]

    module.exit_json(changed=False, policies=policies)


if __name__ == "__main__":
    main()
