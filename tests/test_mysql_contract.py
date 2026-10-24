"""Focused safety checks for the role's MySQL task contract.

These tests inspect the task/default files only; they do not connect to or change
a MySQL server.
"""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MYSQL_TASKS = (ROOT / "tasks" / "mysql.yml").read_text(encoding="utf-8")
DEFAULTS = (ROOT / "defaults" / "main.yml").read_text(encoding="utf-8")


class MySQLTaskContractTests(unittest.TestCase):
    def test_root_setup_uses_mysql_modules_and_local_socket(self):
        self.assertIn("community.mysql.mysql_user:", MYSQL_TASKS)
        self.assertIn("login_unix_socket: /var/run/mysqld/mysqld.sock", MYSQL_TASKS)
        self.assertIn("check_implicit_admin: true", MYSQL_TASKS)
        self.assertIn('login_password: "{{ mysql_root_password }}"', MYSQL_TASKS)
        self.assertIn("no_log: true", MYSQL_TASKS)

    def test_mysql_is_not_started_without_grant_checks_or_killed_globally(self):
        self.assertNotIn("shell:", MYSQL_TASKS)
        self.assertNotIn("command:", MYSQL_TASKS)
        self.assertNotIn("skip-grant-tables", MYSQL_TASKS)
        self.assertNotIn("killall mysqld", MYSQL_TASKS)
        self.assertNotIn("state: stopped", MYSQL_TASKS)

    def test_application_privileges_are_database_scoped(self):
        self.assertIn('priv: "{{ db_1 }}.*:ALL/{{ db_2 }}.*:ALL"', MYSQL_TASKS)
        self.assertIn("host: localhost", MYSQL_TASKS)
        self.assertNotIn("*.*:", MYSQL_TASKS)

    def test_credentials_have_no_weak_defaults_and_are_required(self):
        self.assertIn('mysql_root_password: ""', DEFAULTS)
        self.assertIn('db_password: ""', DEFAULTS)
        self.assertIn('db_user: ""', DEFAULTS)
        self.assertIn("mysql_root_password | string | trim | length > 0", MYSQL_TASKS)
        self.assertIn("db_password | string | trim | length > 0", MYSQL_TASKS)
        self.assertNotIn("root_password_default", DEFAULTS)
        self.assertNotIn("default_password", DEFAULTS)


if __name__ == "__main__":
    unittest.main()
