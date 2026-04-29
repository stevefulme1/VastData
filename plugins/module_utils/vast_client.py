"""VAST Data client wrapper using the vastpy SDK."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

try:
    from vastpy import VASTClient
    HAS_VASTPY = True
except ImportError:
    HAS_VASTPY = False


def get_vast_client(module):
    """Create a VASTClient from module params or environment."""
    if not HAS_VASTPY:
        module.fail_json(msg="The 'vastpy' Python SDK is required. Install with: pip install vastpy")
        return None

    host = module.params["vms_host"]
    port = module.params.get("vms_port", 443)
    username = module.params.get("vms_user")
    password = module.params.get("vms_password")
    api_token = module.params.get("api_token")
    verify_ssl = module.params.get("validate_certs", True)

    try:
        if api_token:
            client = VASTClient(
                host=host,
                port=port,
                api_token=api_token,
                verify_ssl=verify_ssl,
            )
        elif username and password:
            client = VASTClient(
                host=host,
                port=port,
                username=username,
                password=password,
                verify_ssl=verify_ssl,
            )
        else:
            module.fail_json(
                msg="Either 'api_token' or both 'vms_user' and 'vms_password' are required."
            )
            return None
    except Exception as e:
        module.fail_json(msg=f"Failed to connect to VAST VMS at {host}:{port}: {e}")
        return None

    return client
