# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data block host to volume mappings."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_block_host_mapping
short_description: Manage VAST Data block host to volume mappings
description:
    - Create, update, and delete mappings between block hosts and volumes on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    host_id:
        description:
            - ID of the block host to map.
        type: int
        required: true
    volume_id:
        description:
            - ID of the volume to map.
        type: int
        required: true
    lun:
        description:
            - Logical Unit Number for the mapping.
        type: int
    state:
        description:
            - The desired state of the block host mapping.
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
- name: Create block host to volume mapping
  stevefulme1.vastdata.vast_block_host_mapping:
    host_id: 1
    volume_id: 5
    lun: 0
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
    validate_certs: true

- name: Update block host mapping LUN
  stevefulme1.vastdata.vast_block_host_mapping:
    host_id: 1
    volume_id: 5
    lun: 1
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Delete block host mapping
  stevefulme1.vastdata.vast_block_host_mapping:
    host_id: 1
    volume_id: 5
    state: absent
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
"""

RETURN = r"""
resource:
    description: Details of the block host mapping.
    returned: on success
    type: dict
    sample:
        id: 1
        host_id: 1
        volume_id: 5
        lun: 0
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastBlockHostMapping(VastResourceBase):
    resource_path = "/api/blockhostmappings/"

    def get_resource(self):
        """Look up mapping by host_id + volume_id composite key."""
        host_id = self.module.params["host_id"]
        volume_id = self.module.params["volume_id"]
        try:
            resources = self.client.get(self.resource_path)
            if isinstance(resources, list):
                for r in resources:
                    if r.get("host_id") == host_id and r.get("volume_id") == volume_id:
                        return r
        except Exception:
            pass
        return None

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "host_id",
            "volume_id",
            "lun"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["lun"]


def main():
    module_args = dict(
        host_id=dict(type="int", required=True),
        volume_id=dict(type="int", required=True),
        lun=dict(type="int"),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastBlockHostMapping(module).run()


if __name__ == "__main__":
    main()
