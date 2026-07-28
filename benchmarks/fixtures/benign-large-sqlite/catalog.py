"""A deliberately simple, single-owner local catalog."""

import sqlite3
from pathlib import Path


def open_catalog(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def replace_generated_lookup(
    connection: sqlite3.Connection,
    rows: list[tuple[str, str]],
) -> None:
    with connection:
        connection.execute("DELETE FROM generated_lookup")
        connection.executemany(
            "INSERT INTO generated_lookup(key, value) VALUES (?, ?)",
            rows,
        )
