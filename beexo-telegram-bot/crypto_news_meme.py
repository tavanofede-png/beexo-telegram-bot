"""
Genera memes de alta calidad basados en noticias cripto reales.

Pipeline:
  1. Busca noticias cripto recientes (DuckDuckGo) + datos de mercado (CoinGecko)
  2. Gemini escribe el meme (top/bottom text + prompt de imagen)
  3. Gemini genera la imagen del meme (gemini-2.5-flash-image)
  4. Pillow compone el meme final (texto legible + branding Beexo)
"""

import io
import os
import random
import logging
from datetime import datetime

import httpx
import re
import asyncio
import json
from PIL import Image, ImageDraw, ImageFont

from duckduckgo_search import DDGS
from google import genai
from generate_memes import create_meme

from config import GEMINI_API_KEY, GEMINI_IMAGE_MODEL, GEMINI_MODEL, TZ

logger = logging.getLogger("beexo.meme_ai")

MEMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memes")
os.makedirs(MEMES_DIR, exist_ok=True)

COINGECKO_BASE = "https://api.coingecko.com/api/v3"


# ═══════════════════════════════════════════════════════════════
# 1. FETCH CONTEXT (noticias + mercado)
# ═══════════════════════════════════════════════════════════════

async def fetch_crypto_context() -> dict:
    """
    Reune contexto para generar un meme:
    - 5 noticias cripto recientes (DuckDuckGo)
    - Top movers del mercado (CoinGecko)
    - Monedas trending (CoinGecko)
    """
    context: dict = {"news": [], "movers": [], "trending": []}

    # ── Noticias vía DuckDuckGo ──
    try:
        if DDGS:
            queries = [
                "crypto bitcoin ethereum noticias",
                "criptomonedas blockchain web3 novedades",
            ]
            query = random.choice(queries)
            with DDGS() as ddgs:
                results = list(ddgs.news(query, region="wt-wt", max_results=8))
            for r in results[:5]:
                context["news"].append({
                    "title": r.get("title", ""),
                    "body": (r.get("body") or "")[:200],
                    "source": r.get("source", ""),
                })
    except Exception as e:
        logger.warning("⚠️ Error buscando noticias para meme: %s", e)

    # ── Top movers vía CoinGecko ──
    async with httpx.AsyncClient(timeout=15) as client:
        try:
            resp = await client.get(
                f"{COINGECKO_BASE}/coins/markets",
                params={
                    "vs_currency": "usd",
                    "order": "market_cap_desc",
                    "per_page": 25,
                    "page": 1,
                    "price_change_percentage": "24h",
                },
            )
            if resp.status_code == 200:
                for coin in resp.json():
                    change = coin.get("price_change_percentage_24h") or 0
                    if abs(change) >= 2:
                        context["movers"].append({
                            "symbol": coin["symbol"].upper(),
                            "name": coin["name"],
                            "price": coin["current_price"],
                            "change_24h": round(change, 1),
                        })
        except Exception as e:
            logger.warning("⚠️ Error fetching market data: %s", e)

        # ── Trending ──
        try:
            resp = await client.get(f"{COINGECKO_BASE}/search/trending")
            if resp.status_code == 200:
                for item in resp.json().get("coins", [])[:3]:
                    c = item.get("item", {})
                    context["trending"].append({
                        "name": c.get("name", ""),
                        "symbol": c.get("symbol", "").upper(),
                    })
        except Exception as e:
            logger.warning("⚠️ Error fetching trending: %s", e)

    return context


# ═══════════════════════════════════════════════════════════════
# 2. GEMINI: GENERAR TEXTO DEL MEME
# ═══════════════════════════════════════════════════════════════

MEME_WRITER_PROMPT = """Sos un experto en memes de crypto para una comunidad de Telegram en español argentino (usá "vos").

Tu trabajo: crear un meme VIRAL, GRACIOSO y RELEVANTE basado en las noticias y datos cripto que te paso.

REGLAS:
1. El meme tiene "top" (setup/observación) y "bottom" (remate gracioso/punchline)
2. MÁXIMO 12 palabras en top, MÁXIMO 15 en bottom
3. El humor debe ser RELATABLE para la comunidad cripto argentina
4. NO seas genérico — referenciá noticias o datos específicos cuando puedas
5. Estilos de humor que funcionan:
   - Autodeprecación del trader ("compré el ATH")
   - FOMO/HODL culture
   - Comparaciones con la vida cotidiana
   - Reacciones exageradas ante movimientos del mercado
   - Regulaciones y sus efectos
   - Hacks/scams y la paranoia que generan
6. NO uses insultos ni contenido ofensivo
7. El image_prompt debe describir UNA ESCENA VISUAL concreta para la imagen del meme
   - Describí personajes, expresiones, entorno, colores, estilo
   - El estilo debe ser "cartoon/meme illustration" moderno y colorido
   - NO incluyas texto en la imagen — el texto va superpuesto después
   - Ejemplo: "A cartoon person in pajamas looking at phone screen with a shocked face at 3am, green candlestick chart glowing on screen, dark bedroom, dramatic lighting"

CONTEXTO ACTUAL:

{context}

Respondé SOLO con este formato de texto plano (sin markdown, sin JSON):
TOP: [texto de arriba]
BOTTOM: [texto de abajo]
PROMPT: [descripción de imagen en inglés]"""


async def generate_meme_content(context: dict) -> dict | None:
    """
    Usa Gemini para escribir el meme (top, bottom, image_prompt)
    basado en el contexto de noticias y mercado.
    """
    if not GEMINI_API_KEY:
        logger.warning("❌ No hay GEMINI_API_KEY para generar memes")
        return None

    # Formatear contexto
    lines = []
    if context.get("news"):
        lines.append("📰 NOTICIAS RECIENTES:")
        for n in context["news"]:
            lines.append(f"  • {n['title']}")
            if n["body"]:
                lines.append(f"    {n['body']}")

    if context.get("movers"):
        lines.append("\n📊 MOVIMIENTOS DEL MERCADO (24h):")
        for m in context["movers"][:5]:
            sign = "+" if m["change_24h"] >= 0 else ""
            lines.append(f"  • {m['symbol']} ({m['name']}): {sign}{m['change_24h']}%")

    if context.get("trending"):
        lines.append("\n🔥 TENDENCIA:")
        t_str = ", ".join([f"{t['symbol']}" for t in context["trending"]])
        lines.append(f"  {t_str}")

    if not lines:
        lines.append("No hay datos específicos — generá un meme genérico de crypto culture")

    full_context = "\n".join(lines)
    prompt = MEME_WRITER_PROMPT.format(context=full_context)

    try:
        text = None
        # Retry loop for 503 errors
        for attempt in range(1, 4):
            try:
                client = genai.Client(api_key=GEMINI_API_KEY)
                response = client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt,
                    config={
                        "temperature": 0.9,
                        "max_output_tokens": 1000,
                        "safety_settings": [
                            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                        ]
                    },
                )

                text = (response.text or "").strip()
                if not text:
                    logger.warning("Gemini devolvió respuesta vacía para meme (intento %d)", attempt)
                    if attempt < 3:
                        await asyncio.sleep(2 * attempt)
                        continue
                    return None

                logger.info("Gemini raw response length: %d", len(text))
                if response.candidates:
                     if hasattr(response.candidates[0], "finish_reason"):
                        logger.info("Finish reason: %s", response.candidates[0].finish_reason)
                break

            except Exception as e:
                logger.warning("⚠️ Error Gemini (intento %d): %s", attempt, e)
                if "503" in str(e) or "429" in str(e):
                    if attempt < 3:
                        await asyncio.sleep(2 * attempt)
                        continue
                else:
                    return None

        if not text:
            return None

        # Parsear formato TOP/BOTTOM/PROMPT
        top_match = re.search(r"TOP:\s*(.*)", text, re.IGNORECASE)
        bottom_match = re.search(r"BOTTOM:\s*(.*)", text, re.IGNORECASE)
        prompt_match = re.search(r"PROMPT:\s*(.*)", text, re.IGNORECASE)

        top = top_match.group(1).strip() if top_match else ""
        bottom = bottom_match.group(1).strip() if bottom_match else ""
        image_prompt = prompt_match.group(1).strip() if prompt_match else ""

        # Limpieza básica
        if not top and not bottom:
            logger.warning("❌ No se encontró TOP/BOTTOM en la respuesta: %s", text[:200])
            return None

        return {
            "top": top,
            "bottom": bottom,
            "image_prompt": image_prompt or f"funny meme about crypto market, {top} {bottom}"
        }

    except Exception as e:
        logger.warning("⚠️ Error generando contenido de meme: %s", e)
        return None


# ═══════════════════════════════════════════════════════════════
# 3. GEMINI: GENERAR IMAGEN DEL MEME
# ═══════════════════════════════════════════════════════════════

async def generate_meme_image(image_prompt: str) -> bytes | None:
    """
    Genera una imagen para el meme usando Gemini gemini-2.5-flash-image.
    Retorna los bytes PNG o None si falla.
    """
    if not GEMINI_API_KEY or not image_prompt:
        return None

    full_prompt = (
        f"Generate a high-quality meme illustration. Style: colorful modern cartoon, "
        f"vibrant colors, expressive characters, clean composition. "
        f"DO NOT include any text, words, or letters in the image. "
        f"Scene: {image_prompt}"
    )

    try:
        # Retry loop for 503 errors
        for attempt in range(1, 4):
            try:
                client = genai.Client(api_key=GEMINI_API_KEY)
                response = client.models.generate_content(
                    model=GEMINI_IMAGE_MODEL,
                    contents=full_prompt,
                    config={
                        "response_modalities": ["IMAGE", "TEXT"],
                    },
                )

                # Extraer la imagen de la respuesta
                if response and response.candidates:
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, "inline_data") and part.inline_data is not None:
                            img = part.as_image()
                            buf = io.BytesIO()
                            img.save(buf, format="PNG")
                            logger.info("🎨 Imagen de meme generada por Gemini (%d bytes)", buf.tell())
                            return buf.getvalue()
                
                logger.warning("Gemini no devolvió imagen (intento %d)", attempt)
            
            except Exception as e:
                logger.warning("⚠️ Error Gemini Imagen (intento %d): %s", attempt, e)
                if "503" in str(e) or "429" in str(e):
                    if attempt < 3:
                        await asyncio.sleep(2 * attempt)
                        continue
                else:
                    return None
        
        return None

    except Exception as e:
        logger.warning("⚠️ Error generando imagen de meme: %s", e)
        return None


# ═══════════════════════════════════════════════════════════════
# 4. PILLOW: COMPONER MEME FINAL
# ═══════════════════════════════════════════════════════════════

def _get_font(size: int, bold: bool = True):
    """Carga una fuente con fallback a la default."""
    font_names = [
        "Impact", "arial", "arialbd", "DejaVuSans-Bold",
        "DejaVuSans", "FreeSansBold", "LiberationSans-Bold",
    ]
    if not bold:
        font_names = [f.replace("Bold", "").replace("bd", "") for f in font_names]

    for name in font_names:
        try:
            return ImageFont.truetype(name, size)
        except (IOError, OSError):
            try:
                return ImageFont.truetype(f"{name}.ttf", size)
            except (IOError, OSError):
                continue
    return ImageFont.load_default()


def _draw_text_with_stroke(
    draw: ImageDraw.ImageDraw,
    text: str,
    font,
    y_start: int,
    width: int,
    fill: str = "white",
    stroke_width: int = 4,
    stroke_fill: str = "black",
    max_chars: int = 28,
):
    """Dibuja texto con word-wrap y stroke para legibilidad."""
    words = text.split()
    lines_list: list[str] = []
    current = ""
    for w in words:
        test = f"{current} {w}".strip()
        if len(test) <= max_chars:
            current = test
        else:
            if current:
                lines_list.append(current)
            current = w
    if current:
        lines_list.append(current)

    y = y_start
    for line in lines_list:
        bb = draw.textbbox((0, 0), line, font=font)
        tw = bb[2] - bb[0]
        x = (width - tw) // 2
        draw.text(
            (x, y), line, font=font, fill=fill,
            stroke_width=stroke_width, stroke_fill=stroke_fill,
        )
        y += bb[3] - bb[1] + 8


def compose_meme(
    image_bytes: bytes,
    top_text: str,
    bottom_text: str,
    accent_color: str = "#4ecdc4",
) -> str:
    """
    Compone el meme final: imagen AI + texto superpuesto + branding.
    Retorna path al archivo PNG guardado.
    """
    # Abrir imagen base
    base = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    # Resize a dimensión estándar
    target_w, target_h = 800, 800
    base = base.resize((target_w, target_h), Image.LANCZOS)

    # Crear overlay de vignette para legibilidad del texto
    overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    # Vignette superior (para top text)
    for y in range(250):
        alpha = int(200 * (1 - y / 250) ** 1.5)
        od.line([(0, y), (target_w, y)], fill=(0, 0, 0, alpha))

    # Vignette inferior (para bottom text)
    for y in range(target_h - 250, target_h):
        alpha = int(200 * ((y - (target_h - 250)) / 250) ** 1.5)
        od.line([(0, y), (target_w, y)], fill=(0, 0, 0, alpha))

    img = Image.alpha_composite(base, overlay)
    draw = ImageDraw.Draw(img)

    # Barras de acento
    draw.rectangle([(0, 0), (target_w, 4)], fill=accent_color)
    draw.rectangle([(0, target_h - 4), (target_w, target_h)], fill=accent_color)

    # Texto superior
    top_font = _get_font(52)
    _draw_text_with_stroke(
        draw, top_text.upper(), top_font, 25, target_w,
        fill="white", stroke_width=5, stroke_fill="#000000", max_chars=24,
    )

    # Texto inferior
    bottom_font = _get_font(46)
    # Calcular posición Y dinámica para el bottom text
    words = bottom_text.split()
    num_lines = max(1, (len(" ".join(words)) // 24) + 1)
    bottom_y = target_h - 40 - (num_lines * 60)
    _draw_text_with_stroke(
        draw, bottom_text.upper(), bottom_font, bottom_y, target_w,
        fill=accent_color, stroke_width=4, stroke_fill="#000000", max_chars=26,
    )

    # Branding Beexo
    brand_font = _get_font(14, bold=False)
    draw.text(
        (target_w - 75, target_h - 22), "🐝 BEEXO",
        font=brand_font, fill=accent_color,
        stroke_width=2, stroke_fill="#000000",
    )

    # Guardar
    filename = f"meme_ai_{random.randint(1000, 9999)}.png"
    path = os.path.join(MEMES_DIR, filename)
    img.convert("RGB").save(path, "PNG", quality=95)
    logger.info("🎭 Meme compuesto guardado: %s", filename)
    return path


# ═══════════════════════════════════════════════════════════════
# 5. FALLBACK: MEME CON PILLOW (sistema anterior)
# ═══════════════════════════════════════════════════════════════

def _fallback_pillow_meme(top_text: str, bottom_text: str) -> str | None:
    """Genera un meme con el sistema Pillow existente como fallback."""
    try:
        filename = f"meme_fallback_{random.randint(1000, 9999)}.png"
        path = create_meme(
            filename=filename,
            top_text=top_text,
            bottom_text=bottom_text,
            grad_top="#0a0a2a",
            grad_bottom="#1a1a4a",
            accent="#4ecdc4",
            sep_style=random.choice(["line", "dots", "arrow"]),
            icon_text="🐝",
        )
        return path
    except Exception as e:
        logger.warning("⚠️ Fallback Pillow también falló: %s", e)
        return None


# ═══════════════════════════════════════════════════════════════
# ORQUESTADOR PRINCIPAL
# ═══════════════════════════════════════════════════════════════

ACCENT_COLORS = [
    "#4ecdc4", "#03dac6", "#bb86fc", "#e94560",
    "#ffc947", "#79f7ff", "#00ff88", "#f7dc6f",
]


async def generate_news_meme() -> tuple[str | None, str | None]:
    """
    Pipeline completo de generación de meme de alta calidad.
    Retorna (path_al_meme, caption) o (None, None) si falla.
    """
    # 1. Obtener contexto
    logger.info("📰 Buscando contexto para meme...")
    context = await fetch_crypto_context()

    # 2. Generar texto del meme con Gemini
    logger.info("✍️ Generando texto del meme con Gemini...")
    meme_content = await generate_meme_content(context)

    if not meme_content:
        logger.warning("❌ No se pudo generar contenido del meme")
        return None, None

    top_text = meme_content["top"]
    bottom_text = meme_content["bottom"]
    image_prompt = meme_content.get("image_prompt", "")

    # 3. Generar imagen con Gemini
    accent = random.choice(ACCENT_COLORS)
    path = None

    if image_prompt:
        logger.info("🎨 Generando imagen con Gemini...")
        image_bytes = await generate_meme_image(image_prompt)
        if image_bytes:
            try:
                path = compose_meme(image_bytes, top_text, bottom_text, accent)
            except Exception as e:
                logger.warning("⚠️ Error componiendo meme: %s", e)

    # 4. Fallback a Pillow si la imagen AI falló
    if not path:
        logger.info("🔄 Usando fallback Pillow para el meme...")
        path = _fallback_pillow_meme(top_text, bottom_text)

    if not path:
        return None, None

    # 5. Construir caption
    caption = (
        f"🐝 *{top_text}*\n"
        f"{bottom_text}\n\n"
    )

    return path, caption
