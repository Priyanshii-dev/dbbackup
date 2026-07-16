from app.core.config import DBConfig
from app.providers.base import BackupProvider
from app.providers.postgres import PostgresProvider

PROVIDERS = {
    "postgres": PostgresProvider,
}


def get_provider(db_type: str, config: DBConfig) -> BackupProvider:
    provider_cls = PROVIDERS.get(db_type)
    if provider_cls is None:
        supported = ", ".join(PROVIDERS.keys())
        raise ValueError(f"Unsupported db_type '{db_type}'. Supported: {supported}")
    return provider_cls(config)