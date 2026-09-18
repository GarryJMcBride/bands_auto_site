# db_migrate.py
"""Sync the live database to the table definitions in src/backend/schemas.py.

    python -m scripts.db_migrate            # dry run: show what would change
    python -m scripts.db_migrate --apply    # run the safe changes in one transaction

`CREATE TABLE IF NOT EXISTS` (run by the app at startup) never alters an existing table, so a
column added to schemas.py won't reach a database created earlier. This script closes that gap
without a hand-maintained migration list: it runs the DDL from schemas.py into a throwaway
schema (rolled back afterwards), reads back what Postgres made of it, and diffs that against
the real tables.

Only additive changes are applied: missing tables and missing columns. Anything that could lose
data or needs a judgement call (extra DB columns, changed types/nullability/defaults, new
NOT NULL columns with no DEFAULT on a table that already has rows) is reported, never applied.
Constraints and indexes beyond NOT NULL/DEFAULT are not compared.

Exit code is 1 if anything was refused or has drifted, otherwise 0.
"""

import argparse
import asyncio
from dataclasses import dataclass, field

import asyncpg

from scripts._db import DDL_STATEMENTS, Column, connect, load_columns, quote_ident

SCRATCH_SCHEMA = "_schema_check"


@dataclass
class Plan:
    statements: list[str] = field(default_factory=list)  # safe changes, in order
    refused: list[str] = field(default_factory=list)  # additive changes that would fail
    drift: list[str] = field(default_factory=list)  # differences we never auto-apply


async def load_desired(conn: asyncpg.Connection) -> tuple[dict[str, dict[str, Column]], dict[str, str]]:
    """Run schemas.py's DDL in a scratch schema; return (its columns, table -> DDL that creates it)."""
    desired: dict[str, dict[str, Column]] = {}
    table_ddl: dict[str, str] = {}
    tx = conn.transaction()
    await tx.start()
    try:
        await conn.execute(f"CREATE SCHEMA {SCRATCH_SCHEMA}")
        await conn.execute(f"SET LOCAL search_path TO {SCRATCH_SCHEMA}")
        for ddl in DDL_STATEMENTS:
            known = set(desired)
            await conn.execute(ddl)
            desired = await load_columns(conn, SCRATCH_SCHEMA)
            for table in desired.keys() - known:
                table_ddl[table] = ddl.strip()
    finally:
        await tx.rollback()
    return desired, table_ddl


def add_column_sql(table: str, col: Column) -> str:
    sql = f"ALTER TABLE {quote_ident(table)} ADD COLUMN {quote_ident(col.name)} {col.type}"
    if col.default is not None:
        sql += f" DEFAULT {col.default}"
    if col.not_null:
        sql += " NOT NULL"
    return sql + ";"


async def build_plan(conn: asyncpg.Connection) -> Plan:
    schema = await conn.fetchval("SELECT current_schema()")
    actual = await load_columns(conn, schema)
    desired, table_ddl = await load_desired(conn)

    plan = Plan()
    for table, want_cols in desired.items():
        if table not in actual:
            plan.statements.append(table_ddl[table])
            continue

        have_cols = actual[table]
        row_count: int | None = None  # fetched lazily, only if a NOT NULL column needs it

        for name, want in want_cols.items():
            have = have_cols.get(name)
            if have is None:
                if want.not_null and want.default is None:
                    if row_count is None:
                        row_count = await conn.fetchval(f"SELECT count(*) FROM {quote_ident(table)}")
                    if row_count:
                        plan.refused.append(
                            f"{table}.{name}: NOT NULL with no DEFAULT, but the table has {row_count} row(s). "
                            "Give it a DEFAULT or make it nullable in schemas.py."
                        )
                        continue
                plan.statements.append(add_column_sql(table, want))
            elif have != want:
                plan.drift.append(
                    f"{table}.{name}: database has {describe(have)}, schemas.py has {describe(want)}. "
                    "Alter it manually if intended."
                )

        for name in have_cols.keys() - want_cols.keys():
            plan.drift.append(
                f"{table}.{name}: exists in the database but not in schemas.py "
                "(renamed or removed? drop it manually if intended)."
            )
    return plan


def describe(col: Column) -> str:
    parts = [col.type]
    if col.not_null:
        parts.append("NOT NULL")
    if col.default is not None:
        parts.append(f"DEFAULT {col.default}")
    return " ".join(parts)


async def main(apply: bool) -> int:
    conn = await connect()
    try:
        plan = await build_plan(conn)

        if plan.statements:
            print("Changes to apply:" if apply else "Changes that would be applied (dry run):")
            for statement in plan.statements:
                print("  " + statement.replace("\n", "\n  "))
        elif not (plan.refused or plan.drift):
            print("No changes needed - the database matches schemas.py.")
        else:
            print("No safe changes to apply.")

        for heading, items in (("REFUSED", plan.refused), ("DRIFT (not auto-applied)", plan.drift)):
            if items:
                print(f"\n{heading}:")
                for item in items:
                    print(f"  - {item}")

        if apply and plan.statements:
            async with conn.transaction():
                for statement in plan.statements:
                    await conn.execute(statement)
            print(f"\nApplied {len(plan.statements)} statement(s).")
        elif plan.statements:
            print("\nDry run only - re-run with --apply to make these changes.")

        return 1 if plan.refused or plan.drift else 0
    finally:
        await conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync the database tables to src/backend/schemas.py.")
    parser.add_argument("--apply", action="store_true", help="execute the changes (default is a dry run)")
    raise SystemExit(asyncio.run(main(parser.parse_args().apply)))
