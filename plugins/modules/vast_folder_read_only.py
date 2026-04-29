# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data Folder Read-Only Flags."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_folder_read_only
short_description: Manage VAST Data folder read-only flags
description:
    - Create, update, and delete folder read-only flags on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    path:
        description:
            - The filesystem path of the folder.
        type: str
        required: true
    is_read_only:
        description:
            - Whether the folder should be read-only.
        type: bool
        required: true
    tenant_id:
        description:
            - ID of the tenant this folder belongs to.
        type: int
    state:
        description:
            - The desired state of the folder read-only flag.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - vastdata.cluster.vast_common
"""

EXAMPLES = r"""
- name: Set folder to read-only
  vastdata.cluster.vast_folder_read_only:
    path: /data/archive
    is_read_only: true
    tenant_id: 1
    state: present

- name: Remove read-only flag from folder
  vastdata.cluster.vast_folder_read_only:
    path: /data/archive
    is_read_only: false
    state: present

- name: Delete folder read-only configuration
  vastdata.cluster.vast_folder_read_only:
    path: /data/archive
    is_read_only: true
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the folder read-only configuration.
    returned: on success
    type: dict
    sample:
        id: 1
        path: /data/archive
        is_read_only: true
        tenant_id: 1
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource import VastResourceBase


class VastFolderReadOnly(VastResourceBase):
    resource_path = "/api/folders/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in ["path", "is_read_only", "tenant_id"] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["is_read_only"]


def main():
    module_args = dict(
        path=dict(type="str", required=True),
        is_read_only=dict(type="bool", required=True),
        tenant_id=dict(type="int"),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastFolderReadOnly(module).run()


if __name__ == "__main__":
    main()
