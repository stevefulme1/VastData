# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data API tokens."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_api_token
short_description: Manage VAST Data API tokens
description:
    - Create, update, and delete API tokens on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the API token.
        type: str
        required: true
    expiration:
        description:
            - Expiration date/time for the token in ISO 8601 format.
        type: str
        required: false
    token_type:
        description:
            - Type of the API token.
        type: str
        required: false
        choices: [access, refresh]
    state:
        description:
            - The desired state of the API token.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - vastdata.cluster.vast_common
"""

EXAMPLES = r"""
- name: Create an API token
  vastdata.cluster.vast_api_token:
    vms_host: "vms.example.com"
    vms_user: "admin"
    vms_password: "secret"
    name: "automation-token"
    expiration: "2026-12-31T23:59:59Z"
    token_type: "access"
    state: present

- name: Update an API token
  vastdata.cluster.vast_api_token:
    vms_host: "vms.example.com"
    api_token: "my-token"
    name: "automation-token"
    expiration: "2027-12-31T23:59:59Z"
    state: present

- name: Delete an API token
  vastdata.cluster.vast_api_token:
    vms_host: "vms.example.com"
    api_token: "my-token"
    name: "automation-token"
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the API token.
    returned: on success
    type: dict
    sample:
        id: 1
        name: "automation-token"
        expiration: "2026-12-31T23:59:59Z"
        token_type: "access"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource import VastResourceBase


class VastApiToken(VastResourceBase):
    resource_path = "/api/tokens/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "expiration",
            "token_type"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["expiration"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        expiration=dict(type="str", required=False),
        token_type=dict(type="str", required=False, choices=["access", "refresh"]),
        state=dict(type="str", default="present", choices=["present", "absent"]),
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastApiToken(module).run()


if __name__ == "__main__":
    main()
