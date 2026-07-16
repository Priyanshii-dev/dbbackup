"""
Database Backup Utility - CLI entrypoint

Run:
    python main.py --help
    python main.py backup --help
    python main.py restore --help
    python main.py test-connection --help
"""

from enum import Enum
from typing import Optional

import typer

from app.core.config import DBConfig
from app.providers.factory import get_provider

app = typer.Typer(help="Database Backup Utility CLI")


class DBType(str, Enum):
    postgres = "postgres"
    mysql = "mysql"
    mongo = "mongo"
    sqlite = "sqlite"


@app.command("test-connection")
def test_connection(
    db_type: DBType = typer.Option(..., help="Type of database"),
    host: str = typer.Option("localhost", help="Database host"),
    port: Optional[int] = typer.Option(None, help="Database port"),
    username: Optional[str] = typer.Option(None, help="Database username"),
    password: Optional[str] = typer.Option(
        None, prompt=True, hide_input=True, help="Database password"
    ),
    database: str = typer.Option(..., help="Database name"),
):
    """Validate connection parameters against the target database."""
    config = DBConfig(
        db_type=db_type.value, host=host, port=port,
        username=username, password=password, database=database,
    )
    try:
        provider = get_provider(db_type.value, config)
    except (ValueError, EnvironmentError) as e:
        typer.secho(f"✘ {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    ok = provider.test_connection()
    if ok:
        typer.secho(f"✔ Connection to '{database}' succeeded", fg=typer.colors.GREEN)
    else:
        typer.secho(f"✘ Connection to '{database}' failed", fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command()
def backup(
    db_type: DBType = typer.Option(..., help="Type of database"),
    host: str = typer.Option("localhost", help="Database host"),
    port: Optional[int] = typer.Option(None, help="Database port"),
    username: Optional[str] = typer.Option(None, help="Database username"),
    password: Optional[str] = typer.Option(
        None, prompt=True, hide_input=True, help="Database password"
    ),
    database: str = typer.Option(..., help="Database name"),
    output_dir: str = typer.Option("./backups", help="Local directory to store the backup"),
):
    """Backup a database."""
    config = DBConfig(
        db_type=db_type.value, host=host, port=port,
        username=username, password=password, database=database,
    )
    try:
        provider = get_provider(db_type.value, config)
        backup_path = provider.backup(output_dir)
    except (ValueError, RuntimeError, EnvironmentError) as e:
        typer.secho(f"✘ Backup failed: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.secho(f"✔ Backup saved to {backup_path}", fg=typer.colors.GREEN)


@app.command()
def restore(
    db_type: DBType = typer.Option(..., help="Type of database"),
    host: str = typer.Option("localhost", help="Database host"),
    port: Optional[int] = typer.Option(None, help="Database port"),
    username: Optional[str] = typer.Option(None, help="Database username"),
    password: Optional[str] = typer.Option(
        None, prompt=True, hide_input=True, help="Database password"
    ),
    database: str = typer.Option(..., help="Database name"),
    backup_file: str = typer.Option(..., help="Path to the backup file to restore from"),
):
    """Restore a database from a backup file."""
    config = DBConfig(
        db_type=db_type.value, host=host, port=port,
        username=username, password=password, database=database,
    )
    try:
        provider = get_provider(db_type.value, config)
        provider.restore(backup_file)
    except (ValueError, RuntimeError, EnvironmentError, FileNotFoundError) as e:
        typer.secho(f"✘ Restore failed: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.secho(f"✔ Restored '{database}' from {backup_file}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()