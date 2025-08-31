from dj_lite.configurator import sqlite_config
from dj_lite.enums import JournalMode, Synchronous, TempStore, TransactionMode

SQLITE_INIT_COMMAND = """PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
PRAGMA temp_store=MEMORY;
PRAGMA mmap_size=134217728;
PRAGMA journal_size_limit=27103364;
PRAGMA cache_size=2000;
"""


__all__ = [
    "SQLITE_INIT_COMMAND",
    "JournalMode",
    "Synchronous",
    "TempStore",
    "TransactionMode",
    "sqlite_config",
]
