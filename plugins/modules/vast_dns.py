# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data DNS configuration."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_dns
short_description: Manage VAST Data DNS configuration
description:
    - Create, update, and delete DNS configurations on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the DNS configuration.
        type: str
        required: true
    vip_pool_id:
        description:
            - ID of the VIP pool to use for DNS.
        type: int
        required: true
    domain_suffix:
        description:
            - Domain suffix for DNS resolution.
        type: str
    vip_gateway:
        description:
            - Gateway IP address for the VIP pool.
        type: str
    vip_vlan:
        description:
            - VLAN ID for the VIP pool.
        type: int
    state:
        description:
            - The desired state of the DNS configuration.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Create DNS configuration
  stevefulme1.vastdata.vast_dns:
    name: cluster-dns
    vip_pool_id: 1
    domain_suffix: example.com
    vip_gateway: 192.168.1.1
    vip_vlan: 100
    state: present

- name: Update DNS configuration domain suffix
  stevefulme1.vastdata.vast_dns:
    name: cluster-dns
    vip_pool_id: 1
    domain_suffix: corp.example.com
    vip_gateway: 192.168.1.1
    vip_vlan: 100
    state: present

- name: Delete DNS configuration
  stevefulme1.vastdata.vast_dns:
    name: cluster-dns
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the DNS configuration.
    returned: on success
    type: dict
    sample:
        id: 1
        name: cluster-dns
        vip_pool_id: 1
        domain_suffix: example.com
        vip_gateway: 192.168.1.1
        vip_vlan: 100
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastDns(VastResourceBase):
    resource_path = "/api/dns/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "vip_pool_id",
            "domain_suffix",
            "vip_gateway",
            "vip_vlan"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["vip_pool_id", "domain_suffix", "vip_gateway", "vip_vlan"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        vip_pool_id=dict(type="int", required=True),
        domain_suffix=dict(type="str"),
        vip_gateway=dict(type="str"),
        vip_vlan=dict(type="int"),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastDns(module).run()


if __name__ == "__main__":
    main()
