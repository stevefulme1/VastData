# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data VIP pools."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_vip_pool
short_description: Manage VAST Data VIP pools
description:
    - Create, update, and delete VIP pools on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the VIP pool.
        type: str
        required: true
    subnet_cidr:
        description:
            - IPv4 subnet CIDR prefix length.
        type: int
        required: true
    subnet_cidr_ipv6:
        description:
            - IPv6 subnet CIDR prefix length.
        type: int
    ip_ranges:
        description:
            - List of IP address ranges in the pool.
        type: list
        elements: dict
        suboptions:
            start_ip:
                description: Starting IP address of the range.
                type: str
                required: true
            end_ip:
                description: Ending IP address of the range.
                type: str
                required: true
    role:
        description:
            - Role of the VIP pool.
        type: str
        choices: [PROTOCOLS, REPLICATION, MANAGEMENT]
    domain_name:
        description:
            - Domain name for the VIP pool.
        type: str
    vlan:
        description:
            - VLAN ID for the VIP pool.
        type: int
    tenant_id:
        description:
            - Tenant ID for the VIP pool.
        type: int
    enabled:
        description:
            - Whether the VIP pool is enabled.
        type: bool
        default: true
    state:
        description:
            - The desired state of the VIP pool.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - vastdata.cluster.vast_common
"""

EXAMPLES = r"""
- name: Create a VIP pool for protocols
  vastdata.cluster.vast_vip_pool:
    name: protocols-vip-pool
    subnet_cidr: 24
    ip_ranges:
      - start_ip: 192.168.1.10
        end_ip: 192.168.1.20
    role: PROTOCOLS
    vlan: 100
    enabled: true
    state: present

- name: Update VIP pool with additional IP range
  vastdata.cluster.vast_vip_pool:
    name: protocols-vip-pool
    subnet_cidr: 24
    ip_ranges:
      - start_ip: 192.168.1.10
        end_ip: 192.168.1.30
    role: PROTOCOLS
    vlan: 100
    enabled: true
    state: present

- name: Delete a VIP pool
  vastdata.cluster.vast_vip_pool:
    name: protocols-vip-pool
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the VIP pool.
    returned: on success
    type: dict
    sample:
        id: 1
        name: protocols-vip-pool
        subnet_cidr: 24
        role: PROTOCOLS
        vlan: 100
        enabled: true
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource import VastResourceBase

class VastVipPool(VastResourceBase):
    resource_path = "/api/vippools/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in ["name", "subnet_cidr", "subnet_cidr_ipv6", "ip_ranges", "role", "domain_name", "vlan", "tenant_id", "enabled"] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["subnet_cidr", "subnet_cidr_ipv6", "ip_ranges", "role", "domain_name", "vlan", "tenant_id", "enabled"]

def main():
    module_args = dict(
        name=dict(type="str", required=True),
        subnet_cidr=dict(type="int", required=True),
        subnet_cidr_ipv6=dict(type="int"),
        ip_ranges=dict(type="list", elements="dict"),
        role=dict(type="str", choices=["PROTOCOLS", "REPLICATION", "MANAGEMENT"]),
        domain_name=dict(type="str"),
        vlan=dict(type="int"),
        tenant_id=dict(type="int"),
        enabled=dict(type="bool", default=True),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastVipPool(module).run()

if __name__ == "__main__":
    main()
