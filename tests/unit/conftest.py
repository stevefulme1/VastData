"""Shared pytest fixtures for VAST Data collection unit tests."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
import sys
import types
from unittest.mock import MagicMock

import pytest

# ---------------------------------------------------------------------------
# 1.  Provide a mock ``vastpy`` SDK if the real one is not installed.
# ---------------------------------------------------------------------------
try:
    import vastpy as _real_vastpy  # noqa: F401
except ImportError:
    _vastpy = types.ModuleType("vastpy")
    _vastpy.__path__ = []
    _vastpy.__package__ = "vastpy"
    _vastpy.VASTClient = MagicMock

    sys.modules["vastpy"] = _vastpy


# ---------------------------------------------------------------------------
# 2.  Set up the ansible_collections.vastdata.cluster namespace package so
#     that collection imports work from a standalone checkout.
# ---------------------------------------------------------------------------
_collection_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

_namespace_root = os.path.abspath(os.path.join(_collection_root, os.pardir, os.pardir))
if os.path.isdir(os.path.join(_namespace_root, "ansible_collections")) and _namespace_root not in sys.path:
    sys.path.insert(0, _namespace_root)

if "ansible_collections.vastdata.cluster" not in sys.modules:
    for _pkg_name in ("ansible_collections", "ansible_collections.vastdata"):
        if _pkg_name not in sys.modules:
            _pkg = types.ModuleType(_pkg_name)
            _pkg.__path__ = []
            _pkg.__package__ = _pkg_name
            sys.modules[_pkg_name] = _pkg

    _cluster_mod = types.ModuleType("ansible_collections.vastdata.cluster")
    _cluster_mod.__path__ = [_collection_root]
    _cluster_mod.__package__ = "ansible_collections.vastdata.cluster"
    sys.modules["ansible_collections.vastdata.cluster"] = _cluster_mod

    sys.modules["ansible_collections"].vastdata = sys.modules["ansible_collections.vastdata"]
    sys.modules["ansible_collections.vastdata"].cluster = _cluster_mod


@pytest.fixture
def module_args():
    """Return a base dict of VAST common module arguments."""
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
        "state": "present",
    }


@pytest.fixture
def mock_vast_client():
    """Factory fixture that returns a MagicMock configured as a VAST client."""

    def _factory(client_name: str = "VASTClient") -> MagicMock:
        client = MagicMock(name=client_name)
        return client

    return _factory
