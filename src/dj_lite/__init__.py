from typeguard import typechecked
from enum import StrEnum
from pathlib import Path


SQLITE_INIT_COMMAND = """
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
PRAGMA mmap_size=134217728;
PRAGMA journal_size_limit=27103364;
PRAGMA cache_size=2000;
"""


class TransactionMode(StrEnum):
    DEFERRED = "DEFERRED"
    IMMEDIATE = "IMMEDIATE"
    EXCLUSIVE = "EXCLUSIVE"


@typechecked
def sqlite_config(
    base_dir: Path,
    *,
    file_name: str = "db.sqlite3",
    engine: str = "django.db.backends.sqlite3",
    transaction_mode: TransactionMode = TransactionMode.IMMEDIATE,
    timeout: int = 5,
    init_command: str = SQLITE_INIT_COMMAND,
):
    config = {
        "ENGINE": engine,
        "NAME": base_dir / file_name,
        "OPTIONS": {
            "transaction_mode": str(transaction_mode),
            "timeout": timeout,
            "init_command": init_command,
        },
    }

    return config


__all__ = [
    sqlite_config,
    SQLITE_INIT_COMMAND,
]
