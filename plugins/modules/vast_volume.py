# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data Volumes."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_volume
short_description: Manage VAST Data block volumes
description:
    - Create, update, and delete block volumes on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - The name of the volume.
        type: str
        required: true
    size:
        description:
            - The size of the volume in bytes.
        type: int
        required: true
    tenant_id:
        description:
            - ID of the tenant this volume belongs to.
        type: int
    path:
        description:
            - The filesystem path for the volume.
        type: str
    state:
        description:
            - The desired state of the volume.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Create a block volume
  stevefulme1.vastdata.vast_volume:
    name: db_volume
    size: 1099511627776
    path: /volumes/db
    tenant_id: 1
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
    validate_certs: true

- name: Update volume size
  stevefulme1.vastdata.vast_volume:
    name: db_volume
    size: 2199023255552
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Delete a volume
  stevefulme1.vastdata.vast_volume:
    name: db_volume
    size: 1099511627776
    state: absent
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
"""

RETURN = r"""
resource:
    description: Details of the volume.
    returned: on success
    type: dict
    sample:
        id: 1
        name: db_volume
        size: 1099511627776
        path: /volumes/db
        tenant_id: 1
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastVolume(VastResourceBase):
    resource_path = "/api/volumes/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "size",
            "tenant_id",
            "path"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["size", "path"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        size=dict(type="int", required=True),
        tenant_id=dict(type="int"),
        path=dict(type="str"),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastVolume(module).run()


if __name__ == "__main__":
    main()
