# Testing Guide for stevefulme1.vastdata

This document describes how to run the test suites for the VAST Data Ansible
Collection.

## Prerequisites

- Python 3.12+
- `ansible-core >= 2.16`
- `pytest` and `pytest-cov`
- (optional) `molecule` for integration/molecule tests
- (optional) access to a VAST VMS cluster for live integration tests

Install test dependencies:

```bash
pip install ansible-core vastpy vastdb pytest pytest-cov molecule
```

## Unit Tests

Unit tests live under `tests/unit/` and use pytest with mocked VAST API
clients. No live cluster is required.

```bash
# Run all unit tests
pytest tests/unit/ -v

# Run tests for a single module
pytest tests/unit/plugins/modules/test_vast_view.py -v

# Run with coverage
pytest tests/unit/ --cov=plugins --cov-report=term-missing
```

The `conftest.py` fixture automatically provides a mock `vastpy` SDK and wires
up the `ansible_collections.stevefulme1.vastdata` namespace so that module
imports work from a standalone checkout.

## Sanity Tests

Ansible sanity tests validate coding standards, documentation, and import
correctness:

```bash
ansible-test sanity --python 3.12 --color yes -v
```

## Integration Tests

Integration tests live under `tests/integration/targets/` and test full CRUD
lifecycles against a real (or mocked) VAST VMS cluster.

### Configuration

1. Copy the credential template:

   ```bash
   cp tests/integration/cloud-config-vast.ini.template \
      tests/integration/cloud-config-vast.ini
   ```

2. Edit `cloud-config-vast.ini` with your cluster credentials.

3. Export the variables:

   ```bash
   export VAST_VMS_HOST=vms.mylab.example.com
   export VAST_VMS_USER=admin
   export VAST_VMS_PASSWORD='my-password'
   export VAST_VALIDATE_CERTS=false
   ```

### Running Integration Tests

```bash
# Run all integration targets
ansible-test integration --python 3.12 -v

# Run a single target
ansible-test integration vast_tenant --python 3.12 -v
```

Available targets:

| Target                    | Description                          |
|---------------------------|--------------------------------------|
| `vast_tenant`             | Tenant CRUD + idempotency            |
| `vast_view`               | View CRUD with protocol changes      |
| `vast_vip_pool`           | VIP pool lifecycle                   |
| `vast_protection_policy`  | Protection policy with schedule      |

## Molecule Tests

Molecule provides a higher-level test harness using a delegated (local)
driver.

```bash
# Run the default scenario
cd extensions/molecule/default
molecule test

# Or from the collection root
molecule test -s default
```

The default scenario runs converge (tenant + view + VIP pool CRUD) and then
verify (cleanup confirmation).

## CI Pipeline

The GitHub Actions CI workflow (`.github/workflows/ci.yml`) runs:

- **ansible-lint** -- linting and yamllint
- **sanity** -- ansible-test sanity across Python 3.12/3.13 and Ansible
  2.16/2.17/2.18/2.20
- **unit** -- pytest unit tests
- **integration-mock** -- integration targets with mocked credentials
  (manual trigger only)
- **integration-cloud** -- integration targets against a live cluster
  (manual trigger only, requires repository secrets)
- **dependency-audit** -- pip-audit for known vulnerabilities

To trigger integration tests manually, use the GitHub Actions
`workflow_dispatch` trigger and set the `run_integration` input to `true`.
