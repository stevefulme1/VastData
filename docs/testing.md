# Testing Guide — vastdata.cluster

This document covers how to run tests for the `vastdata.cluster` Ansible collection.

## Prerequisites

```bash
pip install ansible-core>=2.16 vastpy vastdb pytest pytest-cov molecule
```

## Unit Tests

Unit tests live in `tests/unit/` and use pytest with mocked VAST API clients.

### Run all unit tests

```bash
pytest tests/unit/ -v --tb=short
```

### Run a single test file

```bash
pytest tests/unit/plugins/modules/test_vast_vip_pool.py -v
```

### Run with coverage

```bash
pytest tests/unit/ --cov=plugins --cov-report=term-missing
```

## Sanity Tests

Ansible sanity tests check for coding standards, documentation, and import issues.

```bash
ansible-test sanity --python 3.12 --color yes -v
```

## Integration Tests

Integration tests require a live VAST cluster. They are located in
`tests/integration/targets/`.

### Configuration

1. Copy the credential template:

```bash
cp tests/integration/cloud-config-vast.ini.template tests/integration/cloud-config-vast.ini
```

2. Fill in your VAST cluster credentials, or export environment variables:

```bash
export VAST_VMS_HOST="vms.example.com"
export VAST_VMS_USER="admin"
export VAST_VMS_PASSWORD="secret"
```

### Run integration targets

```bash
ansible-test integration vast_tenant --python 3.12 -v
ansible-test integration vast_view --python 3.12 -v
ansible-test integration vast_vip_pool --python 3.12 -v
ansible-test integration vast_protection_policy --python 3.12 -v
```

## Molecule Tests

Molecule scenarios are in `extensions/molecule/`. They use the delegated driver
(no VM provisioning) and expect a pre-existing VAST cluster.

### Run the default scenario

```bash
export VAST_VMS_HOST="vms.example.com"
export VAST_VMS_USER="admin"
export VAST_VMS_PASSWORD="secret"

molecule test
```

### Run individual phases

```bash
molecule converge   # run the playbook
molecule verify     # run verification checks
molecule destroy    # clean up (no-op for delegated)
```

## CI Workflows

The GitHub Actions CI workflow (`.github/workflows/ci.yml`) runs automatically
on pull requests and pushes to `main`:

| Job | Trigger | Description |
|-----|---------|-------------|
| `ansible-lint` | Every PR / push | yamllint, flake8, ansible-lint |
| `sanity` | Every PR / push | ansible-test sanity (matrix) |
| `unit` | Every PR / push | pytest unit tests (matrix) |
| `dependency-audit` | Every PR / push | pip-audit for vulnerable deps |
| `integration-mock` | Every PR / push | Integration targets with mocked API |
| `integration-cloud` | Manual dispatch only | Live VAST cluster integration |

### Running cloud integration manually

1. Configure repository secrets: `VAST_VMS_HOST`, `VAST_VMS_USER`, `VAST_VMS_PASSWORD`
2. Go to Actions > CI > Run workflow
3. Select the branch and trigger the run
