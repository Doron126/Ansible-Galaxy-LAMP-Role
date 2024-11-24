<<<<<<< HEAD
LAMP Server Role
=========

This Ansible role sets up a LAMP server on Ubuntu systems.

Requirements
------------

- Ansile 2.10
- Ubuntu 22.04

Role Variables
--------------

# MySQL configuration
mysql_root_password: root_password_default
db_user: default_user
db_password: default_password
db_1: database1
db_2: database2

# PHP version
php_version: 8.3

# Apache configuration
apache_service: apache2
php_fpm_service: "php{{ php_version }}-fpm"
php_packages:
  - "php{{ php_version }}"
  - "php{{ php_version }}-fpm"
  - "php{{ php_version }}-cli"
  - "php{{ php_version }}-mysql"
  - "php{{ php_version }}-curl"
libapache_mod_php: "libapache2-mod-php{{ php_version }}"

# Other packages to install
common_packages:
  - update-notifier-common
  - mysql-server
  - python3-pymysql
  - "{{ libapache_mod_php }}"

# Service configurations
services_to_enable:
  - "{{ php_fpm_service }}"
  - "{{ apache_service }}"

# File permissions
php_info_file_owner: www-data
php_info_file_group: www-data
php_info_file_mode: "0644"
mysql_socket_directory_mode: "0755"

# Environment variables
debian_frontend: noninteractive



Dependencies
------------

None.

Example Playbook
----------------


    - hosts: servers
      become: true
      roles:
         - lamp_server

License
-------

MIT

Author Information
------------------

Doron Shamo, Doron126 on Ansible Galaxy and GitHub.
