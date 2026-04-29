# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data Native Replication Peers."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_replication_peer
short_description: Manage VAST Data native replication peers
description:
    - Create, update, and delete native replication peers on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - Name of the replication peer.
        type: str
        required: true
    remote_vms_host:
        description:
            - Hostname or IP address of the remote VMS.
        type: str
        required: true
    remote_vms_port:
        description:
            - Port number of the remote VMS.
        type: int
        default: 443
    remote_pool_id:
        description:
            - ID of the remote pool.
        type: int
    remote_credentials:
        description:
            - Credentials for authenticating to the remote cluster.
        type: dict
        suboptions:
            username:
                description:
                    - Username for remote authentication.
                type: str
            password:
                description:
                    - Password for remote authentication.
                type: str
                no_log: true
    secure:
        description:
            - Whether to use secure (HTTPS) connection.
        type: bool
        default: true
    state:
        description:
            - The desired state of the replication peer.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - vastdata.cluster.vast_common
"""

EXAMPLES = r"""
- name: Create a native replication peer
  vastdata.cluster.vast_replication_peer:
    name: dr_cluster
    remote_vms_host: dr-vast.example.com
    remote_vms_port: 443
    remote_pool_id: 1
    remote_credentials:
      username: repl_user
      password: secret_password
    secure: true
    state: present

- name: Update replication peer configuration
  vastdata.cluster.vast_replication_peer:
    name: dr_cluster
    remote_vms_host: dr-vast.example.com
    remote_pool_id: 2
    state: present

- name: Delete a replication peer
  vastdata.cluster.vast_replication_peer:
    name: dr_cluster
    remote_vms_host: dr-vast.example.com
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the replication peer.
    returned: on success
    type: dict
    sample: {
        "id": 100,
        "name": "dr_cluster",
        "remote_vms_host": "dr-vast.example.com",
        "remote_vms_port": 443,
        "remote_pool_id": 1,
        "secure": true
    }
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource import VastResourceBase

class VastReplicationPeer(VastResourceBase):
    resource_path = "/api/replicationpeers/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in ["name", "remote_vms_host", "remote_vms_port", "remote_pool_id", "remote_credentials", "secure"] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return ["remote_vms_host", "remote_vms_port", "remote_pool_id", "remote_credentials", "secure"]

def main():
    module_args = dict(
        name=dict(type="str", required=True),
        remote_vms_host=dict(type="str", required=True),
        remote_vms_port=dict(type="int", default=443),
        remote_pool_id=dict(type="int"),
        remote_credentials=dict(
            type="dict",
            options=dict(
                username=dict(type="str"),
                password=dict(type="str", no_log=True)
            )
        ),
        secure=dict(type="bool", default=True),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastReplicationPeer(module).run()

if __name__ == "__main__":
    main()
