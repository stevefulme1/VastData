# vast_capacity_expansion

Ansible role for VAST Data cluster capacity expansion operations.

## Requirements

- VAST Data cluster access credentials
- `stevefulme1.vastdata` collection installed

## Role Variables

See `defaults/main.yml` for available variables.

## Example Playbook

```yaml
- hosts: localhost
  roles:
    - stevefulme1.vastdata.vast_capacity_expansion
```

## License

GPL-3.0-or-later
