"""Unit tests for stevefulme1.vastdata.vast_protection_policy module."""

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


class TestVastProtectionPolicyCreate:
    """Test protection policy creation."""

    @patch(CLIENT_PATH + ".get_vast_client")
    def test_create_protection_policy(self, mock_get_client):
        """Creating a protection policy calls POST /api/protectionpolicies/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = []
        mock_client.post.return_value = {
            "id": 42,
            "name": "daily_protection",
            "prefix": "daily",
            "clone_type": "LOCAL",
            "frames": [
                {"every": 86400, "start_at": "00:00", "keep_local": 7, "keep_remote": 0}
            ],
            "indestructible": False,
        }

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "daily_protection",
            "prefix": "daily",
            "clone_type": "LOCAL",
            "frames": [
                {"every": 86400, "start_at": "00:00", "keep_local": 7, "keep_remote": 0}
            ],
            "indestructible": False,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_protection_policy import VastProtectionPolicy
        policy = VastProtectionPolicy(module)
        result = policy.create_resource()

        mock_client.post.assert_called_once()
        call_data = mock_client.post.call_args[1]["data"]
        assert call_data["name"] == "daily_protection"
        assert call_data["prefix"] == "daily"
        assert call_data["clone_type"] == "LOCAL"
        assert result["id"] == 42


class TestVastProtectionPolicyDelete:
    """Test protection policy deletion."""

    @patch(CLIENT_PATH + ".get_vast_client")
    def test_delete_protection_policy(self, mock_get_client):
        """Deleting a protection policy calls DELETE /api/protectionpolicies/{id}/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "daily_protection",
            "state": "absent",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_protection_policy import VastProtectionPolicy
        policy = VastProtectionPolicy(module)
        policy.delete_resource({"id": 42, "name": "daily_protection"})

        mock_client.delete.assert_called_once_with("/api/protectionpolicies/42/")


class TestVastProtectionPolicyIdempotent:
    """Test idempotent behavior."""

    @patch(CLIENT_PATH + ".get_vast_client")
    def test_no_change_needed(self, mock_get_client):
        """When policy exists and matches, needs_update returns False."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "daily_protection",
            "prefix": None,
            "clone_type": None,
            "frames": None,
            "indestructible": None,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_protection_policy import VastProtectionPolicy
        policy = VastProtectionPolicy(module)

        existing = {
            "id": 42,
            "name": "daily_protection",
            "prefix": "daily",
            "clone_type": "LOCAL",
            "indestructible": False,
        }
        assert not policy.needs_update(existing)

    @patch(CLIENT_PATH + ".get_vast_client")
    def test_update_needed(self, mock_get_client):
        """When indestructible differs, needs_update returns True."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "daily_protection",
            "prefix": None,
            "clone_type": None,
            "frames": None,
            "indestructible": True,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_protection_policy import VastProtectionPolicy
        policy = VastProtectionPolicy(module)

        existing = {
            "id": 42,
            "name": "daily_protection",
            "indestructible": False,
        }
        assert policy.needs_update(existing)

    @patch(CLIENT_PATH + ".get_vast_client")
    def test_update_resource(self, mock_get_client):
        """Updating a policy calls PATCH /api/protectionpolicies/{id}/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.patch.return_value = {
            "id": 42,
            "name": "daily_protection",
            "indestructible": True,
        }

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "daily_protection",
            "prefix": None,
            "clone_type": None,
            "frames": None,
            "indestructible": True,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_protection_policy import VastProtectionPolicy
        policy = VastProtectionPolicy(module)
        result = policy.update_resource({"id": 42, "name": "daily_protection"})

        mock_client.patch.assert_called_once()
        assert result["indestructible"] is True
