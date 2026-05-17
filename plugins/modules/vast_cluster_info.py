# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for querying VAST Data cluster health and status."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_cluster_info
short_description: Query VAST Data cluster health and status
description:
    - Retrieve cluster health and status information from a VAST Data cluster.
    - Returns cluster name, state, build version, PSNT, leader CNode, and
      upgrade state.
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
- name: Get cluster status
  stevefulme1.vastdata.vast_cluster_info:
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: cluster_info

- name: Display cluster state
  ansible.builtin.debug:
    msg: "Cluster {{ cluster_info.clusters[0].name }} is {{ cluster_info.clusters[0].state }}"
"""

RETURN = r"""
clusters:
    description: List of cluster objects returned by the API.
    returned: on success
    type: list
    elements: dict
    sample: [
        {
            "name": "vast-cluster-01",
            "state": "ONLINE",
            "build": "5.1.0.42",
            "psnt": "ABC123",
            "leader_cnode": "cnode-1",
            "upgrade_state": "IDLE"
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
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    client = get_vast_client(module)

    try:
        clusters = client.get("/api/clusters/")
        if not isinstance(clusters, list):
            clusters = [clusters]
    except Exception as e:
        module.fail_json(msg=f"Failed to query cluster status: {e}")
        return

    module.exit_json(changed=False, clusters=clusters)


if __name__ == "__main__":
    main()
