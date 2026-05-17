# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data BGP configuration."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_bgp_config
short_description: Manage VAST Data BGP routing configuration
description:
    - Create, update, and delete BGP routing configurations on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the BGP configuration.
        type: str
        required: true
    local_as:
        description:
            - Local Autonomous System number.
        type: int
        required: true
    peer_as:
        description:
            - Peer Autonomous System number.
        type: int
        required: true
    peer_ip:
        description:
            - IP address of the BGP peer.
        type: str
        required: true
    router_id:
        description:
            - Router ID for BGP.
        type: str
    hold_timer:
        description:
            - BGP hold timer in seconds.
        type: int
        default: 90
    keepalive_interval:
        description:
            - BGP keepalive interval in seconds.
        type: int
        default: 30
    enabled:
        description:
            - Whether the BGP configuration is enabled.
        type: bool
        default: true
    state:
        description:
            - The desired state of the BGP configuration.
        type: str
        default: present
        choices: [present, absent]
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
- name: Create BGP configuration
  stevefulme1.vastdata.vast_bgp_config:
    name: primary-bgp
    local_as: 65001
    peer_as: 65002
    peer_ip: 10.0.0.1
    router_id: 10.0.0.2
    hold_timer: 90
    keepalive_interval: 30
    enabled: true
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
    validate_certs: true

- name: Update BGP configuration timers
  stevefulme1.vastdata.vast_bgp_config:
    name: primary-bgp
    local_as: 65001
    peer_as: 65002
    peer_ip: 10.0.0.1
    hold_timer: 180
    keepalive_interval: 60
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Delete BGP configuration
  stevefulme1.vastdata.vast_bgp_config:
    name: primary-bgp
    state: absent
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
"""

RETURN = r"""
resource:
    description: Details of the BGP configuration.
    returned: on success
    type: dict
    sample:
        id: 1
        name: primary-bgp
        local_as: 65001
        peer_as: 65002
        peer_ip: 10.0.0.1
        router_id: 10.0.0.2
        hold_timer: 90
        keepalive_interval: 30
        enabled: true
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastBgpConfig(VastResourceBase):
    resource_path = "/api/bgp/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "local_as",
            "peer_as",
            "peer_ip",
            "router_id",
            "hold_timer",
            "keepalive_interval",
            "enabled"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["local_as", "peer_as", "peer_ip", "router_id", "hold_timer", "keepalive_interval", "enabled"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        local_as=dict(type="int", required=True),
        peer_as=dict(type="int", required=True),
        peer_ip=dict(type="str", required=True),
        router_id=dict(type="str"),
        hold_timer=dict(type="int", default=90),
        keepalive_interval=dict(type="int", default=30),
        enabled=dict(type="bool", default=True),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastBgpConfig(module).run()


if __name__ == "__main__":
    main()
