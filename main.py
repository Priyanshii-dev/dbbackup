from enum import Enum
from typing import Optional

import typer

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
    typer.echo(f"[stub] Would test connection to {db_type} database '{database}' at {host}")
    # TODO: build config -> pick provider -> call provider.test_connection()


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
    compress: bool = typer.Option(True, help="Compress the backup file"),
):
    """Backup a database."""
    typer.echo(f"[stub] Would back up {db_type} database '{database}' -> {output_dir}")
    # TODO: build config -> pick provider -> call provider.backup()


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
    typer.echo(f"[stub] Would restore {db_type} database '{database}' from {backup_file}")
    # TODO: build config -> pick provider -> call provider.restore()


if __name__ == "__main__":
    app()