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
extends_documentation_fragment:
    - vastdata.cluster.vast_common
"""

EXAMPLES = r"""
- name: Create block host to volume mapping
  vastdata.cluster.vast_block_host_mapping:
    host_id: 1
    volume_id: 5
    lun: 0
    state: present

- name: Update block host mapping LUN
  vastdata.cluster.vast_block_host_mapping:
    host_id: 1
    volume_id: 5
    lun: 1
    state: present

- name: Delete block host mapping
  vastdata.cluster.vast_block_host_mapping:
    host_id: 1
    volume_id: 5
    state: absent
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
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource import VastResourceBase


class VastBlockHostMapping(VastResourceBase):
    resource_path = "/api/blockhostmappings/"

    def get_resource(self):
        return self._get_by_name()

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
