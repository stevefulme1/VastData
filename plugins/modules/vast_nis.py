# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data NIS providers."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_nis
short_description: Manage VAST Data NIS providers
description:
    - Create, update, and delete NIS providers on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the NIS provider.
        type: str
        required: true
    domain:
        description:
            - NIS domain name.
            - Required when I(state=present).
        type: str
    servers:
        description:
            - List of NIS server addresses.
            - Required when I(state=present).
        type: list
        elements: str
    state:
        description:
            - The desired state of the NIS provider.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Create NIS provider
  stevefulme1.vastdata.vast_nis:
    name: corporate_nis
    domain: example.com
    servers:
      - nis1.example.com
      - nis2.example.com
    state: present
    vms_host: vast.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Update NIS provider
  stevefulme1.vastdata.vast_nis:
    name: corporate_nis
    domain: example.com
    servers:
      - nis1.example.com
      - nis2.example.com
      - nis3.example.com
    state: present
    vms_host: vast.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"

- name: Delete NIS provider
  stevefulme1.vastdata.vast_nis:
    name: corporate_nis
    state: absent
    vms_host: vast.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
"""

RETURN = r"""
resource:
    description: Details of the NIS provider.
    returned: on success
    type: dict
    sample:
        id: 1
        name: corporate_nis
        domain: example.com
        servers:
          - nis1.example.com
          - nis2.example.com
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource import VastResourceBase


class VastNis(VastResourceBase):
    resource_path = "/api/nis/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "domain",
            "servers"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["domain", "servers"]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        domain=dict(type="str"),
        servers=dict(type="list", elements="str"),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ("state", "present", ["domain", "servers"]),
        ],
    )
    VastNis(module).run()


if __name__ == "__main__":
    main()
