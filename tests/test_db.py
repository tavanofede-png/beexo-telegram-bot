"""
Tests para db.py — operaciones CRUD y context managers.
"""

import sys
import os
import sqlite3

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "beexo-telegram-bot"))

# Forzar SQLite para testing (no postgres)
os.environ.pop("DATABASE_URL", None)
os.environ.setdefault("TELEGRAM_BOT_TOKEN", "test:token")
os.environ.setdefault("TARGET_CHAT_IDS", "123")
os.environ.setdefault("GROQ_API_KEY", "test_key")

import tempfile
import pytest

# Override DB_PATH antes de importar db
_tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_tmp.close()
os.environ["DB_PATH_OVERRIDE"] = _tmp.name

import config
config.DB_PATH = _tmp.name

import db

# Patch db module to use test path
db.DB_PATH = _tmp.name
# Also need to import config and override it for get_conn
import importlib


@pytest.fixture(autouse=True)
def fresh_db():
    """Crea una DB fresca para cada test."""
    db.DB_PATH = _tmp.name
    # Drop tables if exist  
    conn = sqlite3.connect(_tmp.name)
    cur = conn.cursor()
    for table in ["interactions", "reports", "reminders", "ai_history", "kb_docs"]:
        cur.execute(f"DROP TABLE IF EXISTS {table}")
    conn.commit()
    conn.close()
    db.init_db()
    yield


class TestGetConn:
    """Tests para el context manager de conexión."""

    def test_conn_opens_and_closes(self):
        with db.get_conn() as conn:
            assert conn is not None
            cur = conn.cursor()
            cur.execute("SELECT 1")
            assert cur.fetchone()[0] == 1

    def test_conn_closes_on_error(self):
        try:
            with db.get_conn() as conn:
                raise ValueError("test error")
        except ValueError:
            pass
        # No debería haber leak


class TestLogInteraction:
    """Tests para log_interaction."""

    def test_log_and_retrieve(self):
        db.log_interaction(42, "tester", "hola", "hola mundo")
        with db.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT user_id, user_name, question, answer FROM interactions")
            row = cur.fetchone()
        assert row is not None
        assert row[0] == 42
        assert row[1] == "tester"
        assert row[2] == "hola"
        assert row[3] == "hola mundo"


class TestSaveReport:
    """Tests para save_report."""

    def test_save_and_id(self):
        rid = db.save_report(1, "admin", 2, "spammer", 100, "spam")
        assert rid is not None and rid > 0

    def test_retrieves_report(self):
        db.save_report(1, "admin", 2, "bad_user", 100, "scam attempt")
        with db.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT reporter_name, reported_name, reason FROM reports")
            row = cur.fetchone()
        assert row[0] == "admin"
        assert row[1] == "bad_user"
        assert row[2] == "scam attempt"


class TestReminders:
    """Tests para save_reminder, get_pending, mark_fired."""

    def test_save_and_get_pending(self):
        rid = db.save_reminder(1, "user1", 100, "comprar ETH", 9999999999)
        assert rid is not None
        pending = db.get_pending_reminders()
        assert len(pending) == 1
        assert pending[0]["text"] == "comprar ETH"

    def test_mark_fired(self):
        rid = db.save_reminder(1, "user1", 100, "test", 9999999999)
        db.mark_reminder_fired(rid)
        pending = db.get_pending_reminders()
        assert len(pending) == 0


class TestAIHistory:
    """Tests para save_ai_message y load_ai_history."""

    def test_save_and_load(self):
        db.save_ai_message(42, "user", "hola")
        db.save_ai_message(42, "assistant", "hola!")
        history = db.load_ai_history(42)
        assert len(history) == 2
        assert history[0]["role"] == "user"
        assert history[1]["role"] == "assistant"

    def test_limit(self):
        for i in range(20):
            db.save_ai_message(42, "user", f"msg {i}")
        history = db.load_ai_history(42, limit=5)
        assert len(history) == 5

    def test_separate_users(self):
        db.save_ai_message(1, "user", "hola user 1")
        db.save_ai_message(2, "user", "hola user 2")
        h1 = db.load_ai_history(1)
        h2 = db.load_ai_history(2)
        assert len(h1) == 1
        assert len(h2) == 1
        assert h1[0]["content"] == "hola user 1"
