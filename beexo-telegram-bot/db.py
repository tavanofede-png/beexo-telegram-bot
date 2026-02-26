"""
Capa de base de datos para BeeXy.
Soporta SQLite (local) y Postgres (Railway) de forma transparente.
Usa context managers para garantizar que las conexiones se cierren.
"""

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Generator

from config import DATABASE_URL, DB_PATH, logger


# ═══════════════════════════════════════════════════════════════
# CONEXIÓN
# ═══════════════════════════════════════════════════════════════

def _is_postgres() -> bool:
    return bool(DATABASE_URL)


@contextmanager
def get_conn() -> Generator:
    """Context manager que devuelve una conexión DB abierta y la cierra al salir."""
    conn = None
    try:
        if _is_postgres():
            import psycopg2
            conn = psycopg2.connect(DATABASE_URL)
        else:
            conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        yield conn
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass


def _ph(name: str = "?") -> str:
    """Devuelve el placeholder correcto según el backend."""
    return "%s" if _is_postgres() else "?"


def _now_str() -> str | datetime:
    """Devuelve el timestamp actual en el formato adecuado para el backend."""
    now = datetime.now(timezone.utc)
    return now if _is_postgres() else now.isoformat()


# ═══════════════════════════════════════════════════════════════
# INIT
# ═══════════════════════════════════════════════════════════════

def init_db() -> None:
    """Crea las tablas si no existen."""
    try:
        with get_conn() as conn:
            cur = conn.cursor()
            if _is_postgres():
                _init_postgres(cur)
            else:
                _init_sqlite(cur)
            conn.commit()
    except Exception as e:
        logger.warning("Error inicializando DB: %s", e)


def _init_postgres(cur: Any) -> None:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT,
            user_name TEXT,
            question TEXT,
            answer TEXT,
            created_at TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS kb_docs (
            id BIGSERIAL PRIMARY KEY,
            title TEXT,
            content TEXT,
            source TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    cur.execute("""
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
    """)
    cur.execute("""
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
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ai_history (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT,
            role TEXT,
            content TEXT,
            created_at TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_stats (
            user_id BIGINT PRIMARY KEY,
            user_name TEXT,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            last_message_at TIMESTAMP
        )
    """)


def _init_sqlite(cur: Any) -> None:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            user_name TEXT,
            question TEXT,
            answer TEXT,
            created_at TEXT
        )
    """)
    try:
        cur.execute("CREATE VIRTUAL TABLE IF NOT EXISTS kb_docs USING fts5(title, content, source);")
    except Exception:
        cur.execute("CREATE TABLE IF NOT EXISTS kb_docs (title TEXT, content TEXT, source TEXT);")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reporter_id INTEGER,
            reporter_name TEXT,
            reported_id INTEGER,
            reported_name TEXT,
            chat_id INTEGER,
            reason TEXT,
            created_at TEXT,
            handled INTEGER DEFAULT 0
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            user_name TEXT,
            chat_id INTEGER,
            text TEXT,
            scheduled_at INTEGER,
            created_at TEXT,
            fired INTEGER DEFAULT 0
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ai_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            role TEXT,
            content TEXT,
            created_at TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_stats (
            user_id INTEGER PRIMARY KEY,
            user_name TEXT,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            last_message_at TEXT
        )
    """)


# ═══════════════════════════════════════════════════════════════
# OPERACIONES CRUD
# ═══════════════════════════════════════════════════════════════

def log_interaction(user_id: int, user_name: str | None, question: str, answer: str) -> None:
    """Guarda una interacción IA en la base."""
    try:
        p = _ph()
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                f"INSERT INTO interactions (user_id, user_name, question, answer, created_at) "
                f"VALUES ({p}, {p}, {p}, {p}, {p})",
                (user_id, user_name or "", question, answer, _now_str()),
            )
            conn.commit()
    except Exception as e:
        logger.debug("Error logging interaction: %s", e)


def save_report(
    reporter_id: int, reporter_name: str,
    reported_id: int | None, reported_name: str,
    chat_id: int, reason: str,
) -> int | None:
    """Guarda un reporte y devuelve el ID."""
    try:
        p = _ph()
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                f"INSERT INTO reports (reporter_id, reporter_name, reported_id, reported_name, "
                f"chat_id, reason, created_at, handled) "
                f"VALUES ({p}, {p}, {p}, {p}, {p}, {p}, {p}, 0)",
                (reporter_id, reporter_name, reported_id, reported_name,
                 chat_id, reason, _now_str()),
            )
            conn.commit()
            return cur.lastrowid
    except Exception as e:
        logger.warning("Error guardando reporte: %s", e)
        return None


def save_reminder(
    user_id: int, user_name: str, chat_id: int,
    text: str, scheduled_at: int,
) -> int | None:
    """Guarda un recordatorio y devuelve el ID."""
    try:
        p = _ph()
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                f"INSERT INTO reminders (user_id, user_name, chat_id, text, scheduled_at, "
                f"created_at, fired) VALUES ({p}, {p}, {p}, {p}, {p}, {p}, 0)",
                (user_id, user_name, chat_id, text, scheduled_at, _now_str()),
            )
            conn.commit()
            return cur.lastrowid
    except Exception as e:
        logger.debug("Error guardando reminder: %s", e)
        return None


def mark_reminder_fired(reminder_id: int) -> None:
    """Marca un recordatorio como disparado."""
    try:
        p = _ph()
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(f"UPDATE reminders SET fired=1 WHERE id={p}", (reminder_id,))
            conn.commit()
    except Exception as e:
        logger.debug("Error marcando reminder: %s", e)


def get_pending_reminders() -> list[dict]:
    """Devuelve recordatorios pendientes."""
    try:
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, chat_id, user_id, user_name, text, scheduled_at "
                "FROM reminders WHERE fired=0 AND scheduled_at IS NOT NULL"
            )
            rows = cur.fetchall()
            return [
                {"id": r[0], "chat_id": r[1], "user_id": r[2],
                 "user_name": r[3], "text": r[4], "scheduled_at": r[5]}
                for r in rows
            ]
    except Exception as e:
        logger.debug("Error leyendo reminders: %s", e)
        return []


def query_kb(query: str, limit: int = 3) -> list[dict]:
    """Busca en la Knowledge Base."""
    if not query:
        return []
    try:
        with get_conn() as conn:
            cur = conn.cursor()
            p = _ph()
            if _is_postgres():
                pattern = f"%{query}%"
                cur.execute(
                    f"SELECT title, content, source FROM kb_docs "
                    f"WHERE content ILIKE {p} OR title ILIKE {p} LIMIT {p}",
                    (pattern, pattern, limit),
                )
            else:
                try:
                    cur.execute(
                        f"SELECT title, content, source FROM kb_docs WHERE kb_docs MATCH {p} LIMIT {p}",
                        (query, limit),
                    )
                except Exception:
                    cur.execute(
                        f"SELECT title, content, source FROM kb_docs WHERE content LIKE {p} OR title LIKE {p} LIMIT {p}",
                        (f"%{query}%", f"%{query}%", limit),
                    )
            rows = cur.fetchall()
            return [{"title": r[0], "content": r[1], "source": r[2] or ""} for r in rows]
    except Exception:
        return []


# ── AI History ──

def save_ai_message(user_id: int, role: str, content: str) -> None:
    """Persiste un mensaje del historial de IA."""
    try:
        p = _ph()
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                f"INSERT INTO ai_history (user_id, role, content, created_at) "
                f"VALUES ({p}, {p}, {p}, {p})",
                (user_id, role, content, _now_str()),
            )
            conn.commit()
    except Exception as e:
        logger.debug("Error guardando AI history: %s", e)


def load_ai_history(user_id: int, limit: int = 8) -> list[dict]:
    """Carga los últimos mensajes del historial de IA de un usuario."""
    try:
        p = _ph()
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                f"SELECT role, content FROM ("
                f"  SELECT role, content, created_at FROM ai_history "
                f"  WHERE user_id={p} ORDER BY created_at DESC LIMIT {p}"
                f") sub ORDER BY created_at ASC",
                (user_id, limit),
            )
            rows = cur.fetchall()
            return [{"role": r[0], "content": r[1]} for r in rows]
    except Exception:
        return []


# ═══════════════════════════════════════════════════════════════
# RANKING Y REPUTACIÓN (XP)
# ═══════════════════════════════════════════════════════════════

def add_xp(user_id: int, user_name: str, amount: int) -> tuple[int, int, bool]:
    """
    Suma XP a un usuario. Si sube de nivel, level_up es True. 
    Retorna (xp_actual, nivel_actual, level_up).
    """
    try:
        p = _ph()
        with get_conn() as conn:
            cur = conn.cursor()
            
            if _is_postgres():
                cur.execute(
                    f"INSERT INTO user_stats (user_id, user_name, xp, level, last_message_at) "
                    f"VALUES ({p}, {p}, {p}, 1, {p}) "
                    f"ON CONFLICT (user_id) DO UPDATE SET "
                    f"user_name = EXCLUDED.user_name, "
                    f"xp = user_stats.xp + EXCLUDED.xp, "
                    f"last_message_at = EXCLUDED.last_message_at "
                    f"RETURNING xp, level",
                    (user_id, user_name, amount, _now_str())
                )
                row = cur.fetchone()
                if not row:
                    return 0, 1, False
                xp, level = row[0], row[1]
            else:
                cur.execute("SELECT xp, level FROM user_stats WHERE user_id = ?", (user_id,))
                row = cur.fetchone()
                now = _now_str()
                if row:
                    xp = row[0] + amount
                    level = row[1]
                    cur.execute(
                        "UPDATE user_stats SET user_name = ?, xp = ?, last_message_at = ? WHERE user_id = ?",
                        (user_name, xp, now, user_id)
                    )
                else:
                    xp = amount
                    level = 1
                    cur.execute(
                        "INSERT INTO user_stats (user_id, user_name, xp, level, last_message_at) VALUES (?, ?, ?, ?, ?)",
                        (user_id, user_name, xp, level, now)
                    )
            
            # Fórmula simple: Nivel = int(sqrt(XP / 25)) + 1
            # L1: 0, L2: 25, L3: 100, L4: 225, L5: 400
            new_level = int((xp / 25) ** 0.5) + 1
            
            level_up = new_level > level
            if level_up:
                if _is_postgres():
                    cur.execute(f"UPDATE user_stats SET level = {p} WHERE user_id = {p}", (new_level, user_id))
                else:
                    cur.execute("UPDATE user_stats SET level = ? WHERE user_id = ?", (new_level, user_id))
            
            conn.commit()
            return xp, new_level, level_up
    except Exception as e:
        logger.warning("Error sumando XP: %s", e)
        return 0, 1, False


def get_top_users(limit: int = 10) -> list[dict]:
    """Devuelve el leaderboard de usuarios."""
    try:
        p = _ph()
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                f"SELECT user_id, user_name, xp, level FROM user_stats "
                f"ORDER BY xp DESC LIMIT {p}", 
                (limit,)
            )
            rows = cur.fetchall()
            return [
                {"user_id": r[0], "user_name": r[1], "xp": r[2], "level": r[3]} 
                for r in rows
            ]
    except Exception as e:
        logger.warning("Error obteniendo top users: %s", e)
        return []


def get_user_stats(user_id: int) -> dict | None:
    """Devuelve las estadísticas (XP, nivel) de un usuario."""
    try:
        p = _ph()
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT user_name, xp, level FROM user_stats WHERE user_id = {p}", (user_id,))
            r = cur.fetchone()
            if r:
                return {"user_name": r[0], "xp": r[1], "level": r[2]}
    except Exception as e:
        logger.warning("Error obteniendo stats de usuario: %s", e)
    return None


# ═══════════════════════════════════════════════════════════════
# CONFIGURACIONES Y ESTADO INTERNO (SETTINGS MIGRATION)
# ═══════════════════════════════════════════════════════════════

def get_setting(key: str) -> str | None:
    """Obtiene un valor de la tabla settings."""
    try:
        p = _ph()
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT value FROM settings WHERE key = {p}", (key,))
            r = cur.fetchone()
            return r[0] if r else None
    except Exception as e:
        logger.warning("Error leyendo setting %s: %s", key, e)
    return None

def set_setting(key: str, value: str) -> None:
    """Guarda (upsert) un valor en la tabla settings."""
    try:
        p = _ph()
        with get_conn() as conn:
            cur = conn.cursor()
            if _is_postgres():
                cur.execute(
                    f"INSERT INTO settings (key, value) VALUES ({p}, {p}) "
                    f"ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value",
                    (key, value)
                )
            else:
                cur.execute(
                    "INSERT INTO settings (key, value) VALUES (?, ?) "
                    "ON CONFLICT (key) DO UPDATE SET value = excluded.value",
                    (key, value)
                )
            conn.commit()
    except Exception as e:
        logger.warning("Error guardando setting %s: %s", key, e)
