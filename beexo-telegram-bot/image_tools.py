"""
Módulo de imágenes para BeeXy.
- Búsqueda de imágenes vía DuckDuckGo (gratis, sin API key)
- Generación de imágenes vía Hugging Face Inference API (100% gratis)
  Modelo: FLUX.1-schnell (Black Forest Labs) - alta calidad
- Detección inteligente: personas reales → búsqueda, creativo → generación
"""

import os
import re
import random
import httpx
from duckduckgo_search import DDGS


def _get_hf_token() -> str:
    return os.getenv("HF_TOKEN", "")


# ═══════════════════════════════════════════════════════════════
# DETECCIÓN DE PERSONAS REALES (redirige a búsqueda)
# ═══════════════════════════════════════════════════════════════

REAL_PEOPLE = [
    # Fútbol
    "messi", "cr7", "cristiano", "ronaldo", "neymar", "mbappé", "mbappe",
    "haaland", "maradona", "pelé", "pele", "zidane", "beckham", "modric",
    "benzema", "lewandowski", "salah", "de bruyne", "vinicius", "bellingham",
    "di maria", "di maría", "scaloni", "guardiola", "mourinho", "klopp",
    "riquelme", "boca", "river",
    # Música
    "taylor swift", "bad bunny", "drake", "beyoncé", "beyonce",
    "eminem", "shakira", "daddy yankee", "peso pluma", "karol g",
    "bizarrap", "duki", "tini", "maria becerra", "wos",
    # Tech / Negocios
    "elon musk", "jeff bezos", "mark zuckerberg", "bill gates",
    "steve jobs", "sam altman", "satoshi", "vitalik", "cz",
    # Política / Figuras públicas
    "trump", "biden", "milei", "obama", "putin", "zelensky",
    "papa francisco", "pope francis",
    # Actores / Celebridades
    "dicaprio", "brad pitt", "tom cruise", "keanu reeves",
    "scarlett johansson", "margot robbie", "timothée chalamet",
    "the rock", "dwayne johnson",
]


def _mentions_real_person(text: str) -> bool:
    """Detecta si el texto menciona una persona real."""
    text_lower = text.lower()
    for person in REAL_PEOPLE:
        if person in text_lower:
            return True
    return False


# ═══════════════════════════════════════════════════════════════
# BÚSQUEDA DE IMÁGENES (DuckDuckGo)
# ═══════════════════════════════════════════════════════════════

async def _optimize_search_query(query: str) -> str:
    """Usa Groq para crear un query de búsqueda óptimo en inglés."""
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return query
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You optimize image search queries. RULES:\n"
                                "1. OUTPUT ONLY the search query, nothing else.\n"
                                "2. Translate to English for wider results.\n"
                                "3. Keep it short: 2-6 keywords max.\n"
                                "4. Add 'HD' or 'high quality' if appropriate.\n"
                                "5. For people: use their full real name + what the user wants.\n"
                                "6. For memes/funny: keep the original intent.\n"
                                "7. Remove filler words, keep only meaningful terms.\n"
                                "Examples:\n"
                                "- 'cr7 con la camiseta del real madrid' → 'Cristiano Ronaldo Real Madrid jersey HD'\n"
                                "- 'messi celebrando gol' → 'Lionel Messi goal celebration HD'\n"
                                "- 'bitcoin logo' → 'Bitcoin logo HD transparent'\n"
                                "- 'gato gracioso' → 'funny cat meme HD'\n"
                            ),
                        },
                        {"role": "user", "content": query},
                    ],
                    "max_tokens": 60,
                    "temperature": 0.3,
                },
            )
        if resp.status_code == 200:
            optimized = resp.json()["choices"][0]["message"]["content"].strip()
            optimized = optimized.strip('"\'')
            if optimized and len(optimized) > 2:
                return optimized
    except Exception:
        pass
    return query


async def search_image(query: str, max_results: int = 15) -> tuple[bytes, str] | None:
    """
    Busca imágenes en DuckDuckGo con query optimizado por IA.
    Prioriza imágenes de buena calidad y tamaño.
    Retorna (image_bytes, title) o None si no encuentra nada.
    """
    # Optimizar query con Groq para mejores resultados
    optimized_query = await _optimize_search_query(query)

    # Buscar con query optimizado + fallback con original
    all_results = []
    for q in [optimized_query, query]:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.images(
                    q,
                    region="wt-wt",
                    safesearch="moderate",
                    size="Large",
                    max_results=max_results,
                ))
                all_results.extend(results)
        except Exception:
            continue

    if not all_results:
        return None

    # Deduplicar por URL
    seen_urls = set()
    unique = []
    for r in all_results:
        url = r.get("image", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique.append(r)

    # Priorizar: primeros resultados del query optimizado son más relevantes
    # Tomar los primeros 10 sin mezclar para mantener relevancia
    candidates = unique[:12]

    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        for r in candidates:
            url = r.get("image", "")
            title = r.get("title", "Imagen encontrada")
            if not url:
                continue
            try:
                resp = await client.get(url)
                if resp.status_code != 200:
                    continue
                content = resp.content
                # Mínimo 10KB para asegurar calidad decente
                if len(content) < 10000:
                    continue
                ct = resp.headers.get("content-type", "")
                is_img = (
                    "image" in ct
                    or url.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))
                )
                if not is_img:
                    continue
                # Límite Telegram: 10 MB para fotos
                if len(content) > 10 * 1024 * 1024:
                    continue
                return (content, title)
            except Exception:
                continue

    return None


# ═══════════════════════════════════════════════════════════════
# GENERACIÓN DE IMÁGENES - Multi-proveedor (100% gratis)
# 1. Pollinations.ai con FLUX (gratis, sin API key)
# 2. Hugging Face Inference (backup, necesita token con permisos)
# ═══════════════════════════════════════════════════════════════

POLLINATIONS_URL = "https://image.pollinations.ai/prompt/{prompt}?model=flux&width=1024&height=1024&enhance=true&nologo=true&seed={seed}"

HF_ROUTER_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"


async def _enhance_prompt(prompt: str) -> str:
    """Usa Groq para convertir el prompt a inglés optimizado para FLUX."""
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return prompt
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are an expert prompt engineer for FLUX AI image generation.\n\n"
                                "RULES:\n"
                                "1. OUTPUT ONLY the optimized English prompt. Nothing else.\n"
                                "2. Be extremely descriptive: subject, action, environment, "
                                "lighting (golden hour, studio light, neon, etc.), "
                                "camera angle (close-up, wide shot, bird's eye), "
                                "art style, mood, color palette, textures.\n"
                                "3. Add quality tags: 'masterpiece, best quality, ultra detailed, "
                                "sharp focus, high resolution, 8K'.\n"
                                "4. For photorealistic: 'photorealistic, DSLR photograph, "
                                "natural lighting, bokeh, depth of field, film grain'.\n"
                                "5. For artistic: specify style explicitly "
                                "(oil painting, watercolor, anime, cyberpunk, concept art, "
                                "pixel art, etc.).\n"
                                "6. For characters/people: describe pose, expression, clothing, "
                                "hair, skin tone, body type in detail.\n"
                                "7. For landscapes: describe sky, vegetation, water, structures, "
                                "time of day, weather, atmosphere.\n"
                                "8. Max 120 words. Every word must add visual information.\n"
                                "9. NEVER include text/words TO APPEAR in the image unless "
                                "the user specifically requests it.\n"
                                "10. Do NOT mention real people's names - instead describe "
                                "their distinctive visual features if the user asks for someone.\n"
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    "max_tokens": 250,
                    "temperature": 0.6,
                },
            )
        if resp.status_code == 200:
            enhanced = resp.json()["choices"][0]["message"]["content"].strip()
            enhanced = enhanced.strip('"\'')
            if enhanced:
                return enhanced
    except Exception:
        pass
    return prompt


async def _generate_pollinations(enhanced_prompt: str) -> bytes | None:
    """Genera imagen con Pollinations.ai + modelo FLUX (100% gratis, sin key)."""
    import urllib.parse
    encoded = urllib.parse.quote(enhanced_prompt, safe='')
    seed = random.randint(1, 999999)
    url = POLLINATIONS_URL.format(prompt=encoded, seed=seed)

    try:
        async with httpx.AsyncClient(timeout=120, follow_redirects=True) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                content = resp.content
                ct = resp.headers.get("content-type", "")
                if ("image" in ct or len(content) > 10000):
                    return content
    except Exception:
        pass

    # Reintento con seed diferente
    try:
        seed2 = random.randint(1, 999999)
        url2 = POLLINATIONS_URL.format(prompt=encoded, seed=seed2)
        async with httpx.AsyncClient(timeout=120, follow_redirects=True) as client:
            resp = await client.get(url2)
            if resp.status_code == 200 and len(resp.content) > 5000:
                return resp.content
    except Exception:
        pass

    return None


async def _generate_hf(enhanced_prompt: str) -> bytes | None:
    """Genera imagen con Hugging Face Inference API (FLUX.1-schnell). Backup."""
    hf_token = _get_hf_token()
    if not hf_token:
        return None

    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "inputs": enhanced_prompt,
        "parameters": {
            "seed": random.randint(1, 999999),
        },
    }

    try:
        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(HF_ROUTER_URL, headers=headers, json=payload)

            # Si el modelo se está cargando, esperar y reintentar
            if resp.status_code == 503:
                import asyncio
                wait_time = 20
                try:
                    data = resp.json()
                    wait_time = min(data.get("estimated_time", 20), 60)
                except Exception:
                    pass
                await asyncio.sleep(wait_time)
                resp = await client.post(HF_ROUTER_URL, headers=headers, json=payload)

            if resp.status_code == 200:
                content = resp.content
                ct = resp.headers.get("content-type", "")
                if "image" in ct and len(content) > 5000:
                    return content
    except Exception:
        pass
    return None


async def generate_image(prompt: str) -> tuple[bytes, str] | None:
    """
    Genera una imagen con FLUX vía múltiples proveedores (gratis).
    Si menciona persona real → busca foto real en vez de generar.
    Retorna (image_bytes, prompt_usado) o None.
    """
    # Si menciona persona real, redirigir a búsqueda
    if _mentions_real_person(prompt):
        result = await search_image(prompt)
        if result:
            return result

    # Mejorar prompt con Groq
    enhanced = await _enhance_prompt(prompt)

    # 1. Intentar Pollinations (principal, gratis sin key)
    img_bytes = await _generate_pollinations(enhanced)
    if img_bytes:
        return (img_bytes, enhanced)

    # 2. Fallback: HF (si el token tiene permisos)
    img_bytes = await _generate_hf(enhanced)
    if img_bytes:
        return (img_bytes, enhanced)

    # 3. Último recurso: buscar imagen similar en la web
    result = await search_image(prompt)
    if result:
        return result

    return None


# ═══════════════════════════════════════════════════════════════
# DETECCIÓN DE PEDIDOS DE IMAGEN EN LENGUAJE NATURAL
# Sistema inteligente con regex + combinaciones de palabras
# ═══════════════════════════════════════════════════════════════

# ── Verbos que indican GENERAR (crear algo nuevo) ──
# Estos son específicos de creación visual, pueden ir sin sustantivo de imagen
_GEN_VERBS = (
    r"(?:genera|generá|generame|genérame|"
    r"dibuja|dibujá|dibujame|dibujáme|"
    r"diseña|diseñá|diseñame|diseñáme|"
    r"ilustra|ilustrá|ilustrame|"
    r"renderizá|renderiza|renderizame)"
)

# ── Verbos genéricos que SOLO indican imagen si van con sustantivo de imagen ──
_GENERIC_VERBS = (
    r"(?:busca|buscá|buscame|búscame|"
    r"mostra|mostrá|mostrame|mostráme|"
    r"enseña|enseñá|enseñame|"
    r"pasa|pasá|pasame|pasáme|"
    r"manda|mandá|mandame|mandáme|"
    r"trae|traé|traeme|traéme|"
    r"consegui|conseguí|conseguime|"
    r"encontra|encontrá|encontrame|"
    r"hacé|hace|haceme|hacéme|"
    r"crea|creá|creame|créame|"
    r"arma|armá|armame|"
    r"inventá|inventame|inventa|"
    r"imaginá|imaginame|imagina|"
    r"pon[eé]|poneme|ponéme|poné)"
)

# ── Sustantivos de imagen ──
_IMG_NOUNS = (
    r"(?:imagen|imágen|foto|fotografía|fotografia|"
    r"dibujo|ilustración|ilustracion|"
    r"pic|picture|"
    r"arte|diseño|wallpaper|fondo)"
)

# ── Patrones compilados ──

# 1. Generación directa: "dibujame X", "generame X" (verbos específicos, NO necesitan sustantivo)
_RE_GEN_DIRECT = re.compile(
    _GEN_VERBS + r"\s+(?:una?\s+)?(?:" + _IMG_NOUNS + r"\s+(?:de\s+|sobre\s+|con\s+)?)?(.+)",
    re.IGNORECASE,
)

# 2. Verbo genérico + sustantivo de imagen OBLIGATORIO: "buscame una FOTO de X", "haceme una IMAGEN de X"
_RE_GENERIC_WITH_IMG = re.compile(
    _GENERIC_VERBS + r"\s+(?:una?\s+)?" + _IMG_NOUNS + r"\s+(?:de\s+|sobre\s+|con\s+)?(.+)",
    re.IGNORECASE,
)

# 3. "quiero/necesito + una imagen/foto de [tema]" (requiere sustantivo de imagen)
_RE_WANT_IMG = re.compile(
    r"(?:quiero|necesito|me (?:gustaría|gustaria)|puedo ver|podés? (?:hacer|generar|buscar|crear|mostrar))"
    r"\s+(?:una?\s+)?" + _IMG_NOUNS + r"\s+(?:de\s+|sobre\s+|con\s+)?(.+)",
    re.IGNORECASE,
)

# 4. "una imagen de [tema]" / "foto de [tema]" standalone (sustantivo de imagen obligatorio)
_RE_STANDALONE_IMG = re.compile(
    r"(?:^|\s)(?:una?\s+)?" + _IMG_NOUNS + r"\s+(?:de\s+|sobre\s+|con\s+)(.+)",
    re.IGNORECASE,
)

# ── Verbos de generación para detección (qué acción asociar) ──
# SOLO estos verbos gatillan "generate". Son específicos de creación visual.
_GEN_VERB_SET = {
    "genera", "generá", "generame", "genérame",
    "dibuja", "dibujá", "dibujame", "dibujáme",
    "diseña", "diseñá", "diseñame", "diseñáme",
    "ilustra", "ilustrá", "ilustrame",
    "renderizá", "renderiza", "renderizame",
}


def detect_image_request(text: str) -> tuple[str, str] | None:
    """
    Detecta si el texto pide una imagen con detección inteligente.
    Retorna ("generate", topic) o ("search", topic) o None.
    
    Regla clave:
    - "generate" SOLO con verbos de creación visual: genera, dibuja, diseña, ilustra, renderiza
    - "search" para TODO lo demás: busca, mostra, haceme, quiero, foto de X, etc.
    """
    text_clean = text.strip()
    if len(text_clean) < 4:
        return None

    # 1. Verbos específicos de creación visual → GENERATE
    #    "dibujame X", "generame X", "renderizá X"
    m = _RE_GEN_DIRECT.search(text_clean)
    if m:
        topic = _clean_topic(m.group(1))
        if topic:
            return ("generate", topic)

    # 2. Verbo genérico + sustantivo de imagen → SEARCH
    #    "buscame una foto de X", "haceme una imagen de X", "mandame una foto de X"
    m = _RE_GENERIC_WITH_IMG.search(text_clean)
    if m:
        topic = _clean_topic(m.group(1))
        if topic:
            return ("search", topic)

    # 3. "quiero una imagen/foto de X" → SEARCH
    m = _RE_WANT_IMG.search(text_clean)
    if m:
        topic = _clean_topic(m.group(1))
        if topic:
            return ("search", topic)

    # 4. "una imagen de X" / "foto de X" standalone → SEARCH
    m = _RE_STANDALONE_IMG.search(text_clean)
    if m:
        topic = _clean_topic(m.group(1))
        if topic:
            return ("search", topic)

    return None


def _clean_topic(raw: str) -> str:
    """Limpia y normaliza el tema extraído."""
    topic = raw.strip()

    # Remover fillers al inicio
    filler_start = [
        "de", "sobre", "con", "un", "una", "el", "la", "los", "las",
        "unos", "unas", "del", "al",
        "beexy", "por favor", "porfa", "porfavor", "please", "pls",
        "que sea", "que tenga", "tipo",
    ]
    words = topic.split()
    while words and words[0].lower() in filler_start:
        words.pop(0)

    # Remover fillers al final
    filler_end = ["por favor", "porfa", "porfavor", "please", "pls", "dale", "va"]
    topic = " ".join(words).strip(".,!?¿¡ ")
    for f in filler_end:
        if topic.lower().endswith(f):
            topic = topic[:-(len(f))].strip(".,!?¿¡ ")

    return topic if len(topic) >= 2 else ""
