from dj_lite import sqlite_config, TransactionMode
from pathlib import Path
from copy import deepcopy


default = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": Path("db.sqlite3"),
    "OPTIONS": {
        "transaction_mode": "IMMEDIATE",
        "timeout": 5,
        "init_command": """
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
PRAGMA mmap_size=134217728;
PRAGMA journal_size_limit=27103364;
PRAGMA cache_size=2000;\n""",
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
