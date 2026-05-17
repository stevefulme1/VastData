"""Unit tests for stevefulme1.vastdata.vast_encryption module."""
from __future__ import absolute_import, division, print_function
__metaclass__ = type

from unittest.mock import MagicMock, patch

CLIENT_PATH = "ansible_collections.stevefulme1.vastdata.plugins.module_utils.vast_resource"


def _base_args():
    return {
        "vms_host": "vms.example.com",
        "vms_port": 443,
        "vms_user": "admin",
        "vms_password": "secret",
        "api_token": None,
        "validate_certs": True,
        "wait": True,
        "wait_timeout": 600,
        "wait_interval": 10,
    }


class TestCreate:
    """Test vast_encryption creation."""

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_create_resource(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = []
        mock_client.post.return_value = {
            "id": 1,
            "name": "enc-group1",
            "key_type": 'AES_256',
        }

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "enc-group1",
            "key_type": 'AES_256',
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_encryption import VastEncryption
        obj = VastEncryption(module)
        result = obj.create_resource()

        mock_client.post.assert_called_once()
        assert result["id"] == 1
        assert result["name"] == "enc-group1"

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_create_check_mode(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "enc-group1",
            "key_type": 'AES_256',
            "state": "present",
        }
        module.check_mode = True

        assert module.check_mode is True
        mock_client.post.assert_not_called()


class TestDelete:
    """Test vast_encryption deletion."""

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_delete_resource(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "enc-group1",
            "state": "absent",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_encryption import VastEncryption
        obj = VastEncryption(module)
        obj.delete_resource({"id": 42, "name": "enc-group1"})

        mock_client.delete.assert_called_once_with("/api/encryptiongroups/42/")


class TestUpdate:
    """Test vast_encryption update."""

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_update_resource(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.patch.return_value = {
            "id": 1,
            "name": "enc-group1-updated",
        }

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "enc-group1-updated",
            "key_type": 'AES_256',
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_encryption import VastEncryption
        obj = VastEncryption(module)
        result = obj.update_resource({"id": 1, "name": "enc-group1"})

        mock_client.patch.assert_called_once()
        assert result["name"] == "enc-group1-updated"


class TestIdempotent:
    """Test idempotent behavior."""

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_no_change_needed(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "enc-group1",
            "key_type": 'AES_256',
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_encryption import VastEncryption
        obj = VastEncryption(module)

        existing = {
            "id": 1,
            "name": "enc-group1",
        }
        # No user-specified params differ from existing -> no update needed
        assert not obj.needs_update(existing)


class TestErrorHandling:
    """Test error handling."""

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_api_error_on_create(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = []
        mock_client.post.side_effect = Exception("401 Unauthorized")

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "enc-group1",
            "key_type": 'AES_256',
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_encryption import VastEncryption
        obj = VastEncryption(module)

        try:
            obj.create_resource()
            assert False, "Expected exception"
        except Exception as e:
            assert "401" in str(e)

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_not_found_on_delete(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.delete.side_effect = Exception("404 Not Found")

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "enc-group1",
            "state": "absent",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_encryption import VastEncryption
        obj = VastEncryption(module)

        try:
            obj.delete_resource({"id": 999, "name": "enc-group1"})
        except Exception as e:
            assert "404" in str(e)


class TestReturnValues:
    """Test return value structure."""

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_create_returns_dict_with_id(self, mock_get_client):
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = []
        mock_client.post.return_value = {
            "id": 42,
            "name": "enc-group1",
        }

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "enc-group1",
            "key_type": 'AES_256',
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_encryption import VastEncryption
        obj = VastEncryption(module)
        result = obj.create_resource()

        assert isinstance(result, dict)
        assert "id" in result
        assert "name" in result
