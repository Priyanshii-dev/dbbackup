from abc import ABC, abstractmethod

from app.core.config import DBConfig


class BackupProvider(ABC):
    def __init__(self, config: DBConfig):
        self.config = config

    @abstractmethod
    def test_connection(self) -> bool:
        """Return True if a connection can be established with the given config."""
        raise NotImplementedError

    @abstractmethod
    def backup(self, output_path: str) -> str:
        """Run the backup and return the path to the created backup file."""
        raise NotImplementedError

    @abstractmethod
    def restore(self, backup_file: str) -> None:
        """Restore the database from the given backup file."""
        raise NotImplementedError