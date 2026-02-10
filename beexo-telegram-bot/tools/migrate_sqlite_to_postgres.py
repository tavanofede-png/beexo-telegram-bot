"""One-shot migration utility: copy data from local SQLite to a Postgres DATABASE_URL.

Usage:
  python migrate_sqlite_to_postgres.py --sqlite-path ./beexo-telegram-bot/beexy_history.db --database-url "postgres://..."

The script copies tables: interactions, kb_docs (uses rowid as id), reports, reminders.
It preserves numeric IDs when possible and advances Postgres sequences.
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
import traceback
from typing import Iterable, List, Tuple


def chunked(iterable: Iterable, size: int):
    it = iter(iterable)
    while True:
        chunk = []
        try:
            for _ in range(size):
                chunk.append(next(it))
        except StopIteration:
            if chunk:
                yield chunk
            break
        yield chunk


def migrate(sqlite_path: str, database_url: str) -> None:
    try:
        import psycopg2
        import psycopg2.extras
    except Exception as e:
        print("psycopg2 is required. Install with: pip install psycopg2-binary")
        raise

    print(f"Opening SQLite DB: {sqlite_path}")
    sconn = sqlite3.connect(sqlite_path)
    sconn.row_factory = sqlite3.Row
    scur = sconn.cursor()

    print(f"Connecting to Postgres: {database_url.split('@')[-1] if '@' in database_url else database_url}")
    pconn = psycopg2.connect(database_url)
    pcur = pconn.cursor()

    # Create Postgres schema if missing
    print("Ensuring Postgres tables exist...")
    pcur.execute(
        """
        CREATE TABLE IF NOT EXISTS interactions (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT,
            user_name TEXT,
            question TEXT,
            answer TEXT,
            created_at TIMESTAMP
        )
        """
    )
    pcur.execute(
        """
        CREATE TABLE IF NOT EXISTS kb_docs (
            id BIGSERIAL PRIMARY KEY,
            title TEXT,
            content TEXT,
            source TEXT
        )
        """
    )
    pcur.execute(
        """
        CREATE TABLE IF NOT EXISTS reports (
            id BIGSERIAL PRIMARY KEY,
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
    pcur.execute(
        """
        CREATE TABLE IF NOT EXISTS reminders (
            id BIGSERIAL PRIMARY KEY,
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
    pconn.commit()

    def copy_table(select_sql: str, params: Tuple, insert_sql: str, transform_row=lambda r: r):
        scur.execute(select_sql, params or ())
        rows = scur.fetchall()
        if not rows:
            print(f"No rows to copy for query: {select_sql}")
            return 0
        total = 0
        # Use execute_values for faster bulk insert
        vals: List[Tuple] = [tuple(transform_row(r)) for r in rows]
        psycopg2.extras.execute_values(pcur, insert_sql, vals, page_size=500)
        pconn.commit()
        total = len(vals)
        print(f"Copied {total} rows.")
        return total

    print("Copying interactions...")
    try:
        # SQLite interactions may have id column
        try:
            scur.execute("SELECT id, user_id, user_name, question, answer, created_at FROM interactions")
            _ = scur.fetchone()
            scur.execute("SELECT id, user_id, user_name, question, answer, created_at FROM interactions")
            rows = scur.fetchall()
            if rows:
                vals = []
                for r in rows:
                    vals.append((r[0], r[1], r[2], r[3], r[4], r[5]))
                psycopg2.extras.execute_values(
                    pcur,
                    "INSERT INTO interactions (id, user_id, user_name, question, answer, created_at) VALUES %s ON CONFLICT (id) DO NOTHING",
                    vals,
                    template=None,
                    page_size=500,
                )
                pconn.commit()
                print(f"Copied {len(vals)} interactions (preserved ids)")
        except sqlite3.OperationalError:
            # Fallback: try selecting without id
            scur.execute("SELECT user_id, user_name, question, answer, created_at FROM interactions")
            rows = scur.fetchall()
            if rows:
                vals = [tuple(r) for r in rows]
                psycopg2.extras.execute_values(
                    pcur,
                    "INSERT INTO interactions (user_id, user_name, question, answer, created_at) VALUES %s",
                    vals,
                    page_size=500,
                )
                pconn.commit()
                print(f"Copied {len(vals)} interactions (new ids)")
    except Exception:
        print("Failed to copy interactions:")
        traceback.print_exc()

    print("Copying kb_docs (using rowid as id)...")
    try:
        scur.execute("SELECT rowid, title, content, source FROM kb_docs")
        rows = scur.fetchall()
        if rows:
            vals = [(r[0], r[1], r[2], r[3]) for r in rows]
            psycopg2.extras.execute_values(
                pcur,
                "INSERT INTO kb_docs (id, title, content, source) VALUES %s ON CONFLICT (id) DO NOTHING",
                vals,
                page_size=500,
            )
            pconn.commit()
            print(f"Copied {len(vals)} kb_docs (preserved rowid as id)")
    except Exception:
        print("Failed to copy kb_docs:")
        traceback.print_exc()

    print("Copying reports...")
    try:
        scur.execute("SELECT id, reporter_id, reporter_name, reported_id, reported_name, chat_id, reason, created_at, handled FROM reports")
        rows = scur.fetchall()
        if rows:
            vals = [tuple(r) for r in rows]
            psycopg2.extras.execute_values(
                pcur,
                "INSERT INTO reports (id, reporter_id, reporter_name, reported_id, reported_name, chat_id, reason, created_at, handled) VALUES %s ON CONFLICT (id) DO NOTHING",
                vals,
                page_size=500,
            )
            pconn.commit()
            print(f"Copied {len(vals)} reports")
    except Exception:
        print("Failed to copy reports (maybe table missing):")
        traceback.print_exc()

    print("Copying reminders...")
    try:
        scur.execute("SELECT id, user_id, user_name, chat_id, text, scheduled_at, created_at, fired FROM reminders")
        rows = scur.fetchall()
        if rows:
            vals = [tuple(r) for r in rows]
            psycopg2.extras.execute_values(
                pcur,
                "INSERT INTO reminders (id, user_id, user_name, chat_id, text, scheduled_at, created_at, fired) VALUES %s ON CONFLICT (id) DO NOTHING",
                vals,
                page_size=500,
            )
            pconn.commit()
            print(f"Copied {len(vals)} reminders")
    except Exception:
        print("Failed to copy reminders (maybe table missing):")
        traceback.print_exc()

    # Advance sequences
    try:
        print("Advancing Postgres sequences to max(id) values...")
        seqs = [
            ("interactions",),
            ("kb_docs",),
            ("reports",),
            ("reminders",),
        ]
        for name, in seqs:
            try:
                pcur.execute(
                    "SELECT setval(pg_get_serial_sequence(%s, 'id'), COALESCE((SELECT MAX(id) FROM " + name + "), 1), true);"
                )
            except Exception:
                # best-effort; ignore failures
                pass
        pconn.commit()
    except Exception:
        print("Failed to advance sequences:")
        traceback.print_exc()

    print("Migration complete.")
    try:
        sconn.close()
    except Exception:
        pass
    try:
        pconn.close()
    except Exception:
        pass


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Migrate SQLite DB to Postgres")
    parser.add_argument("--sqlite-path", default="./beexo-telegram-bot/beexy_history.db")
    parser.add_argument("--database-url", required=True)
    args = parser.parse_args(argv)

    try:
        migrate(args.sqlite_path, args.database_url)
        return 0
    except Exception:
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
#!/usr/bin/env python3
"""Migrate data from local SQLite (`beexy_history.db`) to a Postgres `DATABASE_URL`.

Usage:
  python migrate_sqlite_to_postgres.py --database-url POSTGRES_URL
Or set env var `DATABASE_URL` and run without args.

This is a one-shot migration script that preserves numeric IDs and timestamps.
"""
import os
import argparse
import sqlite3
from datetime import datetime

try:
    import psycopg2
    from psycopg2.extras import execute_values
except ImportError:
    print("psycopg2 is required. Install with: pip install psycopg2-binary")
    raise


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--database-url", help="Postgres DATABASE_URL (overrides env)")
    p.add_argument(
        "--sqlite-path",
        help="Path to SQLite DB",
        default=None,
    )
    return p.parse_args()


def get_sqlite_path(provided: str | None) -> str:
    if provided:
        return provided
    # derive from package layout
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # here points to beexo-telegram-bot/ (package root)
    candidate = os.path.join(here, "beexy_history.db")
    if os.path.exists(candidate):
        return candidate
    # fallback: same folder as this script
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


def copy_table(conn_sqlite, pg_conn, table_name, columns, transform_row=None):
    s_cur = conn_sqlite.cursor()
    s_cur.execute(f"SELECT {', '.join(columns)} FROM {table_name}")
    rows = s_cur.fetchall()
    if not rows:
        print(f"{table_name}: 0 rows to migrate")
        return 0

    # Optionally transform each row (e.g., convert timestamp strings)
    if transform_row:
        rows = [transform_row(r) for r in rows]

    pg_cur = pg_conn.cursor()
    placeholders = ",".join(["%s"] * len(columns))
    cols = ",".join(columns)
    sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders}) ON CONFLICT (id) DO NOTHING"
    try:
        execute_values(pg_cur, sql, rows, page_size=100)
    except Exception:
        # fallback to executemany for small datasets
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


def main():
    args = parse_args()
    database_url = args.database_url or os.getenv("DATABASE_URL")
    if not database_url:
        print("Provide --database-url or set DATABASE_URL environment variable.")
        return

    sqlite_path = get_sqlite_path(args.sqlite_path)
    if not os.path.exists(sqlite_path):
        print(f"SQLite DB not found at {sqlite_path}")
        return

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
        "interactions",
        ["id", "user_id", "user_name", "question", "answer", "created_at"],
        transform_row=lambda r: (
            r[0],
            r[1],
            r[2],
            r[3],
            r[4],
            # convert ISO text to timestamp for Postgres if possible
            (r[5] if isinstance(r[5], str) and r[5] else None),
        ),
    )

    # kb_docs
    copy_table(
        conn_sqlite,
        pg_conn,
        "kb_docs",
        ["rowid as id", "title", "content", "source"],
    )

    # reports
    copy_table(
        conn_sqlite,
        pg_conn,
        "reports",
        ["id", "reporter_id", "reporter_name", "reported_id", "reported_name", "chat_id", "reason", "created_at", "handled"],
    )

    # reminders
    copy_table(
        conn_sqlite,
        pg_conn,
        "reminders",
        ["id", "user_id", "user_name", "chat_id", "text", "scheduled_at", "created_at", "fired"],
    )

    # set sequences where applicable
    for t in ("interactions", "kb_docs", "reports", "reminders"):
        set_sequence(pg_conn, t)

    conn_sqlite.close()
    pg_conn.close()
    print("Migration finished.")


if __name__ == "__main__":
    main()
