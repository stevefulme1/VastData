# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data block storage hosts."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_block_host
short_description: Manage VAST Data block storage host entries
description:
    - Create, update, and delete block storage host entries on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the block host.
        type: str
        required: true
    iqn:
        description:
            - iSCSI Qualified Name for iSCSI hosts.
        type: str
    nqn:
        description:
            - NVMe Qualified Name for NVMe hosts.
        type: str
    host_type:
        description:
            - Type of block storage host.
        type: str
        choices: [ISCSI, NVME]
    tenant_id:
        description:
            - Tenant ID for the block host.
        type: int
    state:
        description:
            - The desired state of the block host.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Create iSCSI block host
  stevefulme1.vastdata.vast_block_host:
    name: iscsi-host-01
    iqn: iqn.1994-05.com.example:server01
    host_type: ISCSI
    state: present

- name: Create NVMe block host
  stevefulme1.vastdata.vast_block_host:
    name: nvme-host-01
    nqn: nqn.2014-08.org.nvmexpress:uuid:12345678-1234-1234-1234-123456789012
    host_type: NVME
    state: present

- name: Delete block host
  stevefulme1.vastdata.vast_block_host:
    name: iscsi-host-01
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the block host.
    returned: on success
    type: dict
    sample:
        id: 1
        name: iscsi-host-01
        iqn: iqn.1994-05.com.example:server01
        host_type: ISCSI
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastBlockHost(VastResourceBase):
    resource_path = "/api/blockhosts/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "iqn",
            "nqn",
            "host_type",
            "tenant_id"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["iqn", "nqn", "host_type", "tenant_id"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        iqn=dict(type="str"),
        nqn=dict(type="str"),
        host_type=dict(type="str", choices=["ISCSI", "NVME"]),
        tenant_id=dict(type="int"),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastBlockHost(module).run()


if __name__ == "__main__":
    main()
