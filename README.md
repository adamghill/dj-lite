# dj-lite

>Use SQLite in production with Django

## Overview

Simplify deploying and maintaining production Django websites by using SQLite in production. `dj-lite` helps enable the best performance for SQLite for small to medium-sized projects. It requires Django 5.1+.

## Installation

1. Install `dj-lite` with `pip`, `uv`, etc.

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

3. That's it! You're all set to go.

## What is even happening here

The Django defaults for SQLite are not great for production use. `dj-lite` tunes SQLite so it can be safely used in production.

### Init Command

When SQLite opens a database connection, settings (called `pragmas`) can be passed in to tune the performance. `dj-lite` comes with highly tuned defaults for these `pragmas`.

```
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;
PRAGMA mmap_size=134217728;
PRAGMA journal_size_limit=27103364;
PRAGMA cache_size=2000;
```

### Transaction Mode

According to the [Django documentation](https://docs.djangoproject.com/en/stable/ref/databases/#transactions-behavior), SQLite supports three transaction modes: `DEFERRED`, `IMMEDIATE`, and `EXCLUSIVE`. However, the default is `DEFERRED`. However, "[to] make sure your transactions wait until timeout before raising “Database is Locked”, change the transaction mode to IMMEDIATE."

In my experience, using `IMMEDIATE` has been ok as long as database queries are short.

Note: `django-tasks` requires a transaction mode of `EXCLUSIVE` for locking purposes.

## Inspiration

- https://github.com/oldmoe/litestack
- https://blog.pecar.me/django-sqlite-dblock
- https://blog.pecar.me/sqlite-prod
- https://blog.pecar.me/sqlite-django-config

## Developing

### Run the tests

1. `uv pip install -e .`
2. `uv run pytest`
