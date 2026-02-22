"""
Jobs automáticos programados de BeeXy.
Incluye: mensajes diarios, memes, resumen cripto, noticias,
trivias, efemérides, datos curiosos y memes de noticias cripto.
"""

import os
import random
from datetime import datetime, time, timedelta

import httpx
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from config import TARGET_CHAT_IDS, TZ, MEMES_DIR, logger
from chat_roles import community_chats, memes_chat
from content import GOOD_MORNING, GOOD_NIGHT, POLLS
from trivias_data import TRIVIAS_DATA as TRIVIAS
from crypto_data import CRYPTO_EPHEMERIDES, CRYPTO_FUN_FACTS


# ═══════════════════════════════════════════════════════════════
# UTILIDADES
# ═══════════════════════════════════════════════════════════════

def time_until(target_time: time) -> float:
    """Calcula los segundos desde ahora hasta un time() dado hoy."""
    now = datetime.now(TZ)
    target_dt = now.replace(hour=target_time.hour, minute=target_time.minute, second=0, microsecond=0)
    if target_dt <= now:
        target_dt += timedelta(days=1)
    delta = (target_dt - now).total_seconds()
    return max(delta, 60)


# ═══════════════════════════════════════════════════════════════
# JOBS DIARIOS
# ═══════════════════════════════════════════════════════════════

async def morning_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    for cid in community_chats():
        await context.bot.send_message(
            chat_id=cid, text=random.choice(GOOD_MORNING),
            parse_mode=ParseMode.MARKDOWN,
        )


async def night_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    for cid in community_chats():
        await context.bot.send_message(
            chat_id=cid, text=random.choice(GOOD_NIGHT),
            parse_mode=ParseMode.MARKDOWN,
        )


async def engagement_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    if random.random() < 0.6:
        t = random.choice(TRIVIAS)
        for cid in community_chats():
            await context.bot.send_poll(
                chat_id=cid, question=t["q"], options=t["options"],
                type="quiz", correct_option_id=t["correct"],
                is_anonymous=False, explanation=t["explain"],
            )
    else:
        q, opts = random.choice(POLLS)
        for cid in community_chats():
            await context.bot.send_poll(
                chat_id=cid, question=q, options=opts, is_anonymous=False,
            )



# ═══════════════════════════════════════════════════════════════
# RESUMEN CRIPTO DIARIO
# ═══════════════════════════════════════════════════════════════

async def daily_crypto_summary_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envía resumen diario del mercado cripto a las 10am."""
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={
                    "ids": "bitcoin,ethereum,binancecoin,solana,ripple,cardano,dogecoin,polkadot",
                    "vs_currencies": "usd",
                    "include_24hr_change": "true",
                },
            )
            data = resp.json()
    except Exception as e:
        logger.warning("⚠️ Error en crypto summary: %s", e)
        return

    coins_map = {
        "bitcoin": ("BTC", "₿"), "ethereum": ("ETH", "⟠"), "binancecoin": ("BNB", "🔶"),
        "solana": ("SOL", "◎"), "ripple": ("XRP", "💧"), "cardano": ("ADA", "🔵"),
        "dogecoin": ("DOGE", "🐕"), "polkadot": ("DOT", "⬡"),
    }
    lines = ["📊 *Resumen Diario del Mercado Cripto*\n"]
    valid_coins = 0
    for coin_id, (symbol, icon) in coins_map.items():
        if coin_id in data:
            d = data[coin_id]
            price = d.get("usd", 0)
            change = d.get("usd_24h_change", 0) or 0
            emoji = "🟢" if change >= 0 else "🔴"
            sign = "+" if change >= 0 else ""
            if price >= 1:
                lines.append(f"{emoji} {icon} *{symbol}*: ${price:,.2f} ({sign}{change:.1f}%)")
            else:
                lines.append(f"{emoji} {icon} *{symbol}*: ${price:.4f} ({sign}{change:.1f}%)")
            valid_coins += 1
            
    if valid_coins == 0:
        logger.warning("📊 Resumen cripto diario cancleado: No se obtuvieron datos de precios válidos.")
        return

    lines.append(f"\n_Actualizado: {datetime.now(TZ).strftime('%d/%m/%Y %H:%M')}_")
    for cid in community_chats():
        await context.bot.send_message(
            chat_id=cid, text="\n".join(lines), parse_mode=ParseMode.MARKDOWN,
        )
    logger.info("📊 Resumen cripto diario enviado")


# ═══════════════════════════════════════════════════════════════
# OTROS JOBS
# ═══════════════════════════════════════════════════════════════

async def weekly_fun_fact_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envía un dato curioso de cripto una vez por semana."""
    fact = random.choice(CRYPTO_FUN_FACTS)
    for cid in community_chats():
        await context.bot.send_message(
            chat_id=cid, text=fact, parse_mode=ParseMode.MARKDOWN,
        )
    logger.info("🧠 Dato curioso enviado")


async def ephemerides_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Publica la efeméride cripto del día si existe."""
    today = datetime.now(TZ)
    key = (today.month, today.day)
    if key in CRYPTO_EPHEMERIDES:
        for cid in community_chats():
            await context.bot.send_message(
                chat_id=cid, text=CRYPTO_EPHEMERIDES[key],
                parse_mode=ParseMode.MARKDOWN,
            )
        logger.info("📅 Efémeride enviada: %d/%d", key[0], key[1])


async def weekly_news_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envía las 5 noticias cripto más importantes — solo los lunes a las 11am."""
    # Guardia: solo ejecutar los lunes (weekday 0)
    if datetime.now(TZ).weekday() != 0:
        logger.info("📰 weekly_news_job omitido: hoy no es lunes")
        return

    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.news(
                "criptomonedas bitcoin ethereum crypto noticias",
                region="es-ar", max_results=5,
            ))
    except Exception as e:
        logger.warning("⚠️ Error en weekly news: %s", e)
        return

    if not results:
        logger.info("📰 No se encontraron noticias")
        return

    lines = ["📰 *Las 5 noticias cripto de la semana* 🗞️\n"]
    for i, r in enumerate(results, 1):
        title = r.get("title", "Sin título")
        url = r.get("url", "")
        source = r.get("source", "")
        lines.append(f"*{i}.* [{title}]({url})" + (f" — _{source}_" if source else ""))
    lines.append(f"\n_Resumen semanal — {datetime.now(TZ).strftime('%d/%m/%Y')}_")
    for cid in community_chats():
        await context.bot.send_message(
            chat_id=cid, text="\n".join(lines),
            parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True,
        )
    logger.info("📰 Noticias semanales enviadas")


async def auto_trivia_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envía una trivia al grupo automáticamente cada ~2 días."""
    try:
        t = random.choice(TRIVIAS)
        for cid in community_chats():
            await context.bot.send_poll(
                chat_id=cid, question=t["q"], options=t["options"],
                type="quiz", correct_option_id=t["correct"],
                is_anonymous=False, explanation=t["explain"],
            )
        logger.info("🧩 Trivia automática enviada")
    except Exception as e:
        logger.warning("⚠️ Error en auto_trivia_job: %s", e)
    finally:
        next_delay = random.uniform(36, 60) * 3600
        context.job_queue.run_once(auto_trivia_job, when=next_delay, name="auto_trivia")
        logger.info("🧩 Próxima trivia auto en %.1f horas", next_delay / 3600)
