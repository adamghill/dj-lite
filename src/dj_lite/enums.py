from enum import StrEnum


class TransactionMode(StrEnum):
    """Defines the transaction locking behavior in SQLite.

    Attributes:
        DEFERRED: No locks are acquired until the database is first accessed.
        IMMEDIATE: A RESERVED lock is acquired immediately.
        EXCLUSIVE: An EXCLUSIVE lock is acquired immediately.
    """

    DEFERRED = "DEFERRED"
    IMMEDIATE = "IMMEDIATE"
    EXCLUSIVE = "EXCLUSIVE"


class JournalMode(StrEnum):
    """Defines the journal mode for SQLite database.

    https://sqlite.org/pragma.html#pragma_journal_mode

    Attributes:
        DELETE: Default mode, uses a rollback journal.
        TRUNCATE: Similar to DELETE but truncates the journal file.
        PERSIST: Prevents the rollback journal from being deleted.
        MEMORY: Stores the rollback journal in RAM.
        WAL: Write-Ahead Logging mode.
        OFF: Disables the rollback journal.
    """

    DELETE = "DELETE"
    TRUNCATE = "TRUNCATE"
    PERSIST = "PERSIST"
    MEMORY = "MEMORY"
    WAL = "WAL"
    OFF = "OFF"


class Synchronous(StrEnum):
    """Defines how aggressively SQLite will sync data to disk.

    https://sqlite.org/pragma.html#pragma_synchronous

    Attributes:
        OFF: No syncs occur, fastest but least safe.
        NORMAL: Syncs occur at critical moments.
        FULL: Syncs after every critical operation.
        EXTRA: Like FULL but with additional syncs.
    """

    OFF = "OFF"
    NORMAL = "NORMAL"
    FULL = "FULL"
    EXTRA = "EXTRA"


class TempStore(StrEnum):
    """Defines how temporary files are stored.

    https://sqlite.org/pragma.html#pragma_temp_store

    Attributes:
        DEFAULT: Let SQLite decide the storage method.
        FILE: Store temporary objects in a file.
        MEMORY: Store temporary objects in memory.
    """

    DEFAULT = "DEFAULT"
    FILE = "FILE"
    MEMORY = "MEMORY"
