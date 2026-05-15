# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for querying VAST Data active alerts."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: vast_alert_info
short_description: Query VAST Data active alerts
description:
    - Retrieve active alerts from a VAST Data cluster.
    - Optionally filter alerts by severity or state.
    - Returns a list of alerts with timestamp, object type, description,
      and severity.
    - This is a read-only info module; it does not modify any resources.
version_added: "1.0.0"
author: VAST Data (@vast-data)
options:
    severity:
        description:
            - Filter alerts by severity level.
        type: str
    alert_state:
        description:
            - Filter alerts by state.
        type: str
        choices: [OPEN, ACKNOWLEDGED, CLOSED]
extends_documentation_fragment:
    - stevefulme1.vastdata.vast_common
"""

EXAMPLES = r"""
- name: Get all active alerts
  stevefulme1.vastdata.vast_alert_info:
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: alert_info

- name: Get only critical alerts
  stevefulme1.vastdata.vast_alert_info:
    severity: CRITICAL
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: critical_alerts

- name: Get open alerts
  stevefulme1.vastdata.vast_alert_info:
    alert_state: OPEN
    vms_host: vast-cluster-01.example.com
    vms_user: admin
    vms_password: "{{ vault_vms_password }}"
  register: open_alerts
"""

RETURN = r"""
alerts:
    description: List of alert objects returned by the API.
    returned: on success
    type: list
    elements: dict
    sample: [
        {
            "id": 101,
            "timestamp": "2025-01-15T08:30:00Z",
            "object_type": "CNode",
            "description": "CNode-2 memory utilization exceeded threshold",
            "severity": "WARNING",
            "state": "OPEN"
        }
    ]
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_common import VAST_COMMON_ARGS
from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_client import get_vast_client


def main():
    module_args = dict(
        severity=dict(type="str"),
        alert_state=dict(type="str", choices=["OPEN", "ACKNOWLEDGED", "CLOSED"]),
    )
    module_args.update(VAST_COMMON_ARGS)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    client = get_vast_client(module)

    try:
        alerts = client.get("/api/alerts/")
        if not isinstance(alerts, list):
            alerts = [alerts] if alerts else []
    except Exception as e:
        module.fail_json(msg=f"Failed to query alerts: {e}")
        return

    severity = module.params.get("severity")
    if severity:
        alerts = [a for a in alerts if a.get("severity") == severity]

    alert_state = module.params.get("alert_state")
    if alert_state:
        alerts = [a for a in alerts if a.get("state") == alert_state]

    module.exit_json(changed=False, alerts=alerts)


if __name__ == "__main__":
    main()
