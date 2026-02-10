"""
Genera memes basados en datos cripto en tiempo real.
Usa CoinGecko API (gratuita) para precios y tendencias.
"""

import os
import random
import httpx
from generate_memes import create_meme, MEMES_DIR

# ============================================================
# TEMPLATES DE MEMES SEGÚN ESCENARIO DE MERCADO
# ============================================================

PRICE_UP_TEMPLATES = [
    {"top": "{coin} subio {pct}% hoy", "bottom": "Beexer promedio: les dije que iba a subir", "icon": "UP"},
    {"top": "{coin} pump de {pct}%", "bottom": "El que vendio ayer: por favor no me hablen", "icon": "PUMP"},
    {"top": "{coin} sube {pct}% en 24hs", "bottom": "Los que hicieron HODL: yo siempre supe", "icon": "WIN"},
    {"top": "{coin} hace +{pct}% en un dia", "bottom": "Ahora todos somos expertos en trading", "icon": "GURU"},
    {"top": "{coin} vuela {pct}% para arriba", "bottom": "Mi portfolio por fin respira", "icon": "GREEN"},
    {"top": "{coin} se dispara {pct}%", "bottom": "Cripto Twitter: se los dije pero no me escucharon", "icon": "TOLD"},
    {"top": "Desperte y {coin} subio {pct}%", "bottom": "Hoy si es un buen dia para abrir Beexo", "icon": "AM"},
    {"top": "{coin} +{pct}% de la nada", "bottom": "Los que compraron el dip: somos genios", "icon": "BRAIN"},
]

PRICE_DOWN_TEMPLATES = [
    {"top": "{coin} cayo {pct}% hoy", "bottom": "Beexo: momento perfecto para comprar", "icon": "DIP"},
    {"top": "{coin} dump de {pct}%", "bottom": "Mi portfolio: existir es dolor", "icon": "PAIN"},
    {"top": "{coin} baja {pct}% en 24hs", "bottom": "El que compro ayer: todo segun el plan", "icon": "PLAN"},
    {"top": "{coin} pierde {pct}% hoy", "bottom": "Diamond hands o simplemente no se vender", "icon": "HODL"},
    {"top": "{coin} se desploma {pct}%", "bottom": "Al menos me quedan mis memes de Beexo", "icon": "MEME"},
    {"top": "{coin} -{pct}% y sigue cayendo", "bottom": "Yo esperando el rebote: cualquier momento", "icon": "WAIT"},
    {"top": "{coin} cae {pct}% de golpe", "bottom": "Mi cuenta del banco: te lo adverti", "icon": "BANK"},
    {"top": "Me fui a dormir y {coin} cayo {pct}%", "bottom": "Nota mental: nunca dormir de nuevo", "icon": "SLEEP"},
]

TRENDING_TEMPLATES = [
    {"top": "{coin} esta trending hoy", "bottom": "Todo el mundo: QUE ES ESO Y DONDE COMPRO", "icon": "FOMO"},
    {"top": "Todos hablan de {coin}", "bottom": "Yo que inverti hace un mes: de nada", "icon": "EARLY"},
    {"top": "{coin} se volvio viral", "bottom": "FOMO nivel: vendo mi auto para comprar", "icon": "VIRAL"},
    {"top": "{coin} es tendencia mundial", "bottom": "Mi familia: ya empezaste de nuevo con las criptos", "icon": "TREND"},
    {"top": "{coin} rompe internet hoy", "bottom": "Beexers: nosotros ya lo teniamos", "icon": "OG"},
]

SIDEWAYS_TEMPLATES = [
    {"top": "{coin} se mueve 0.1% en todo el dia", "bottom": "Traders: es el dia mas aburrido de la historia", "icon": "ZZZ"},
    {"top": "{coin} lleva una semana sin moverse", "bottom": "Mi portfolio: soy una stablecoin ahora", "icon": "FLAT"},
    {"top": "{coin} hoy: literalmente +0.01%", "bottom": "Yo mirando el grafico cada 5 minutos igual", "icon": "OJO"},
]

# Paletas de colores según sentimiento
BULLISH_COLORS = [
    {"grad_top": "#0a2a0a", "grad_bottom": "#1a4a1a", "accent": "#00ff88"},
    {"grad_top": "#0a1a20", "grad_bottom": "#1a3a40", "accent": "#03dac6"},
    {"grad_top": "#102010", "grad_bottom": "#204020", "accent": "#4ecdc4"},
]
BEARISH_COLORS = [
    {"grad_top": "#2a0a0a", "grad_bottom": "#4a1a1a", "accent": "#ff4444"},
    {"grad_top": "#1a0a10", "grad_bottom": "#3a1a20", "accent": "#e94560"},
    {"grad_top": "#200a0a", "grad_bottom": "#401010", "accent": "#ff6b6b"},
]
NEUTRAL_COLORS = [
    {"grad_top": "#0a0a2a", "grad_bottom": "#1a1a4a", "accent": "#bb86fc"},
    {"grad_top": "#1a1a0a", "grad_bottom": "#3a3a1a", "accent": "#ffc947"},
    {"grad_top": "#0a1a1a", "grad_bottom": "#1a3a3a", "accent": "#79f7ff"},
]

COINGECKO_BASE = "https://api.coingecko.com/api/v3"


async def fetch_crypto_data():
    """Obtiene datos de precios y tendencias de CoinGecko (API gratuita)."""
    data = {"prices": {}, "trending": []}

    async with httpx.AsyncClient(timeout=15) as client:
        # Precios de top 25 monedas
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
                    data["prices"][coin["symbol"].upper()] = {
                        "name": coin["name"],
                        "price": coin["current_price"],
                        "change_24h": coin.get("price_change_percentage_24h", 0) or 0,
                    }
        except Exception as e:
            print(f"  [!] Error fetching prices: {e}")

        # Monedas trending
        try:
            resp = await client.get(f"{COINGECKO_BASE}/search/trending")
            if resp.status_code == 200:
                for item in resp.json().get("coins", [])[:5]:
                    c = item.get("item", {})
                    data["trending"].append({
                        "name": c.get("name", "???"),
                        "symbol": c.get("symbol", "???").upper(),
                    })
        except Exception as e:
            print(f"  [!] Error fetching trending: {e}")

    return data


def generate_news_meme(crypto_data):
    """
    Genera un meme basado en datos cripto actuales.
    Retorna (path, caption) o (None, None) si no hay datos.
    """
    prices = crypto_data.get("prices", {})
    trending = crypto_data.get("trending", [])
    filename = f"meme_news_{random.randint(1000, 9999)}.png"

    options = []

    # Buscar monedas con movimientos interesantes
    for symbol, info in prices.items():
        change = info["change_24h"]
        if change >= 5:
            options.append(("big_up", symbol, info))
        elif change >= 2:
            options.append(("up", symbol, info))
        elif change <= -5:
            options.append(("big_down", symbol, info))
        elif change <= -2:
            options.append(("down", symbol, info))

    # Agregar opción trending
    if trending:
        options.append(("trending", trending[0]["symbol"], trending[0]))

    # Si no hay movimientos fuertes, usar BTC/ETH
    if not options:
        for sym in ["BTC", "ETH", "SOL"]:
            if sym in prices:
                change = prices[sym]["change_24h"]
                if abs(change) < 1:
                    options.append(("sideways", sym, prices[sym]))
                elif change >= 0:
                    options.append(("up", sym, prices[sym]))
                else:
                    options.append(("down", sym, prices[sym]))
                break

    if not options:
        return None, None

    meme_type, symbol, info = random.choice(options)
    change = info.get("change_24h", 0)
    pct = f"{abs(change):.1f}"

    if meme_type in ("big_up", "up"):
        template = random.choice(PRICE_UP_TEMPLATES)
        colors = random.choice(BULLISH_COLORS)
        cat = "fomo"
    elif meme_type in ("big_down", "down"):
        template = random.choice(PRICE_DOWN_TEMPLATES)
        colors = random.choice(BEARISH_COLORS)
        cat = "dip"
    elif meme_type == "trending":
        template = random.choice(TRENDING_TEMPLATES)
        colors = random.choice(NEUTRAL_COLORS)
        cat = "fomo"
    else:
        template = random.choice(SIDEWAYS_TEMPLATES)
        colors = random.choice(NEUTRAL_COLORS)
        cat = "portfolio"

    top_text = template["top"].format(coin=symbol, pct=pct)
    bottom_text = template["bottom"].format(coin=symbol, pct=pct)

    path = create_meme(
        filename=filename,
        top_text=top_text,
        bottom_text=bottom_text,
        grad_top=colors["grad_top"],
        grad_bottom=colors["grad_bottom"],
        accent=colors["accent"],
        sep_style=random.choice(["line", "dots", "arrow"]),
        icon_text=template["icon"],
        category=cat,
    )

    price_str = ""
    if isinstance(info.get("price"), (int, float)):
        price_str = f" — ${info['price']:,.2f}"

    sign = "+" if change >= 0 else ""
    emoji = "\U0001f7e2" if change >= 0 else "\U0001f534"

    caption = (
        f"{emoji} *{symbol}* hoy: {sign}{change:.1f}%{price_str}\n\n"
        f"{top_text}...\n{bottom_text}\n\n"
        f"\U0001f41d _Meme generado en vivo por Beexo Bot_"
    )

    return path, caption
