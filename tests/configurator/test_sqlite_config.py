from copy import deepcopy
from pathlib import Path

import pytest
from typeguard import TypeCheckError

from dj_lite import (
    SQLITE_INIT_COMMAND,
    JournalMode,
    Synchronous,
    TransactionMode,
    sqlite_config,
)

default = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": Path("db.sqlite3"),
    "OPTIONS": {
        "transaction_mode": "IMMEDIATE",
        "timeout": 5,
        "init_command": SQLITE_INIT_COMMAND,
    },
}


def test_default():
    expected = deepcopy(default)

    actual = sqlite_config(Path("."))

    assert actual == expected


def test_file_name():
    expected = deepcopy(default)
    expected["NAME"] = Path("custom_db.sqlite3")

    actual = sqlite_config(Path("."), file_name="custom_db.sqlite3")

    assert actual == expected


def test_engine():
    expected = deepcopy(default)
    expected["ENGINE"] = "custom.engine.path"

    actual = sqlite_config(Path("."), engine="custom.engine.path")

    assert actual == expected


def test_transaction_mode_deferred():
    expected = deepcopy(default)
    expected["OPTIONS"]["transaction_mode"] = "DEFERRED"

    actual = sqlite_config(Path("."), transaction_mode=TransactionMode.DEFERRED)

    assert actual == expected


def test_transaction_mode_exclusive():
    expected = deepcopy(default)
    expected["OPTIONS"]["transaction_mode"] = "EXCLUSIVE"

    actual = sqlite_config(Path("."), transaction_mode=TransactionMode.EXCLUSIVE)

    assert actual == expected


def test_timeout():
    expected = deepcopy(default)
    expected["OPTIONS"]["timeout"] = 30

    actual = sqlite_config(Path("."), timeout=30)

    assert actual == expected


def test_init_command():
    init_command = """
PRAGMA journal_mode=WAL;
PRAGMA synchronous=FULL;"""

    expected = deepcopy(default)
    expected["OPTIONS"]["init_command"] = init_command

    actual = sqlite_config(Path("."), init_command=init_command)

    assert actual == expected


def test_cache_size():
    expected = deepcopy(default)
    expected["OPTIONS"]["init_command"] = expected["OPTIONS"]["init_command"].replace(
        "PRAGMA cache_size=2000", "PRAGMA cache_size=1"
    )

    actual = sqlite_config(Path("."), cache_size=1)

    assert actual == expected


def test_journal_mode():
    expected = deepcopy(default)
    expected["OPTIONS"]["init_command"] = expected["OPTIONS"]["init_command"].replace(
        "PRAGMA journal_mode=WAL;", "PRAGMA journal_mode=DELETE;"
    )

    actual = sqlite_config(Path("."), journal_mode=JournalMode.DELETE)

    assert actual == expected


def test_synchronous():
    expected = deepcopy(default)
    expected["OPTIONS"]["init_command"] = expected["OPTIONS"]["init_command"].replace(
        "PRAGMA synchronous=NORMAL;", "PRAGMA synchronous=FULL;"
    )

    actual = sqlite_config(Path("."), synchronous=Synchronous.FULL)

    assert actual == expected


def test_mmap_size():
    expected = deepcopy(default)
    expected["OPTIONS"]["init_command"] = expected["OPTIONS"]["init_command"].replace(
        "PRAGMA mmap_size=134217728;", "PRAGMA mmap_size=268435456;"
    )

    actual = sqlite_config(Path("."), mmap_size=268435456)

    assert actual == expected


def test_journal_size_limit():
    expected = deepcopy(default)
    expected["OPTIONS"]["init_command"] = expected["OPTIONS"]["init_command"].replace(
        "PRAGMA journal_size_limit=27103364;", "PRAGMA journal_size_limit=10000000;"
    )

    actual = sqlite_config(Path("."), journal_size_limit=10000000)

    assert actual == expected


def test_incorrect_type():
    with pytest.raises(TypeCheckError) as e:
        sqlite_config(Path("."), journal_size_limit="ohno")

    assert e.exconly() == 'typeguard.TypeCheckError: argument "journal_size_limit" (str) is not an instance of int'


def test_extra_kwargs():
    expected = deepcopy(default)
    expected["OPTIONS"]["init_command"] = f"""PRAGMA something_extra=123;
{expected["OPTIONS"]["init_command"]}"""

    actual = sqlite_config(Path("."), pragmas={"something_extra": 123})

    assert actual == expected


def test_extra_kwargs_overrides():
    expected = deepcopy(default)
    expected["OPTIONS"]["init_command"] = expected["OPTIONS"]["init_command"].replace(
        "PRAGMA journal_mode=WAL;", "PRAGMA journal_mode=OOPS;"
    )

    actual = sqlite_config(Path("."), pragmas={"journal_mode": "OOPS"})

    assert actual == expected
