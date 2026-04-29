"""Common VAST Data argument specs and constants used across all modules."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type


VAST_COMMON_ARGS = dict(
    vms_host=dict(type="str", required=True),
    vms_port=dict(type="int", default=443),
    vms_user=dict(type="str"),
    vms_password=dict(type="str", no_log=True),
    api_token=dict(type="str", no_log=True),
    validate_certs=dict(type="bool", default=True),
    wait=dict(type="bool", default=True),
    wait_timeout=dict(type="int", default=600),
    wait_interval=dict(type="int", default=10),
)
