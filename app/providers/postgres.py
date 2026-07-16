"""
PostgreSQL implementation of BackupProvider.

Relies on the official Postgres client tools being installed and on PATH:
    - psql        (used for a lightweight connection test)
    - pg_dump     (used to create the backup)
    - pg_restore  (used to restore from a backup made with -Fc)

Install on Ubuntu/Debian:   sudo apt install postgresql-client
Install on macOS (brew):    brew install libpq && brew link --force libpq
"""

import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from app.core.config import DBConfig
from app.core.logger import get_logger
from app.providers.base import BackupProvider

logger = get_logger(__name__)


class PostgresProvider(BackupProvider):
    def __init__(self, config: DBConfig):
        super().__init__(config)
        self._check_tools_installed()

    def _check_tools_installed(self) -> None:
        for tool in ("psql", "pg_dump", "pg_restore"):
            if shutil.which(tool) is None:
                raise EnvironmentError(
                    f"Required tool '{tool}' not found on PATH. "
                    f"Install the postgresql-client package first."
                )

    def _env(self) -> dict:
        """Pass the password via PGPASSWORD env var instead of a CLI flag,
        so it never shows up in `ps aux` or shell history."""
        env = os.environ.copy()
        if self.config.password:
            env["PGPASSWORD"] = self.config.password
        return env

    def _base_args(self) -> list:
        args = ["-h", self.config.host, "-U", self.config.username or "postgres"]
        if self.config.port:
            args += ["-p", str(self.config.port)]
        return args

    def test_connection(self) -> bool:
        cmd = ["psql", *self._base_args(), "-d", self.config.database, "-c", "SELECT 1;"]
        logger.info(f"Testing connection to Postgres database '{self.config.database}'")
        result = subprocess.run(
            cmd, env=self._env(), capture_output=True, text=True
        )
        if result.returncode == 0:
            logger.info("Connection successful")
            return True
        logger.error(f"Connection failed: {result.stderr.strip()}")
        return False

    def backup(self, output_path: str) -> str:
        Path(output_path).mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.config.database}_{timestamp}.dump"
        full_path = str(Path(output_path) / filename)

        # -Fc = custom format: compressed by default, and required for pg_restore
        cmd = [
            "pg_dump",
            *self._base_args(),
            "-d", self.config.database,
            "-Fc",
            "-f", full_path,
        ]

        logger.info(f"Starting backup of '{self.config.database}' -> {full_path}")
        start = datetime.now()

        result = subprocess.run(cmd, env=self._env(), capture_output=True, text=True)

        duration = (datetime.now() - start).total_seconds()

        if result.returncode != 0:
            logger.error(f"Backup failed after {duration:.2f}s: {result.stderr.strip()}")
            raise RuntimeError(f"pg_dump failed: {result.stderr.strip()}")

        logger.info(f"Backup completed in {duration:.2f}s -> {full_path}")
        return full_path

    def restore(self, backup_file: str) -> None:
        if not Path(backup_file).exists():
            raise FileNotFoundError(f"Backup file not found: {backup_file}")

        cmd = [
            "pg_restore",
            *self._base_args(),
            "-d", self.config.database,
            "--clean",       # drop existing objects before recreating them
            "--if-exists",   # don't error if an object doesn't exist yet
            backup_file,
        ]

        logger.info(f"Starting restore of '{self.config.database}' from {backup_file}")
        start = datetime.now()

        result = subprocess.run(cmd, env=self._env(), capture_output=True, text=True)

        duration = (datetime.now() - start).total_seconds()

        if result.returncode != 0:
            logger.error(f"Restore failed after {duration:.2f}s: {result.stderr.strip()}")
            raise RuntimeError(f"pg_restore failed: {result.stderr.strip()}")

        logger.info(f"Restore completed in {duration:.2f}s")