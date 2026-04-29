# Contributing to vastdata.cluster

Thank you for your interest in contributing to the VAST Data Ansible
collection. This document explains the process for contributing code,
reporting issues, and running tests.

## Getting Started

### Prerequisites

| Requirement | Version |
|---|---|
| Python | >= 3.12 |
| ansible-core | >= 2.16 |
| VAST Python SDK (`vastpy`) | >= 0.3.22 |
| VAST Database SDK (`vastdb`) | >= 2.0.14 |
| pytest | latest |

### Environment Setup

1. Fork the repository and clone your fork:

   ```bash
   mkdir -p ansible_collections/vastdata
   git clone https://github.com/<your-fork>/VastData.git ansible_collections/vastdata/cluster
   cd ansible_collections/vastdata/cluster
   ```

2. Create a Python virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install ansible-core>=2.16 vastpy vastdb pytest pytest-cov yamllint flake8 ansible-lint
   ```

3. Configure VAST VMS credentials for integration tests.

## Running Tests

### Linting

```bash
yamllint -c .yamllint .
flake8 plugins/ --max-line-length=120 --ignore=E402,W503
ansible-lint --strict
```

### Sanity Tests

```bash
ansible-test sanity --python 3.12 -v
```

### Unit Tests

```bash
pytest tests/unit/ -v --tb=short
```

### Using Nox

```bash
pip install nox
nox -s lint
nox -s unit
nox -s sanity
```

## Module Development Guidelines

### File Structure

Every module file must include:

1. Copyright header (GPLv3)
2. `DOCUMENTATION` block with `extends_documentation_fragment: vastdata.cluster.vast_common`
3. `EXAMPLES` block with at least 3 examples (create, update, delete)
4. `RETURN` block
5. A class extending `VastResourceBase`
6. A `main()` function

### Naming Conventions

- Module files: `vast_<resource>.py`
- Class names: `Vast<Resource>` (CamelCase)
- API paths: `/api/<resource>/`
- FQCN in examples: `vastdata.cluster.vast_<resource>`

### Idempotency

All modules must be idempotent. The base class `VastResourceBase.run()`
handles the standard create/update/delete lifecycle. Override
`_updatable_attributes()` to specify which fields trigger an update.

### Check Mode

All modules must support `check_mode`. The base class handles this
automatically when `supports_check_mode=True` is set in `AnsibleModule`.

### Sensitive Parameters

Mark passwords, tokens, and secrets with `no_log=True` in the argument
spec. Never log sensitive values.

## Pull Request Process

1. Ensure all lint, sanity, and unit tests pass
2. Update `CHANGELOG.md` if adding new modules or features
3. Follow the [Review Checklist](REVIEW_CHECKLIST.md)
4. Request review from a maintainer

## Reporting Issues

Open a GitHub issue with:

- VAST Data cluster version
- Ansible version
- Module name and parameters (redact credentials)
- Expected vs actual behavior
- Error output
