# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data network interfaces and bonds."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_network_interface
short_description: Manage VAST Data network interfaces and bonds
description:
    - Create, update, and delete network interfaces and bond configurations
      on a VAST Data cluster.
    - Supports configuring IP addressing, MTU, and bond modes.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the network interface or bond.
        type: str
        required: true
    ip:
        description:
            - IP address to assign to the interface.
        type: str
    subnet_mask:
        description:
            - Subnet mask for the interface (e.g. 255.255.255.0).
        type: str
    gateway:
        description:
            - Default gateway for the interface.
        type: str
    mtu:
        description:
            - Maximum transmission unit size.
        type: int
    bond_mode:
        description:
            - Bonding mode when creating a bonded interface.
        type: str
        choices: [active-backup, balance-tcp, balance-alb]
    slaves:
        description:
            - List of physical NIC names to include in the bond.
        type: list
        elements: str
    state:
        description:
            - The desired state of the network interface.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Create a network interface
  stevefulme1.vastdata.vast_network_interface:
    name: eth0
    ip: 10.0.0.10
    subnet_mask: 255.255.255.0
    gateway: 10.0.0.1
    mtu: 9000
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Create a bonded interface
  stevefulme1.vastdata.vast_network_interface:
    name: bond0
    ip: 10.0.0.20
    subnet_mask: 255.255.255.0
    gateway: 10.0.0.1
    bond_mode: active-backup
    slaves:
      - eth0
      - eth1
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Delete a network interface
  stevefulme1.vastdata.vast_network_interface:
    name: bond0
    state: absent
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
"""

RETURN = r"""
resource:
    description: Details of the network interface.
    returned: on success
    type: dict
    sample:
        id: 1
        name: bond0
        ip: 10.0.0.20
        subnet_mask: 255.255.255.0
        gateway: 10.0.0.1
        mtu: 9000
        bond_mode: active-backup
        slaves: ["eth0", "eth1"]
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastNetworkInterface(VastResourceBase):
    resource_path = "/api/networkinterfaces/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "ip",
            "subnet_mask",
            "gateway",
            "mtu",
            "bond_mode",
            "slaves",
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["ip", "subnet_mask", "gateway", "mtu", "bond_mode", "slaves"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        ip=dict(type="str"),
        subnet_mask=dict(type="str"),
        gateway=dict(type="str"),
        mtu=dict(type="int"),
        bond_mode=dict(type="str", choices=["active-backup", "balance-tcp", "balance-alb"]),
        slaves=dict(type="list", elements="str"),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastNetworkInterface(module).run()


if __name__ == "__main__":
    main()
