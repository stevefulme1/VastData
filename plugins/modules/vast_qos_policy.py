# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data QoS policies."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_qos_policy
short_description: Manage VAST Data Quality of Service policies
description:
    - Create, update, and delete QoS policies on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the QoS policy.
        type: str
        required: true
    max_reads_bw_mbps:
        description:
            - Maximum read bandwidth in MB/s.
        type: int
    max_writes_bw_mbps:
        description:
            - Maximum write bandwidth in MB/s.
        type: int
    max_reads_iops:
        description:
            - Maximum read IOPS.
        type: int
    max_writes_iops:
        description:
            - Maximum write IOPS.
        type: int
    burst_reads_bw_mbps:
        description:
            - Burst read bandwidth in MB/s.
        type: int
    burst_writes_bw_mbps:
        description:
            - Burst write bandwidth in MB/s.
        type: int
    burst_reads_iops:
        description:
            - Burst read IOPS.
        type: int
    burst_writes_iops:
        description:
            - Burst write IOPS.
        type: int
    mode:
        description:
            - QoS policy mode.
        type: str
        choices: [STATIC, USED_CAPACITY, PROVISIONED_CAPACITY]
    tenant_id:
        description:
            - Tenant ID for the QoS policy.
        type: int
    state:
        description:
            - The desired state of the QoS policy.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Create QoS policy with bandwidth limits
  stevefulme1.vastdata.vast_qos_policy:
    name: production-qos
    max_reads_bw_mbps: 1000
    max_writes_bw_mbps: 800
    max_reads_iops: 50000
    max_writes_iops: 40000
    burst_reads_bw_mbps: 1500
    burst_writes_bw_mbps: 1200
    mode: STATIC
    state: present

- name: Update QoS policy limits
  stevefulme1.vastdata.vast_qos_policy:
    name: production-qos
    max_reads_bw_mbps: 2000
    max_writes_bw_mbps: 1600
    mode: STATIC
    state: present

- name: Delete QoS policy
  stevefulme1.vastdata.vast_qos_policy:
    name: production-qos
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the QoS policy.
    returned: on success
    type: dict
    sample:
        id: 1
        name: production-qos
        max_reads_bw_mbps: 1000
        max_writes_bw_mbps: 800
        max_reads_iops: 50000
        max_writes_iops: 40000
        mode: STATIC
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastQosPolicy(VastResourceBase):
    resource_path = "/api/qospolicies/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "max_reads_bw_mbps",
            "max_writes_bw_mbps",
            "max_reads_iops",
            "max_writes_iops",
            "burst_reads_bw_mbps",
            "burst_writes_bw_mbps",
            "burst_reads_iops",
            "burst_writes_iops",
            "mode",
            "tenant_id"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return [
            "max_reads_bw_mbps",
            "max_writes_bw_mbps",
            "max_reads_iops",
            "max_writes_iops",
            "burst_reads_bw_mbps",
            "burst_writes_bw_mbps",
            "burst_reads_iops",
            "burst_writes_iops",
            "mode",
            "tenant_id"
        ]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        max_reads_bw_mbps=dict(type="int"),
        max_writes_bw_mbps=dict(type="int"),
        max_reads_iops=dict(type="int"),
        max_writes_iops=dict(type="int"),
        burst_reads_bw_mbps=dict(type="int"),
        burst_writes_bw_mbps=dict(type="int"),
        burst_reads_iops=dict(type="int"),
        burst_writes_iops=dict(type="int"),
        mode=dict(type="str", choices=["STATIC", "USED_CAPACITY", "PROVISIONED_CAPACITY"]),
        tenant_id=dict(type="int"),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastQosPolicy(module).run()


if __name__ == "__main__":
    main()
