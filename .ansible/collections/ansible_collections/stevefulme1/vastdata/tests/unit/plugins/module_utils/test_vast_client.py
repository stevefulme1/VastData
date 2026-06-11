"""Unit tests for stevefulme1.vastdata.plugins.module_utils.vast_client."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from unittest.mock import MagicMock, patch


CLIENT_PATH = "ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_client"


class TestGetVastClient:
    """Test VAST client creation for different auth methods."""

    @patch(f"{CLIENT_PATH}.VASTClient")
    @patch(f"{CLIENT_PATH}.HAS_VASTPY", True)
    def test_api_token_auth(self, mock_client_class):
        """API token auth creates client with token."""
        mock_instance = MagicMock()
        mock_client_class.return_value = mock_instance

        module = MagicMock()
        module.params = {
            "vms_host": "vms.example.com",
            "vms_port": 443,
            "vms_user": None,
            "vms_password": None,
            "api_token": "my-secret-token",
            "validate_certs": True,
        }

        from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_client import get_vast_client
        client = get_vast_client(module)

        mock_client_class.assert_called_once_with(
            host="vms.example.com",
            port=443,
            api_token="my-secret-token",
            verify_ssl=True,
        )
        assert client == mock_instance

    @patch(f"{CLIENT_PATH}.VASTClient")
    @patch(f"{CLIENT_PATH}.HAS_VASTPY", True)
    def test_username_password_auth(self, mock_client_class):
        """Username/password auth creates client with credentials."""
        mock_instance = MagicMock()
        mock_client_class.return_value = mock_instance

        module = MagicMock()
        module.params = {
            "vms_host": "vms.example.com",
            "vms_port": 443,
            "vms_user": "admin",
            "vms_password": "secret",
            "api_token": None,
            "validate_certs": False,
        }

        from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_client import get_vast_client
        client = get_vast_client(module)

        mock_client_class.assert_called_once_with(
            host="vms.example.com",
            port=443,
            username="admin",
            password="secret",
            verify_ssl=False,
        )
        assert client == mock_instance

    @patch(f"{CLIENT_PATH}.HAS_VASTPY", False)
    def test_missing_sdk_fails(self):
        """Missing vastpy SDK causes fail_json."""
        module = MagicMock()
        module.params = {
            "vms_host": "vms.example.com",
            "vms_port": 443,
            "vms_user": None,
            "vms_password": None,
            "api_token": None,
            "validate_certs": True,
        }

        from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_client import get_vast_client
        get_vast_client(module)

        module.fail_json.assert_called_once()
        assert "vastpy" in module.fail_json.call_args[1]["msg"].lower()

    @patch(f"{CLIENT_PATH}.VASTClient")
    @patch(f"{CLIENT_PATH}.HAS_VASTPY", True)
    def test_no_credentials_fails(self, mock_client_class):
        """No token or username/password causes fail_json."""
        module = MagicMock()
        module.params = {
            "vms_host": "vms.example.com",
            "vms_port": 443,
            "vms_user": None,
            "vms_password": None,
            "api_token": None,
            "validate_certs": True,
        }

        from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_client import get_vast_client
        get_vast_client(module)

        module.fail_json.assert_called_once()
        assert "api_token" in module.fail_json.call_args[1]["msg"]

    @patch(f"{CLIENT_PATH}.VASTClient")
    @patch(f"{CLIENT_PATH}.HAS_VASTPY", True)
    def test_connection_failure(self, mock_client_class):
        """Connection failure causes fail_json."""
        mock_client_class.side_effect = ConnectionError("refused")

        module = MagicMock()
        module.params = {
            "vms_host": "bad-host",
            "vms_port": 443,
            "vms_user": "admin",
            "vms_password": "secret",
            "api_token": None,
            "validate_certs": True,
        }

        from ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_client import get_vast_client
        get_vast_client(module)

        module.fail_json.assert_called_once()
        assert "bad-host" in module.fail_json.call_args[1]["msg"]
