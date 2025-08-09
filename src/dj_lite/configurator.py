from typeguard import typechecked
from typing import Optional
from pathlib import Path
from dj_lite.enums import Synchronous, TempStore, JournalMode, TransactionMode


@typechecked
def sqlite_config(
    base_dir: Path,
    *,
    file_name: str = "db.sqlite3",
    engine: str = "django.db.backends.sqlite3",
    transaction_mode: TransactionMode = TransactionMode.IMMEDIATE,
    timeout: int = 5,
    init_command: Optional[str] = None,
    journal_mode: JournalMode = JournalMode.WAL,
    synchronous: Synchronous = Synchronous.NORMAL,
    temp_store: TempStore = TempStore.MEMORY,
    mmap_size: int = 134217728,
    journal_size_limit: int = 27103364,
    cache_size: int = 2000,
    pragmas: Optional[dict] = None,
):
    """Generate a Django database configuration dictionary for SQLite. It provides sensible defaults
    while allowing customization of key SQLite parameters.

    Args:
        base_dir: Directory where the database file will be stored.
        file_name: Name of the SQLite database file. Defaults to 'db.sqlite3'.
        engine: Django database backend to use. Defaults to 'django.db.backends.sqlite3'.
        transaction_mode: The transaction locking behavior. Defaults to 'IMMEDIATE'.
        timeout: Time in seconds to wait for a database lock before raising an error. Defaults to 5.
        init_command: Custom SQL command to execute when the database connection is created.
            If None, will be generated from other parameters.
        journal_mode: The journal mode for the database. Defaults to 'WAL'.
        synchronous: How aggressively SQLite syncs data to disk. Defaults to 'NORMAL'.
        temp_store: How to store temporary objects. Defaults to 'MEMORY'.
        mmap_size: Maximum number of bytes to use for memory-mapped I/O. Defaults to 134217728.
        journal_size_limit: Maximum size of the journal in bytes. Defaults to 27103364.
        cache_size: Maximum number of database disk pages to hold in memory. Defaults to 2000.
        pragmas: Additional PRAGMA statements to include in the init command.
            These will override any conflicting settings from other parameters.

    Returns:
        A dictionary containing the database configuration for Django's DATABASES setting.

    Example:
        ```python
        from pathlib import Path
        from dj_lite import sqlite_config

        DATABASES = {
            'default': sqlite_config(
                base_dir=Path(__file__).parent,
                file_name='myapp.db',
                cache_size=4000
            )
        }
        ```
    """

    if pragmas is None:
        pragmas = {}

    # Get default pragmas based on kwargs passed in if there isn't an init_command passed-in
    if not init_command:
        init_command = ""

        default_pragmas = {
            "journal_mode": journal_mode,
            "synchronous": synchronous,
            "temp_store": temp_store,
            "mmap_size": mmap_size,
            "journal_size_limit": journal_size_limit,
            "cache_size": cache_size,
        }

        pragmas.update({k: v for k, v in default_pragmas.items() if k not in pragmas})

    # Update the init_command with an extra pragmas
    if pragmas:
        for key, value in pragmas.items():
            init_command = f"""{init_command}PRAGMA {key}={value};
"""

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
