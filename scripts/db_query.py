# db_query.py
"""Quick read-oriented database queries for development.

    python -m scripts.db_query tables
    python -m scripts.db_query describe book_submissions
    python -m scripts.db_query head enquiry_submissions -n 5
    python -m scripts.db_query sql "SELECT service, count(*) FROM book_submissions GROUP BY service"
    python -m scripts.db_query sql "DELETE FROM book_submissions WHERE ..." --write

`sql` runs in a read-only transaction unless --write is passed, so a typo can't modify data.
Table names given to `describe`/`head` are checked against the real tables, then quoted.
"""

import argparse
import asyncio

import asyncpg

from scripts._db import Column, connect, load_columns, print_table, quote_ident


async def known_tables(conn: asyncpg.Connection) -> dict[str, dict[str, Column]]:
    return await load_columns(conn, await conn.fetchval("SELECT current_schema()"))


async def require_table(conn: asyncpg.Connection, name: str) -> dict[str, Column]:
    tables = await known_tables(conn)
    if name not in tables:
        raise SystemExit(f"No such table '{name}'. Tables: {', '.join(sorted(tables)) or '(none)'}")
    return tables[name]


async def cmd_tables(conn: asyncpg.Connection, _args: argparse.Namespace) -> None:
    rows = [
        (table, await conn.fetchval(f"SELECT count(*) FROM {quote_ident(table)}"))
        for table in sorted(await known_tables(conn))
    ]
    print_table(["table", "rows"], rows)


async def cmd_describe(conn: asyncpg.Connection, args: argparse.Namespace) -> None:
    columns = await require_table(conn, args.table)
    print_table(
        ["column", "type", "not null", "default"],
        [(c.name, c.type, "yes" if c.not_null else "", c.default) for c in columns.values()],
    )


async def cmd_head(conn: asyncpg.Connection, args: argparse.Namespace) -> None:
    columns = await require_table(conn, args.table)
    order = " ORDER BY submitted_at DESC" if "submitted_at" in columns else ""
    rows = await conn.fetch(f"SELECT * FROM {quote_ident(args.table)}{order} LIMIT $1", args.n)
    print_table(list(columns), [list(r.values()) for r in rows])


async def cmd_sql(conn: asyncpg.Connection, args: argparse.Namespace) -> None:
    async with conn.transaction(readonly=not args.write):
        stmt = await conn.prepare(args.statement)
        rows = await stmt.fetch()
        if stmt.get_attributes():
            print_table([a.name for a in stmt.get_attributes()], [list(r.values()) for r in rows])
        print(f"({stmt.get_statusmsg()})")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Development database queries.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("tables", help="list tables with row counts").set_defaults(func=cmd_tables)

    p = sub.add_parser("describe", help="show a table's columns")
    p.add_argument("table")
    p.set_defaults(func=cmd_describe)

    p = sub.add_parser("head", help="show the most recent rows of a table")
    p.add_argument("table")
    p.add_argument("-n", type=int, default=10, help="number of rows (default 10)")
    p.set_defaults(func=cmd_head)

    p = sub.add_parser("sql", help="run an ad-hoc statement (read-only unless --write)")
    p.add_argument("statement")
    p.add_argument("--write", action="store_true", help="allow the statement to modify data")
    p.set_defaults(func=cmd_sql)
    return parser


async def main() -> None:
    args = build_parser().parse_args()
    conn = await connect()
    try:
        await args.func(conn, args)
    except asyncpg.PostgresError as exc:
        raise SystemExit(f"Database error: {exc}") from exc
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
