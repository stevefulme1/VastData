# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing VAST Data VMS settings."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_vms
short_description: Manage VAST Data VMS settings
description:
    - Create, update, and delete VMS settings on a VAST Data cluster.
    - Uses the VAST REST API via the vastpy Python SDK.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    name:
        description:
            - The name of the VMS configuration.
        type: str
        required: true
    ntp_servers:
        description:
            - List of NTP server addresses.
        type: list
        elements: str
    smtp_host:
        description:
            - SMTP server hostname.
        type: str
    smtp_port:
        description:
            - SMTP server port.
        type: int
        default: 25
    smtp_from_address:
        description:
            - SMTP from email address.
        type: str
    syslog_host:
        description:
            - Syslog server hostname.
        type: str
    syslog_port:
        description:
            - Syslog server port.
        type: int
        default: 514
    snmp_community:
        description:
            - SNMP community string.
        type: str
        no_log: true
    snmp_trap_targets:
        description:
            - List of SNMP trap target addresses.
        type: list
        elements: str
    state:
        description:
            - The desired state of the VMS settings.
        type: str
        default: present
        choices: [present, absent]
extends_documentation_fragment:
    - vastdata.cluster.vast_common
"""

EXAMPLES = r"""
- name: Configure VMS settings
  vastdata.cluster.vast_vms:
    name: vms_prod
    ntp_servers:
      - ntp1.example.com
      - ntp2.example.com
    smtp_host: smtp.example.com
    smtp_port: 25
    smtp_from_address: alerts@example.com
    syslog_host: syslog.example.com
    syslog_port: 514
    state: present

- name: Update SNMP configuration
  vastdata.cluster.vast_vms:
    name: vms_prod
    snmp_community: public
    snmp_trap_targets:
      - 192.168.1.100
      - 192.168.1.101
    state: present

- name: Delete VMS configuration
  vastdata.cluster.vast_vms:
    name: vms_prod
    state: absent
"""

RETURN = r"""
resource:
    description: Details of the VMS settings.
    returned: on success
    type: dict
    sample:
        id: 1
        name: vms_prod
        ntp_servers:
          - ntp1.example.com
          - ntp2.example.com
        smtp_host: smtp.example.com
        smtp_port: 25
        smtp_from_address: alerts@example.com
        syslog_host: syslog.example.com
        syslog_port: 514
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource import VastResourceBase


class VastVms(VastResourceBase):
    resource_path = "/api/vms/"

    def get_resource(self):
        return self._get_by_name()

    def create_resource(self):
        data = {k: self.module.params[k] for k in [
            "name",
            "ntp_servers",
            "smtp_host",
            "smtp_port",
            "smtp_from_address",
            "syslog_host",
            "syslog_port",
            "snmp_community",
            "snmp_trap_targets"
        ] if self.module.params.get(k) is not None}
        return self._create(data)

    def update_resource(self, resource):
        data = {k: self.module.params[k] for k in self._updatable_attributes() if self.module.params.get(k) is not None}
        return self._update(resource["id"], data)

    def delete_resource(self, resource):
        self._delete(resource["id"])

    def _updatable_attributes(self):
        return [
            "ntp_servers",
            "smtp_host",
            "smtp_port",
            "smtp_from_address",
            "syslog_host",
            "syslog_port",
            "snmp_community",
            "snmp_trap_targets"
        ]


def main():
    module_args = dict(
        name=dict(type="str", required=True),
        ntp_servers=dict(type="list", elements="str"),
        smtp_host=dict(type="str"),
        smtp_port=dict(type="int", default=25),
        smtp_from_address=dict(type="str"),
        syslog_host=dict(type="str"),
        syslog_port=dict(type="int", default=514),
        snmp_community=dict(type="str", no_log=True),
        snmp_trap_targets=dict(type="list", elements="str"),
        state=dict(type="str", default="present", choices=["present", "absent"])
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    VastVms(module).run()


if __name__ == "__main__":
    main()
