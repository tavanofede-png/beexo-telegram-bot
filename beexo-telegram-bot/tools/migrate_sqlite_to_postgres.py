"""Migrate local SQLite (`beexy_history.db`) to Postgres.

This script will use `--database-url` if provided, or fall back to the
`DATABASE_URL` environment variable (so `railway run` can provide it).

Run inside Railway (recommended):
  railway run python beexo-telegram-bot/tools/migrate_sqlite_to_postgres.py

Or locally with an explicit URL:
  python beexo-telegram-bot/tools/migrate_sqlite_to_postgres.py --database-url "postgres://..."
"""

from __future__ import annotations

import os
import argparse
import sqlite3
import sys
from typing import Iterable, List, Tuple

try:
    import psycopg2
    from psycopg2.extras import execute_values
except Exception:
    print("psycopg2 is required. Install with: pip install psycopg2-binary")
    raise


def get_sqlite_path(provided: str | None) -> str:
    if provided:
        return provided
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidate = os.path.join(here, "beexy_history.db")
    if os.path.exists(candidate):
        return candidate
    candidate2 = os.path.join(os.path.dirname(__file__), "..", "beexy_history.db")
    return os.path.abspath(candidate2)


def ensure_postgres_schema(pg_conn):
    cur = pg_conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS interactions (
            id BIGINT PRIMARY KEY,
            user_id BIGINT,
            user_name TEXT,
            question TEXT,
            answer TEXT,
            created_at TIMESTAMP
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS kb_docs (
            id BIGINT PRIMARY KEY,
            title TEXT,
            content TEXT,
            source TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS reports (
            id BIGINT PRIMARY KEY,
            reporter_id BIGINT,
            reporter_name TEXT,
            reported_id BIGINT,
            reported_name TEXT,
            chat_id BIGINT,
            reason TEXT,
            created_at TIMESTAMP,
            handled INTEGER DEFAULT 0
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS reminders (
            id BIGINT PRIMARY KEY,
            user_id BIGINT,
            user_name TEXT,
            chat_id BIGINT,
            text TEXT,
            scheduled_at BIGINT,
            created_at TIMESTAMP,
            fired INTEGER DEFAULT 0
        )
        """
    )
    pg_conn.commit()


def copy_table(conn_sqlite, pg_conn, select_cols, table_name, transform_row=None):
    s_cur = conn_sqlite.cursor()
    s_cur.execute(f"SELECT {', '.join(select_cols)} FROM {table_name}")
    rows = s_cur.fetchall()
    if not rows:
        print(f"{table_name}: 0 rows to migrate")
        return 0

    if transform_row:
        rows = [transform_row(r) for r in rows]

    pg_cur = pg_conn.cursor()
    placeholders = ",".join(["%s"] * len(select_cols))
    cols = ",".join([c.replace(" rowid as ", "").split()[-1] if "rowid" in c else c for c in select_cols])
    sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders}) ON CONFLICT (id) DO NOTHING"
    try:
        execute_values(pg_cur, sql, rows, page_size=500)
    except Exception:
        pg_cur.executemany(sql, rows)
    pg_conn.commit()
    print(f"{table_name}: migrated {len(rows)} rows")
    return len(rows)


def set_sequence(pg_conn, table: str):
    cur = pg_conn.cursor()
    seq_sql = f"SELECT setval(pg_get_serial_sequence('{table}','id'), COALESCE((SELECT MAX(id) FROM {table}), 1))"
    try:
        cur.execute(seq_sql)
        pg_conn.commit()
    except Exception:
        pass


def parse_args():
    p = argparse.ArgumentParser(description="Migrate SQLite DB to Postgres (uses DATABASE_URL if set)")
    p.add_argument("--database-url", help="Postgres DATABASE_URL (overrides env)")
    p.add_argument("--sqlite-path", help="Path to SQLite DB", default=None)
    return p.parse_args()


def main():
    args = parse_args()
    database_url = args.database_url or os.getenv("DATABASE_URL")
    if not database_url:
        print("Provide --database-url or set DATABASE_URL environment variable.")
        return 2

    sqlite_path = get_sqlite_path(args.sqlite_path)
    if not os.path.exists(sqlite_path):
        print(f"SQLite DB not found at {sqlite_path}")
        return 2

    print(f"SQLite: {sqlite_path}")
    print(f"Postgres: {database_url[:40]}...")

    conn_sqlite = sqlite3.connect(sqlite_path)
    conn_sqlite.row_factory = None
    pg_conn = psycopg2.connect(database_url)

    ensure_postgres_schema(pg_conn)

    # interactions
    copy_table(
        conn_sqlite,
        pg_conn,
        ["id", "user_id", "user_name", "question", "answer", "created_at"],
        "interactions",
        transform_row=lambda r: (
            r[0],
            r[1],
            r[2],
            r[3],
            r[4],
            (r[5] if isinstance(r[5], str) and r[5] else None),
        ),
    )

    # kb_docs (use rowid as id)
    copy_table(
        conn_sqlite,
        pg_conn,
        ["rowid as id", "title", "content", "source"],
        "kb_docs",
    )

    # reports
    copy_table(
        conn_sqlite,
        pg_conn,
        ["id", "reporter_id", "reporter_name", "reported_id", "reported_name", "chat_id", "reason", "created_at", "handled"],
        "reports",
    )

    # reminders
    copy_table(
        conn_sqlite,
        pg_conn,
        ["id", "user_id", "user_name", "chat_id", "text", "scheduled_at", "created_at", "fired"],
        "reminders",
    )

    for t in ("interactions", "kb_docs", "reports", "reminders"):
        set_sequence(pg_conn, t)

    conn_sqlite.close()
    pg_conn.close()
    print("Migration finished.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
