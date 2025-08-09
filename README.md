# dj-lite

>Use SQLite in production with Django

## Overview

Simplify deploying and maintaining production Django websites by using SQLite in production. `dj-lite` helps enable the best performance for SQLite for small to medium-sized projects. It requires Django 5.1+.

I also wrote the [definitive guide to using Django SQLite in production](https://alldjango.com/articles/definitive-guide-to-using-django-sqlite-in-production) which has more details about the actual server setup and operations.

Also read through the [official Django SQLite notes](https://docs.djangoproject.com/en/stable/ref/databases/#sqlite-notes) for more low-level information.

## Installation

1. Install `dj-lite` with `pip`, `uv`, `poetry`, etc.

```bash
pip install dj-lite

OR

uv add dj-lite
```

2. In `settings.py` add the following.

```python
# settings.py

import dj_lite import sqlite_config

DATABASES = {
  "default": sqlite_config(BASE_DIR),
}
```

3. That's it! You're all set to go with the default configuration.

## Args and Kwargs

The `sqlite_config` method takes in many arguments to tweak the database settings.

### base_dir: `Path`

The directory where the database file will be stored. Required.

### file_name: `str`

Name of the SQLite database file. Defaults to 'db.sqlite3'.

### engine: `str`

Django database backend to use. Defaults to 'django.db.backends.sqlite3'.

### transaction_mode: `TransactionMode`

The transaction locking behavior. Defaults to 'IMMEDIATE'.

### timeout: `int`

Time in seconds to wait for a database lock before raising an error. Defaults to 5.

### init_command: `str`

Custom SQL command to execute when the database connection is created. If `None`, will be generated from other parameters.

### journal_mode: `JournalMode`

The journal mode for the database. Defaults to 'WAL'.

### synchronous: `Synchronous`

How aggressively SQLite syncs data to disk. Defaults to 'NORMAL'.

### temp_store: `TempStore`

How to store temporary objects. Defaults to 'MEMORY'.

### mmap_size: `int`

Maximum number of bytes to use for memory-mapped I/O. Defaults to 134217728.

### journal_size_limit: `int`

Maximum size of the journal in bytes. Defaults to 27103364.

### cache_size: `int`

Maximum number of database disk pages to hold in memory. Defaults to 2000.

### pragmas: `dict`

Additional PRAGMA statements to include in the init command. These will override any conflicting settings from other parameters.

## What is even happening here?

The Django defaults for SQLite are fine for local dev or running tests, but they are not great for production use -- specifically when there are concurrent reads/writes to the database. `dj-lite` tunes SQLite so it can be safely used in production.

### Pragmas

When SQLite opens a database connection, settings (called [`pragmas`](https://sqlite.org/pragma.html)) can be passed in to tune the performance. `dj-lite` comes with highly tuned defaults for these `pragmas`.

```
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
PRAGMA temp_store=MEMORY;
PRAGMA mmap_size=134217728;
PRAGMA journal_size_limit=27103364;
PRAGMA cache_size=2000;
```

#### What about the foreign_keys pragma?

You might notice that the SQLite `foreign_keys` `pragma` is not included above. That is because it is the one `pragma` that is [always passed in when Django creates a connection to SQLite](https://github.com/django/django/blob/7a80e29feaa675a27bf525164502ebc8ecbdce1a/django/db/backends/sqlite3/base.py#L209).

### Transaction Mode

According to the [Django documentation](https://docs.djangoproject.com/en/stable/ref/databases/#transactions-behavior), SQLite supports three transaction modes: `DEFERRED`, `IMMEDIATE`, and `EXCLUSIVE` -- the default is `DEFERRED`. However, "[to] make sure your transactions wait until timeout before raising “Database is Locked”, change the transaction mode to `IMMEDIATE`."

In my experience, using `IMMEDIATE` has been ok as long as database queries are short.

## Inspiration

- [Litestack](https://github.com/oldmoe/litestack)
- [Django, SQLite, and the Database is Locked Error](https://blog.pecar.me/django-sqlite-dblock)
- [Gotchas with SQLite in Production](https://blog.pecar.me/sqlite-prod)
- [Django SQLite Production Config](https://blog.pecar.me/sqlite-django-config)
- [DjangoCon Europe 2024 | Django, SQLite, and Production](youtube.com/watch?v=GTDYwEXv-sE)
- [DjangoCon Europe 2023 | Use SQLite in production](https://www.youtube.com/watch?v=yTicYJDT1zE)

## Developing

### Run the tests

1. `uv pip install -e .`
2. `uv run pytest`
