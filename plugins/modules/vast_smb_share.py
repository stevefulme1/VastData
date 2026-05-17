# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data SMB shares."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_smb_share
short_description: Manage VAST Data SMB/CIFS shares
description:
    - Create, update, and delete SMB/CIFS shares on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the SMB share.
        type: str
        required: true
    path:
        description:
            - Filesystem path to share.
        type: str
    share_policy:
        description:
            - Name or ID of the share policy to associate.
        type: str
    encryption:
        description:
            - Whether SMB encryption is required for the share.
        type: bool
    access_based_enumeration:
        description:
            - Whether access-based enumeration is enabled.
        type: bool
    state:
        description:
            - The desired state of the SMB share.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Create an SMB share
  stevefulme1.vastdata.vast_smb_share:
    name: finance_share
    path: /data/finance
    encryption: true
    access_based_enumeration: true
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Update SMB share encryption
  stevefulme1.vastdata.vast_smb_share:
    name: finance_share
    path: /data/finance
    encryption: false
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Delete an SMB share
  stevefulme1.vastdata.vast_smb_share:
    name: finance_share
    state: absent
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
"""

RETURN = r"""
resource:
    description: Details of the SMB share.
    returned: on success
    type: dict
    sample: {
        "id": 7,
        "name": "finance_share",
        "path": "/data/finance",
        "encryption": true,
        "access_based_enumeration": true
    }
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastSmbShare(VastResourceBase):
    resource_path = "/api/smbshares/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "path",
            "share_policy",
            "encryption",
            "access_based_enumeration",
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["path", "share_policy", "encryption", "access_based_enumeration"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        path=dict(type="str"),
        share_policy=dict(type="str"),
        encryption=dict(type="bool"),
        access_based_enumeration=dict(type="bool"),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastSmbShare(module).run()


if __name__ == "__main__":
    main()
