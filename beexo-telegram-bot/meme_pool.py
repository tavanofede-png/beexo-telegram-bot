"""
Sistema de pool de memes con rotación automática.

Flujo:
  1. Al inicio, carga el pool desde `memes_pool.json`
  2. Cuando se pide un meme, elige uno al azar, lo marca como usado
  3. Elimina el meme usado del pool y borra el archivo PNG
  4. Genera un reemplazo vía Gemini (nuevo texto) + generate_memes (nueva imagen)
  5. Agrega el meme nuevo al pool

Si el pool se vacía, lo repuebla desde MEMES_DATA original.
"""

import json
import os
import random
import logging
from typing import Optional

logger = logging.getLogger("beexo.meme_pool")

_dir = os.path.dirname(os.path.abspath(__file__))
POOL_PATH = os.path.join(_dir, "memes_pool.json")
MEMES_DIR = os.path.join(_dir, "memes")


# ═══════════════════════════════════════════════════════════════
# POOL CRUD
# ═══════════════════════════════════════════════════════════════

def _load_pool() -> list[dict]:
    """Carga el pool actual desde JSON."""
    if not os.path.exists(POOL_PATH):
        return []
    try:
        with open(POOL_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("Error leyendo pool: %s, recreando...", e)
        return []


def _save_pool(pool: list[dict]) -> None:
    """Guarda el pool a JSON de forma atómica."""
    tmp = POOL_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(pool, f, ensure_ascii=False, indent=2)
    os.replace(tmp, POOL_PATH)


def init_pool(force: bool = False) -> int:
    """
    Inicializa el pool desde MEMES_DATA si no existe o está vacío.
    Retorna la cantidad de memes en el pool.
    """
    pool = _load_pool()
    if pool and not force:
        logger.info("🎭 Pool existente con %d memes", len(pool))
        return len(pool)

    from memes_data import MEMES_DATA
    pool = []
    for i, m in enumerate(MEMES_DATA):
        pool.append({
            "id": i + 1,
            "file": m["file"],
            "top": m["top"],
            "bottom": m["bottom"],
            "grad_top": m.get("grad_top", "#0a0a1a"),
            "grad_bottom": m.get("grad_bottom", "#1a1a3a"),
            "accent": m.get("accent", "#4ecdc4"),
            "sep": m.get("sep", "line"),
            "icon": m.get("icon", ""),
            "used": False,
        })
    _save_pool(pool)
    logger.info("🎭 Pool inicializado con %d memes", len(pool))
    return len(pool)


def pool_size() -> int:
    """Retorna la cantidad de memes disponibles (no usados) en el pool."""
    pool = _load_pool()
    return sum(1 for m in pool if not m.get("used", False))


def pick_meme() -> Optional[dict]:
    """
    Elige un meme al azar del pool, lo marca como usado.
    Retorna el meme dict o None si el pool está vacío.
    """
    pool = _load_pool()
    available = [m for m in pool if not m.get("used", False)]

    if not available:
        # Pool vacío: re-inicializar desde datos originales
        logger.warning("🎭 Pool vacío, re-inicializando...")
        init_pool(force=True)
        pool = _load_pool()
        available = [m for m in pool if not m.get("used", False)]
        if not available:
            return None

    meme = random.choice(available)
    meme["used"] = True
    _save_pool(pool)
    return meme


def remove_meme(meme_id: int) -> bool:
    """
    Elimina un meme del pool por su ID y borra el archivo PNG.
    Retorna True si se encontró y eliminó.
    """
    pool = _load_pool()
    new_pool: list[dict] = []
    removed: Optional[dict] = None
    for m in pool:
        if m.get("id") == meme_id:
            removed = m
        else:
            new_pool.append(m)

    if removed is None:
        return False

    _save_pool(new_pool)

    # Borrar archivo de imagen
    file_name: str = removed["file"]
    img_path = os.path.join(MEMES_DIR, file_name)
    if os.path.exists(img_path):
        try:
            os.remove(img_path)
            logger.info("🗑️ Meme eliminado: %s", file_name)
        except OSError as e:
            logger.warning("Error borrando %s: %s", img_path, e)

    return True


def add_meme(top: str, bottom: str, accent: str = "#4ecdc4",
             grad_top: str = "#0a0a1a", grad_bottom: str = "#1a1a3a",
             sep: str = "line", icon: str = "") -> dict:
    """
    Agrega un meme nuevo al pool y genera su imagen.
    Retorna el dict del meme creado.
    """
    pool = _load_pool()

    # Calcular nuevo ID
    max_id = max((m.get("id", 0) for m in pool), default=0)
    new_id = max_id + 1
    filename = f"meme_{new_id:04d}.png"

    meme = {
        "id": new_id,
        "file": filename,
        "top": top,
        "bottom": bottom,
        "grad_top": grad_top,
        "grad_bottom": grad_bottom,
        "accent": accent,
        "sep": sep,
        "icon": icon,
        "used": False,
    }

    # Generar la imagen
    try:
        from generate_memes import create_meme
        create_meme(
            filename=filename,
            top_text=top,
            bottom_text=bottom,
            grad_top=grad_top,
            grad_bottom=grad_bottom,
            accent=accent,
            sep_style=sep,
            icon_text=icon,
        )
        logger.info("🎨 Nuevo meme generado: %s", filename)
    except Exception as e:
        logger.warning("Error generando meme %s: %s", filename, e)

    pool.append(meme)
    _save_pool(pool)
    return meme


# ═══════════════════════════════════════════════════════════════
# GENERACIÓN DE MEMES NUEVOS VÍA GEMINI
# ═══════════════════════════════════════════════════════════════

# Categorías y estilos visuales para memes nuevos
CATEGORIES = [
    {"name": "dip", "accent": "#e94560", "grad_top": "#1a0a2e", "grad_bottom": "#3d0a4e", "icon": "DIP"},
    {"name": "security", "accent": "#79f7ff", "grad_top": "#050818", "grad_bottom": "#0d1a40", "icon": "🔐"},
    {"name": "hodl", "accent": "#03dac6", "grad_top": "#0a1a20", "grad_bottom": "#0a3a40", "icon": "HODL"},
    {"name": "scam", "accent": "#ff6b6b", "grad_top": "#1a0a10", "grad_bottom": "#3a1a20", "icon": "⚠️"},
    {"name": "fomo", "accent": "#4ecdc4", "grad_top": "#0a2020", "grad_bottom": "#1a4a4a", "icon": "FOMO"},
    {"name": "gas_fees", "accent": "#e5b8f4", "grad_top": "#200020", "grad_bottom": "#4a004a", "icon": "GAS"},
    {"name": "portfolio", "accent": "#f7dc6f", "grad_top": "#141a0a", "grad_bottom": "#2a3a1a", "icon": "📊"},
    {"name": "trading", "accent": "#bb86fc", "grad_top": "#1a0040", "grad_bottom": "#3a0080", "icon": "📈"},
    {"name": "family", "accent": "#79f7ff", "grad_top": "#081020", "grad_bottom": "#102040", "icon": "👨‍👩‍👦"},
    {"name": "bull_bear", "accent": "#ffc947", "grad_top": "#1a1000", "grad_bottom": "#3a2a00", "icon": "🐂"},
    {"name": "beexo", "accent": "#e94560", "grad_top": "#0a1818", "grad_bottom": "#1a3030", "icon": "🐝"},
]

MEME_GENERATION_PROMPT = """Generá un meme para un grupo cripto de Telegram en español argentino (usá 'vos').
Categoría: {category}

El meme tiene texto arriba (observación/setup) y texto abajo (remate gracioso).
Debe ser gracioso, relatable para la comunidad cripto, y no ofensivo.
Máximo 12 palabras arriba y 15 abajo.

Respondé SOLO con este formato JSON, sin markdown:
{{"top": "texto arriba", "bottom": "texto abajo"}}

Ejemplos de humor cripto:
- top: "Compre el dip 7 veces esta semana" / bottom: "Ya no tengo plata ni para el colectivo"
- top: "Mi novia: o el portfolio o yo" / bottom: "La extraño a veces"
- top: "Password: Bitcoin123" / bottom: "Hacker: Gracias capo ni me esforcé"

NO repitas estos ejemplos, creá uno nuevo y original."""


async def generate_replacement_meme() -> Optional[dict]:
    """
    Genera un meme completamente nuevo usando Gemini para el texto
    y Pillow para la imagen. Retorna el meme dict o None si falla.
    """
    try:
        from google import genai
        from config import GEMINI_API_KEY, GEMINI_MODEL

        if not GEMINI_API_KEY:
            logger.warning("No hay GEMINI_API_KEY para generar memes nuevos")
            return None

        client = genai.Client(api_key=GEMINI_API_KEY)
        category = random.choice(CATEGORIES)

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=MEME_GENERATION_PROMPT.format(category=category["name"]),
            config={
                "temperature": 0.9,
                "max_output_tokens": 150,
            },
        )

        text = response.text.strip() if response and response.text else ""
        if not text:
            logger.warning("Gemini devolvió respuesta vacía para meme")
            return None

        # Parsear JSON de la respuesta
        # Limpiar posible markdown wrapping
        if text.startswith("```"):
            text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()

        data = json.loads(text)
        top = data.get("top", "").strip()
        bottom = data.get("bottom", "").strip()

        if not top or not bottom:
            logger.warning("Gemini devolvió meme vacío: %s", text)
            return None

        meme = add_meme(
            top=top,
            bottom=bottom,
            accent=category["accent"],
            grad_top=category["grad_top"],
            grad_bottom=category["grad_bottom"],
            sep=random.choice(["line", "dots", "arrow"]),
            icon=category["icon"],
        )
        logger.info("✨ Meme reemplazo generado por Gemini: %s", meme["file"])
        return meme

    except json.JSONDecodeError as e:
        logger.warning("Error parseando respuesta de Gemini para meme: %s", e)
        return None
    except Exception as e:
        logger.warning("Error generando meme de reemplazo: %s", e)
        return None


async def use_and_replace(meme: dict) -> None:
    """
    Elimina el meme usado del pool y genera un reemplazo.
    Se ejecuta de forma asincrónica después de enviar el meme.
    """
    meme_id = meme.get("id")
    if meme_id:
        remove_meme(meme_id)

    # Intentar generar reemplazo vía Gemini
    replacement = await generate_replacement_meme()
    if replacement:
        logger.info("🔄 Meme %d reemplazado por meme %d", meme_id, replacement["id"])
    else:
        # Fallback: si falla Gemini, no pasa nada — el pool se repuebla
        # desde MEMES_DATA cuando se vacía
        logger.info("🔄 No se pudo generar reemplazo, pool tiene %d memes", pool_size())
