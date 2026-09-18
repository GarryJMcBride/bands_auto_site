# _db.py
"""Shared helpers for the one-shot database utility scripts (db_migrate.py, db_query.py).

These scripts open their own short-lived asyncpg connection rather than reusing the app's
`classes.db` pool, since the pool only exists while the FastAPI lifespan is running.
"""

import sys
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

import asyncpg

from src.backend import config, schemas

# Every table-creating statement in schemas.py. Add new CREATE_*_TABLE_SQL constants here
# (and in app.py's lifespan) when a new table is introduced.
DDL_STATEMENTS = [schemas.CREATE_BOOK_TABLE_SQL, schemas.CREATE_ENQUIRY_TABLE_SQL]

MAX_CELL_WIDTH = 60


@dataclass(frozen=True)
class Column:
    name: str
    type: str
    not_null: bool
    default: str | None


async def connect() -> asyncpg.Connection:
    """Open a connection using DATABASE_URL from .env, exiting with a clear message if unset."""
    if not config.DATABASE_URL:
        sys.exit("DATABASE_URL is not set - check your .env file.")
    return await asyncpg.connect(config.DATABASE_URL)


def quote_ident(name: str) -> str:
    """Quote a SQL identifier (table/column/schema name) so it is safe to interpolate."""
    return '"' + name.replace('"', '""') + '"'


async def load_columns(conn: asyncpg.Connection, schema: str) -> dict[str, dict[str, Column]]:
    """Return {table: {column: Column}} for every ordinary table in `schema`, in column order."""
    rows = await conn.fetch(
        """
        SELECT c.relname AS table_name,
               a.attname AS column_name,
               format_type(a.atttypid, a.atttypmod) AS data_type,
               a.attnotnull AS not_null,
               pg_get_expr(d.adbin, d.adrelid) AS default_expr
        FROM pg_attribute a
        JOIN pg_class c ON c.oid = a.attrelid
        JOIN pg_namespace n ON n.oid = c.relnamespace
        LEFT JOIN pg_attrdef d ON d.adrelid = a.attrelid AND d.adnum = a.attnum
        WHERE n.nspname = $1 AND c.relkind = 'r' AND a.attnum > 0 AND NOT a.attisdropped
        ORDER BY c.relname, a.attnum
        """,
        schema,
    )
    tables: dict[str, dict[str, Column]] = {}
    for r in rows:
        tables.setdefault(r["table_name"], {})[r["column_name"]] = Column(
            r["column_name"], r["data_type"], r["not_null"], r["default_expr"]
        )
    return tables


def _format_cell(value: Any) -> str:
    text = "NULL" if value is None else str(value).replace("\n", " ")
    return text if len(text) <= MAX_CELL_WIDTH else text[: MAX_CELL_WIDTH - 3] + "..."


def print_table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> None:
    """Print rows as a left-aligned text table; long values are truncated."""
    cells = [[_format_cell(v) for v in row] for row in rows]
    widths = [max([len(h), *(len(r[i]) for r in cells)]) for i, h in enumerate(headers)]
    print("  ".join(h.ljust(w) for h, w in zip(headers, widths, strict=True)))
    print("  ".join("-" * w for w in widths))
    for row in cells:
        print("  ".join(v.ljust(w) for v, w in zip(row, widths, strict=True)))
