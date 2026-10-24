# Ansible LAMP Server Role

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An Ansible role for setting up a basic **Linux, Apache, MySQL, and PHP (LAMP)** stack on Ubuntu. It installs the required packages, configures services, and creates two MySQL databases and an application database user.

> **Note:** This is a demonstration role, not a production-hardened deployment. Review the package upgrade and MySQL authentication tasks before running it on an existing server.

## What it does

- Installs Apache, MySQL, PHP, PHP-FPM, and supporting packages.
- Enables Apache's PHP and SSL modules and starts the configured services.
- Configures MySQL root authentication, creates two databases, and manages a database user.
- Deploys and then removes a temporary `phpinfo()` page.

## Requirements

- **Target:** Ubuntu. The role metadata lists Ubuntu 22.04 (Jammy) and 24.04 (Noble).
- **Controller:** Ansible 2.10 or later, as declared in the role metadata, plus the `community.mysql` collection.
- **Access:** Privilege escalation (`become: true`) and access to the required package repositories.
- **PHP packages:** The selected PHP version must be available in the configured APT repositories. The default is PHP 8.3; Ubuntu 22.04 generally requires an additional package source for that version.

Install the MySQL collection on the Ansible controller:

```bash
ansible-galaxy collection install community.mysql
```

## Quick start

Clone the repository into your Ansible project's `roles` directory using the role name expected by the playbook:

```bash
mkdir -p roles
git clone https://github.com/Doron126/Ansible-Galaxy-LAMP-Role.git roles/lamp_server
```

Create a playbook named `site.yml`:

```yaml
---
- name: Configure LAMP hosts
  hosts: lamp
  become: true
  roles:
    - lamp_server
```

Provide an inventory with a `lamp` group. Override the default variables, for example in `group_vars/lamp.yml`:

```yaml
mysql_root_password: "{{ vault_mysql_root_password }}"
db_user: app_user
db_password: "{{ vault_db_password }}"
db_1: app_db
db_2: app_logs
php_version: "8.3"
```

Define the `vault_mysql_root_password` and `vault_db_password` variables in an encrypted Ansible Vault file accessible to the playbook. Then run:

```bash
ansible-playbook -i inventory.ini site.yml --ask-vault-pass
```

## Key variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `mysql_root_password` | Required; no default | MySQL root password. Store it in Ansible Vault. |
| `db_user` | Required; no default | Application database account, limited to local connections and the two configured databases. |
| `db_password` | Required; no default | Application database password. Store it in Ansible Vault. |
| `db_1` / `db_2` | `database1` / `database2` | Databases to create and grant to the application account. |
| `php_version` | `8.3` | PHP package and module version |
| `apache_service` | `apache2` | Apache service name |

Additional package, service, and file-permission settings are available in [`defaults/main.yml`](defaults/main.yml).

## Operational considerations

- The role runs a **distribution package upgrade** (`apt upgrade: dist`), which can change software beyond the LAMP stack.
- MySQL remains managed by its normal Ubuntu service. The role configures it through the local Unix socket with `community.mysql` modules; it does not disable grant checks or stop the server.
- Supply all three MySQL credentials explicitly. The application account is restricted to `localhost` and the two configured databases.
- The included [local test playbook](tests/test.yml) targets `localhost` with privilege escalation and changes the host. Use it only in a disposable Ubuntu test environment. The focused Python tests can be run safely with `python3 -m unittest discover -s tests`.
- Keep passwords out of version control.

## License

Released under the [MIT License](LICENSE).

**Maintainer:** [Doron Shamo](https://github.com/Doron126).
