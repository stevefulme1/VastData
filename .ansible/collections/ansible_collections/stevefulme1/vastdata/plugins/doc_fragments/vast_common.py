# -*- coding: utf-8 -*-
# Copyright (c) 2025, VAST Data
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


class ModuleDocFragment(object):
    """Common documentation fragment for VAST Data modules."""

    DOCUMENTATION = r"""
options:
  vms_host:
    description:
      - The hostname or IP address of the VAST Management Server (VMS).
    type: str
    required: true
  vms_port:
    description:
      - The HTTPS port of the VMS REST API.
    type: int
    default: 443
  vms_user:
    description:
      - The username for VMS authentication.
      - Required if I(api_token) is not provided.
    type: str
  vms_password:
    description:
      - The password for VMS authentication.
      - Required if I(api_token) is not provided.
    type: str
  api_token:
    description:
      - An API token for VMS authentication.
      - Takes precedence over username/password if both are provided.
    type: str
  validate_certs:
    description:
      - Whether to validate SSL certificates when connecting to VMS.
    type: bool
    default: true
  wait:
    description:
      - Whether to wait for the resource to reach the desired state.
    type: bool
    default: true
  wait_timeout:
    description:
      - Maximum time in seconds to wait for resource state changes.
    type: int
    default: 600
  wait_interval:
    description:
      - Time in seconds between polling attempts when waiting.
    type: int
    default: 10
"""
