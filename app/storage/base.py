"""
Abstract interface that every storage backend must implement.
Phase 6 will add LocalStorage, S3Storage, etc.
"""

from abc import ABC, abstractmethod
from typing import List


class StorageBackend(ABC):
    @abstractmethod
    def save(self, file_path: str) -> str:
        """Persist the given local file to this backend, return its final location."""
        raise NotImplementedError

    @abstractmethod
    def list_backups(self) -> List[str]:
        """List available backup files in this backend."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, file_path: str) -> None:
        """Delete a backup file from this backend."""
        raise NotImplementedError