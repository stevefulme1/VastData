"""Unit tests for stevefulme1.vastdata.vast_tenant module."""

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


def _merge_params(extra):
    """Merge base args with extra params (Python 2.7 compatible)."""
    params = _base_args()
    params.update(extra)
    return params


class TestVastTenantCreate:
    """Test tenant creation."""

    @patch(CLIENT_PATH + ".get_vast_client")
    def test_create_tenant(self, mock_get_client):
        """Creating a tenant calls POST /api/tenants/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get.return_value = []
        mock_client.post.return_value = {
            "id": 5,
            "name": "team-alpha",
            "posix_primary_provider": "LDAP",
        }

        module = MagicMock()
        module.params = _merge_params({
            "name": "team-alpha",
            "smb_privileged_user_name": None,
            "smb_administrator_name": None,
            "default_others_share_level": None,
            "trash_gid": None,
            "client_ip_ranges": None,
            "posix_primary_provider": "LDAP",
            "state": "present",
        })
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_tenant import VastTenant
        tenant = VastTenant(module)
        result = tenant.create_resource()

        mock_client.post.assert_called_once()
        call_data = mock_client.post.call_args[1]["data"]
        assert call_data["name"] == "team-alpha"
        assert result["id"] == 5


class TestVastTenantDelete:
    """Test tenant deletion."""

    @patch(CLIENT_PATH + ".get_vast_client")
    def test_delete_tenant(self, mock_get_client):
        """Deleting a tenant calls DELETE /api/tenants/{id}/."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = _merge_params({"name": "old-tenant", "state": "absent"})
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_tenant import VastTenant
        tenant = VastTenant(module)
        tenant.delete_resource({"id": 3, "name": "old-tenant"})

        mock_client.delete.assert_called_once_with("/api/tenants/3/")


class TestVastTenantIdempotent:
    """Test idempotent behavior."""

    @patch(CLIENT_PATH + ".get_vast_client")
    def test_no_update_when_matching(self, mock_get_client):
        """No update triggered when params are None."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        module = MagicMock()
        module.params = _merge_params({
            "name": "team-alpha",
            "smb_privileged_user_name": None,
            "smb_administrator_name": None,
            "default_others_share_level": None,
            "trash_gid": None,
            "client_ip_ranges": None,
            "posix_primary_provider": None,
            "state": "present",
        })
        module.check_mode = False

        from ansible_collections.stevefulme1.vastdata.plugins.modules.vast_tenant import VastTenant
        tenant = VastTenant(module)

        existing = {"id": 5, "name": "team-alpha", "posix_primary_provider": "LDAP"}
        assert not tenant.needs_update(existing)
