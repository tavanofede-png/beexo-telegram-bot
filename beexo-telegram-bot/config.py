"""
Configuración central de BeeXy — Beexo Telegram Bot.
Variables de entorno, constantes y timezone.
"""

import os
import logging
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

# ── Cargar .env ──
_script_dir = os.path.dirname(os.path.abspath(__file__))
_dotenv_path = os.path.join(_script_dir, ".env")
load_dotenv(_dotenv_path, override=True)

# ── Logging ──
logging.basicConfig(level=logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.WARNING)
logger = logging.getLogger("beexy")

# ── Telegram ──
TOKEN: str = os.environ["TELEGRAM_BOT_TOKEN"]

_raw_targets = os.environ.get("TARGET_CHAT_IDS") or os.environ.get("TARGET_CHAT_ID")
if not _raw_targets:
    raise RuntimeError("TARGET_CHAT_ID or TARGET_CHAT_IDS must be set in environment")
TARGET_CHAT_IDS: list[int] = [int(x.strip()) for x in str(_raw_targets).split(",") if x.strip()]

# ── Timezone ──
TZ = ZoneInfo(os.getenv("TZ", "America/Argentina/Buenos_Aires"))

# ── API Keys ──
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")  # fallback / legacy
HF_TOKEN: str = os.getenv("HF_TOKEN", "")
DATABASE_URL: str | None = os.getenv("DATABASE_URL")

# ── Rutas ──
MEMES_DIR: str = os.path.join(_script_dir, "memes")
DB_PATH: str = os.path.join(_script_dir, "beexy_history.db")

# ── Constantes ──
SCAM_ALERT_COOLDOWN_MIN: int = 5
GEMINI_MODEL: str = "gemini-2.0-flash"
GROQ_URL: str = "https://api.groq.com/openai/v1/chat/completions"  # legacy
GROQ_MODEL: str = "llama-3.3-70b-versatile"  # legacy
MAX_AI_HISTORY: int = 8

# ── Rate limiting ──


# ── Startup log (seguro, sin filtrar token) ──
logger.info("📁 .env cargado desde: %s", _dotenv_path)
logger.info("🔑 TOKEN configurado: %s…", TOKEN[:8])
logger.info("💬 TARGET_CHAT_IDS: %s", TARGET_CHAT_IDS)
logger.info("🌍 Timezone: %s", TZ)
logger.info("🤖 GEMINI_API_KEY: %s", "✅ configurada" if GEMINI_API_KEY else "❌ NO configurada")
