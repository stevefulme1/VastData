# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data encryption groups."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_encryption_group
short_description: Manage VAST Data encryption groups
description:
    - Create, update, and delete encryption groups on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - The name of the encryption group.
        type: str
        required: true
    key_id:
        description:
            - The encryption key ID.
        type: str
    kmip_server:
        description:
            - The KMIP server address.
        type: str
    key_status:
        description:
            - The status of the encryption key.
        type: str
        choices: [ACTIVE, PRE_ACTIVE, DEACTIVATED]
    state:
        description:
            - The desired state of the encryption group.
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
- name: Create an encryption group
  stevefulme1.vastdata.vast_encryption_group:
    name: encryption_group_1
    key_id: key-12345
    kmip_server: kmip.example.com
    key_status: ACTIVE
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
    validate_certs: true

- name: Update encryption group key status
  stevefulme1.vastdata.vast_encryption_group:
    name: encryption_group_1
    key_status: PRE_ACTIVE
    state: present
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Delete an encryption group
  stevefulme1.vastdata.vast_encryption_group:
    name: encryption_group_1
    state: absent
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
"""

RETURN = r"""
resource:
    description: Details of the encryption group.
    returned: on success
    type: dict
    sample:
        id: 10
        name: encryption_group_1
        key_id: key-12345
        kmip_server: kmip.example.com
        key_status: ACTIVE
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastEncryptionGroup(VastResourceBase):
    resource_path = "/api/encryptiongroups/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "key_id",
            "kmip_server",
            "key_status"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["key_id", "kmip_server", "key_status"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        key_id=dict(type="str"),
        kmip_server=dict(type="str"),
        key_status=dict(type="str", choices=["ACTIVE", "PRE_ACTIVE", "DEACTIVATED"]),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastEncryptionGroup(module).run()


if __name__ == "__main__":
    main()
