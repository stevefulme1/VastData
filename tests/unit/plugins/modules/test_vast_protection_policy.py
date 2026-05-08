"""Unit tests for vastdata.cluster.vast_protection_policy module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from unittest.mock import MagicMock, patch


CLIENT_PATH = "ansible_collections.vastdata.cluster.plugins.module_utils.vast_resource"


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

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_create_protection_policy(self, mock_get_client):
        """Creating a protection policy calls POST /api/protectionpolicies/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = []
        mock_client.post.return_value = {
            "id": 3,
            "name": "daily-backup",
            "prefix": "bkp",
            "clone_type": "LOCAL",
            "indestructible": False,
            "frames": [{"every": "1D", "start_at": "00:00"}],
        }

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "daily-backup",
            "prefix": "bkp",
            "clone_type": "LOCAL",
            "frames": [{"every": "1D", "start_at": "00:00"}],
            "indestructible": False,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.vastdata.cluster.plugins.modules.vast_protection_policy import VastProtectionPolicy
        policy = VastProtectionPolicy(module)
        result = policy.create_resource()

        mock_client.post.assert_called_once()
        call_data = mock_client.post.call_args[1]["data"]
        assert call_data["name"] == "daily-backup"
        assert call_data["prefix"] == "bkp"
        assert call_data["clone_type"] == "LOCAL"
        assert len(call_data["frames"]) == 1
        assert result["id"] == 3


class TestVastProtectionPolicyDelete:
    """Test protection policy deletion."""

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_delete_protection_policy(self, mock_get_client):
        """Deleting a protection policy calls DELETE /api/protectionpolicies/{id}/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {**_base_args(), "name": "old-policy", "state": "absent"}
        module.check_mode = False

        from ansible_collections.vastdata.cluster.plugins.modules.vast_protection_policy import VastProtectionPolicy
        policy = VastProtectionPolicy(module)
        policy.delete_resource({"id": 15, "name": "old-policy"})

        mock_client.delete.assert_called_once_with("/api/protectionpolicies/15/")


class TestVastProtectionPolicyIdempotent:
    """Test idempotent behavior."""

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_no_update_when_matching(self, mock_get_client):
        """No update triggered when params are None."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "daily-backup",
            "prefix": None,
            "clone_type": None,
            "frames": None,
            "indestructible": None,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.vastdata.cluster.plugins.modules.vast_protection_policy import VastProtectionPolicy
        policy = VastProtectionPolicy(module)

        existing = {"id": 3, "name": "daily-backup", "prefix": "bkp", "clone_type": "LOCAL"}
        assert not policy.needs_update(existing)

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_update_needed(self, mock_get_client):
        """When clone_type differs, needs_update returns True."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "daily-backup",
            "prefix": None,
            "clone_type": "NATIVE_REPLICATION",
            "frames": None,
            "indestructible": None,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.vastdata.cluster.plugins.modules.vast_protection_policy import VastProtectionPolicy
        policy = VastProtectionPolicy(module)

        existing = {"id": 3, "name": "daily-backup", "clone_type": "LOCAL"}
        assert policy.needs_update(existing)


class TestVastProtectionPolicyUpdate:
    """Test protection policy update."""

    @patch(f"{CLIENT_PATH}.get_vast_client")
    def test_update_protection_policy(self, mock_get_client):
        """Updating a protection policy calls PATCH /api/protectionpolicies/{id}/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.patch.return_value = {
            "id": 3,
            "name": "daily-backup",
            "indestructible": True,
        }

        module = MagicMock()
        module.params = {
            **_base_args(),
            "name": "daily-backup",
            "prefix": None,
            "clone_type": None,
            "frames": None,
            "indestructible": True,
            "state": "present",
        }
        module.check_mode = False

        from ansible_collections.vastdata.cluster.plugins.modules.vast_protection_policy import VastProtectionPolicy
        policy = VastProtectionPolicy(module)
        result = policy.update_resource({"id": 3, "name": "daily-backup"})

        mock_client.patch.assert_called_once()
        call_data = mock_client.patch.call_args[1]["data"]
        assert call_data["indestructible"] is True
        assert result["id"] == 3
