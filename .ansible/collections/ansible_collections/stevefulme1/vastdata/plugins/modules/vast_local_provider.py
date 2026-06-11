# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data local authentication provider settings."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_local_provider
short_description: Manage VAST Data local authentication provider settings
description:
    - Create, update, and delete local authentication provider settings on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the local authentication provider.
        type: str
        required: true
    min_uid:
        description:
            - Minimum user ID for local users.
        type: int
    max_uid:
        description:
            - Maximum user ID for local users.
        type: int
    min_gid:
        description:
            - Minimum group ID for local groups.
        type: int
    max_gid:
        description:
            - Maximum group ID for local groups.
        type: int
    enabled:
        description:
            - Whether the local authentication provider is enabled.
        type: bool
        default: true
    state:
        description:
            - The desired state of the local authentication provider.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Create local authentication provider
  stevefulme1.vastdata.vast_local_provider:
    name: local_auth
    min_uid: 1000
    max_uid: 65535
    min_gid: 1000
    max_gid: 65535
    enabled: true
    state: present
    vms_host: vast.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Update local authentication provider
  stevefulme1.vastdata.vast_local_provider:
    name: local_auth
    min_uid: 2000
    max_uid: 99999
    min_gid: 2000
    max_gid: 99999
    enabled: true
    state: present
    vms_host: vast.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Delete local authentication provider
  stevefulme1.vastdata.vast_local_provider:
    name: local_auth
    state: absent
    vms_host: vast.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
"""

RETURN = r"""
resource:
    description: Details of the local authentication provider.
    returned: on success
    type: dict
    sample:
        id: 1
        name: local_auth
        min_uid: 1000
        max_uid: 65535
        min_gid: 1000
        max_gid: 65535
        enabled: true
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastLocalProvider(VastResourceBase):
    resource_path = "/api/localprovider/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "min_uid",
            "max_uid",
            "min_gid",
            "max_gid",
            "enabled"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["min_uid", "max_uid", "min_gid", "max_gid", "enabled"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        min_uid=dict(type="int"),
        max_uid=dict(type="int"),
        min_gid=dict(type="int"),
        max_gid=dict(type="int"),
        enabled=dict(type="bool", default=True),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastLocalProvider(module).run()


if __name__ == "__main__":
    main()
