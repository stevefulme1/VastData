# Pull Request Review Checklist

Use this checklist when reviewing pull requests for the `vastdata.cluster`
Ansible collection.

## General

- [ ] PR title follows conventional commit format (`feat:`, `fix:`, `docs:`, etc.)
- [ ] PR description clearly explains the change and its motivation
- [ ] No unrelated changes included in the PR

## Code Quality

- [ ] flake8 passes (`--max-line-length=120 --ignore=E402,W503`)
- [ ] yamllint passes
- [ ] ansible-lint passes with `--strict`
- [ ] No shebangs in module files
- [ ] Imports are placed after DOCUMENTATION/EXAMPLES/RETURN blocks
- [ ] No hardcoded credentials or secrets
- [ ] Sensitive parameters use `no_log=True` in argument_spec only (not in DOCUMENTATION)

## Module Standards

- [ ] Module has `DOCUMENTATION`, `EXAMPLES`, and `RETURN` blocks
- [ ] DOCUMENTATION includes `extends_documentation_fragment: vastdata.cluster.vast_common`
- [ ] DOCUMENTATION includes `version_added` set to the correct release
- [ ] DOCUMENTATION includes `author: VAST Data (@vast-data)`
- [ ] List-type parameters include `elements:` definition
- [ ] Module supports `check_mode`
- [ ] Module is idempotent (re-running produces no changes)

## Testing

- [ ] Unit tests added or updated for new/modified code
- [ ] All existing tests pass
- [ ] Edge cases considered (resource not found, API errors, etc.)

## Documentation

- [ ] README.md updated if adding new modules
- [ ] CHANGELOG.md updated with new entry
- [ ] Examples use FQCN `vastdata.cluster.vast_*`
