"""
Command handlers de BeeXy.
Cada función maneja un comando de Telegram (/help, /ask, etc.)
Incluye el nuevo comando /precio y /report.
"""

import re
import random
from datetime import datetime, timezone

import httpx
from telegram import Update, ChatMember
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from config import TZ, MEMES_DIR, logger
from content import POLLS
from handlers import handle_image_request, reminder_fire, safe_reply
from db import save_report, save_reminder
from ai_chat import ask_ai, COIN_ALIASES
from meme_pool import pick_meme, use_and_replace
from trivias_data import TRIVIAS_DATA as TRIVIAS

import os


# ═══════════════════════════════════════════════════════════════
# COMANDOS DE INFO
# ═══════════════════════════════════════════════════════════════

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await safe_reply(
        update.message,
        "🐝 *Soy BeeXy, tu asistente cripto*\n\n"
        "📚 *Info*\n"
        "/rules — Reglas del grupo\n"
        "/faq — Preguntas frecuentes\n\n"
        "🧠 *IA*\n"
        "/ask — Preguntale a BeeXy\n"
        "/imagen — Buscar una imagen 🔍\n"
        "/generar — Generar imagen con IA 🎨\n\n"
        "🎮 *Comunidad*\n"
        "/trivia — Trivia cripto\n"
        "/poll — Encuesta\n"
        "/meme — Meme random\n\n"
        "💰 *Mercado*\n"
        "/precio — Precio de una cripto\n"
        "  Ej: `/precio btc eth sol`\n\n"
        "⏰ *Utilidades*\n"
        "/recordar — Recordatorio personal\n"
        "  Ej: `/recordar 2h comprar ETH`\n\n"
        "💬 *Mencioname:*\n"
        "`BeeXy ¿qué es DeFi?`\n"
        "`BeeXy dibujame un gato astronauta`\n"
        "`BeeXy buscame una foto de bitcoin`\n\n"
        "🤖 *Automático:* resumen diario 10am, noticias lunes 11am, "
        "efemérides, datos curiosos, memes y trivias.",
        parse_mode=ParseMode.MARKDOWN,
    )


async def rules_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🛡 Nunca compartas tu seed phrase.\n"
        "🛡 Nadie te escribirá por privado primero.",
        parse_mode=ParseMode.MARKDOWN,
    )


async def faq_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    faq_text = (
        "📌 *FAQ – Beexo Wallet*\n\n"
        "🔐 *1) ¿Alguien del equipo puede pedirme mis 12 palabras?*\n"
        "No. Nunca. Bajo ningún motivo.\n"
        "Si alguien te las pide, es una estafa.\n\n"
        "💬 *2) ¿El soporte puede escribirme por privado?*\n"
        "No iniciamos conversaciones por privado.\n"
        "Toda ayuda comienza en el grupo oficial.\n\n"
        "🛠 *3) ¿Qué hago si tengo un problema con mi wallet?*\n"
        "Explicá tu situación acá en el grupo y etiquetá al bot.\n"
        "Nunca compartas seed phrase, claves privadas ni capturas sensibles.\n\n"
        "⚠️ *4) Me escribió alguien diciendo que es admin*\n"
        "Verificá el usuario dentro del grupo.\n"
        "Si duda → reportalo inmediatamente acá.\n\n"
        "📚 *5) ¿Dónde aprendo más sobre seguridad en Web3?*\n"
        "Regla básica: si suena urgente o demasiado bueno para ser real, probablemente sea scam.\n\n"
        "🛡 *Recordatorio final:*\n"
        "Tu seed phrase = control total de tus fondos.\n"
        "Nunca la compartas."
    )
    await update.message.reply_text(faq_text, parse_mode=ParseMode.MARKDOWN)


# ═══════════════════════════════════════════════════════════════
# COMANDOS DE COMUNIDAD
# ═══════════════════════════════════════════════════════════════

async def meme_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    meme = pick_meme()
    if meme is None:
        await update.message.reply_text("🎭 No hay memes disponibles, se están generando nuevos...")
        return

    meme_file = meme["file"]
    caption = f'{meme["top"]}... {meme["bottom"]}'
    image_path = os.path.join(MEMES_DIR, meme_file)

    if os.path.exists(image_path):
        with open(image_path, "rb") as photo:
            await update.message.reply_photo(photo=photo, caption=caption)
    else:
        await update.message.reply_text(caption)

    # Eliminar usado y generar reemplazo
    await use_and_replace(meme)


async def trivia_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    t = random.choice(TRIVIAS)
    await context.bot.send_poll(
        chat_id=update.effective_chat.id,
        question=t["q"], options=t["options"],
        type="quiz", correct_option_id=t["correct"],
        is_anonymous=False, explanation=t["explain"],
    )


async def poll_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    q, opts = random.choice(POLLS)
    await context.bot.send_poll(
        chat_id=update.effective_chat.id,
        question=q, options=opts, is_anonymous=False,
    )


# ═══════════════════════════════════════════════════════════════
# COMANDOS DE IA
# ═══════════════════════════════════════════════════════════════

async def ask_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /ask — pregunta a la IA."""
    if not context.args:
        await update.message.reply_text(
            "🤖 Usá el comando así:\n`/ask ¿qué es una seed phrase?`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return
    question = " ".join(context.args)
    thinking_msg = await update.message.reply_text("🤖 Pensando...")
    user_name = update.effective_user.username or update.effective_user.first_name or ""
    answer = await ask_ai(update.effective_user.id, question, user_name)
    await thinking_msg.edit_text(answer)


async def imagen_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /imagen — busca y envía una imagen de la web."""
    if not context.args:
        await update.message.reply_text(
            "🔍 Usá el comando así:\n`/imagen gato con bitcoin`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return
    query = " ".join(context.args)
    await handle_image_request(update.message, "search", query)


async def generar_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /generar — genera una imagen con IA."""
    if not context.args:
        await update.message.reply_text(
            "🎨 Usá el comando así:\n`/generar un astronauta en la luna con bitcoin`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return
    prompt = " ".join(context.args)
    await handle_image_request(update.message, "generate", prompt)


# ═══════════════════════════════════════════════════════════════
# COMANDO /precio (NUEVO)
# ═══════════════════════════════════════════════════════════════

async def precio_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /precio — consulta rápida de precios sin pasar por IA."""
    if not context.args:
        await update.message.reply_text(
            "💰 Usá el comando así:\n"
            "`/precio btc`\n"
            "`/precio eth sol ada`\n\n"
            "Criptos soportadas: BTC, ETH, BNB, SOL, ADA, XRP, DOGE, DOT, "
            "SHIB, AVAX, MATIC, LINK, UNI, ATOM, LTC, TRX, USDT, USDC, "
            "NEAR, APT, ARB, OP, SUI, PEPE",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    # Resolver aliases a IDs de CoinGecko
    coin_ids = []
    unknown = []
    for arg in context.args:
        alias = arg.lower().strip()
        if alias in COIN_ALIASES:
            cg_id = COIN_ALIASES[alias]
            if cg_id not in coin_ids:
                coin_ids.append(cg_id)
        else:
            unknown.append(arg.upper())

    if not coin_ids:
        await update.message.reply_text(
            f"❌ No reconozco {'esas criptos' if len(unknown) > 1 else 'esa cripto'}. "
            "Probá con el símbolo: `/precio btc eth sol`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    # Fetch precios
    try:
        ids_str = ",".join(coin_ids[:10])
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={
                    "ids": ids_str,
                    "vs_currencies": "usd,ars",
                    "include_24hr_change": "true",
                    "include_market_cap": "true",
                },
            )
        if resp.status_code != 200:
            await update.message.reply_text("⚠️ No pude obtener los precios. Intentá de nuevo.")
            return
        data = resp.json()
    except Exception as e:
        logger.warning("Error en /precio: %s", e)
        await update.message.reply_text("⚠️ Error al consultar precios. Intentá de nuevo.")
        return

    # Formatear respuesta
    lines = ["💰 *Precios en vivo*\n"]
    for cg_id in coin_ids:
        if cg_id not in data:
            continue
        p = data[cg_id]
        usd = p.get("usd", 0)
        ars = p.get("ars")
        change = p.get("usd_24h_change", 0) or 0
        mcap = p.get("usd_market_cap", 0) or 0

        emoji = "🟢" if change >= 0 else "🔴"
        sign = "+" if change >= 0 else ""
        symbol = cg_id.upper().replace("-", " ")

        # Formato de precio según magnitud
        if isinstance(usd, (int, float)):
            if usd >= 1:
                price_str = f"${usd:,.2f}"
            elif usd >= 0.001:
                price_str = f"${usd:.4f}"
            else:
                price_str = f"${usd:.8f}"
        else:
            price_str = f"${usd}"

        line = f"{emoji} *{symbol}*: {price_str} ({sign}{change:.1f}%)"
        if ars and isinstance(ars, (int, float)):
            line += f"\n   └ ARS ${ars:,.0f}"
        if mcap > 0:
            if mcap >= 1e12:
                line += f" · MCap ${mcap/1e12:.1f}T"
            elif mcap >= 1e9:
                line += f" · MCap ${mcap/1e9:.1f}B"
            elif mcap >= 1e6:
                line += f" · MCap ${mcap/1e6:.0f}M"
        lines.append(line)

    if unknown:
        lines.append(f"\n⚠️ No encontré: {', '.join(unknown)}")

    lines.append(f"\n_Fuente: CoinGecko · {datetime.now(TZ).strftime('%H:%M')}_")

    await update.message.reply_text(
        "\n".join(lines), parse_mode=ParseMode.MARKDOWN,
    )


# ═══════════════════════════════════════════════════════════════
# COMANDO /recordar
# ═══════════════════════════════════════════════════════════════

async def recordar_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /recordar — programa un recordatorio personal."""
    if len(context.args) < 2:
        await update.message.reply_text(
            "⏰ Usá el comando así:\n"
            "`/recordar 2h comprar ETH`\n"
            "`/recordar 30m revisar portfolio`\n"
            "`/recordar 1d chequear staking`\n\n"
            "Unidades: *m* (minutos), *h* (horas), *d* (días)",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    time_str = context.args[0].lower()
    reminder_text = " ".join(context.args[1:])

    match = re.match(r"^(\d+)(m|h|d)$", time_str)
    if not match:
        await update.message.reply_text(
            "❌ Formato inválido. Usá: `30m`, `2h`, `1d`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    amount = int(match.group(1))
    unit = match.group(2)

    if unit == "m":
        seconds = amount * 60
        display = f"{amount} minuto{'s' if amount != 1 else ''}"
    elif unit == "h":
        seconds = amount * 3600
        display = f"{amount} hora{'s' if amount != 1 else ''}"
    else:
        seconds = amount * 86400
        display = f"{amount} día{'s' if amount != 1 else ''}"

    if seconds < 60:
        await update.message.reply_text("❌ Mínimo 1 minuto.")
        return
    if seconds > 7 * 86400:
        await update.message.reply_text("❌ Máximo 7 días.")
        return

    user = update.effective_user
    user_name = user.first_name or "amigo"
    chat_id = update.effective_chat.id

    scheduled_at = int(datetime.now(timezone.utc).timestamp()) + seconds
    reminder_id = save_reminder(user.id, user_name, chat_id, reminder_text, scheduled_at)

    context.job_queue.run_once(
        reminder_fire, when=seconds,
        data={
            "chat_id": chat_id, "user_id": user.id,
            "user_name": user_name, "text": reminder_text,
            "reminder_id": reminder_id,
        },
        name=f"reminder_{user.id}_{int(datetime.now().timestamp())}",
    )

    await update.message.reply_text(
        f"✅ Te recuerdo en *{display}*:\n_{reminder_text}_",
        parse_mode=ParseMode.MARKDOWN,
    )


# ═══════════════════════════════════════════════════════════════
# COMANDO /report
# ═══════════════════════════════════════════════════════════════

async def report_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /report — solo admins pueden reportar usuarios."""
    msg = update.effective_message
    if not msg:
        return

    chat = update.effective_chat
    user = update.effective_user

    # Verificar permisos de admin
    try:
        member = await context.bot.get_chat_member(chat.id, user.id)
        if member.status not in (ChatMember.ADMINISTRATOR, ChatMember.OWNER):
            await msg.reply_text("❌ Solo los administradores pueden usar /report.")
            return
    except Exception:
        await msg.reply_text("⚠️ No pude verificar permisos.")
        return

    # Determinar usuario reportado
    target_user = None
    reason = None
    if msg.reply_to_message and msg.reply_to_message.from_user:
        target_user = msg.reply_to_message.from_user
        reason = " ".join(context.args).strip() if context.args else "(sin motivo especificado)"
    else:
        if not context.args:
            await msg.reply_text(
                "Uso: /report @usuario motivo  — o responde al mensaje y escribe /report motivo"
            )
            return
        first = context.args[0]
        rest = context.args[1:]
        reason = " ".join(rest).strip() if rest else "(sin motivo especificado)"
        if first.startswith("@"):
            uname = first[1:]
            target_user = type("U", (), {"id": None, "first_name": uname, "username": uname})()
        else:
            try:
                uid = int(first)
                try:
                    cu = await context.bot.get_chat_member(chat.id, uid)
                    target_user = cu.user
                except Exception:
                    target_user = type("U", (), {"id": uid, "first_name": str(uid), "username": None})()
            except Exception:
                await msg.reply_text("Usuario inválido. Usa @usuario o responde al mensaje.")
                return

    rid = save_report(
        reporter_id=user.id,
        reporter_name=user.first_name or "",
        reported_id=getattr(target_user, "id", None),
        reported_name=getattr(target_user, "first_name", getattr(target_user, "username", "")),
        chat_id=chat.id,
        reason=reason,
    )

    if rid is None:
        await msg.reply_text("⚠️ Error al guardar el reporte.")
        return

    await msg.reply_text(f"✅ Reporte guardado (id={rid}). Los administradores pueden gestionarlo desde el backend.")
    try:
        reported_name = getattr(target_user, "first_name", getattr(target_user, "username", "desconocido"))
        await context.bot.send_message(
            chat_id=chat.id,
            text=(
                f"🚨 Reporte registrado por [{user.first_name}](tg://user?id={user.id}) "
                f"contra {reported_name} — id={rid}\nMotivo: {reason}"
            ),
            parse_mode=ParseMode.MARKDOWN,
            disable_notification=True,
        )
    except Exception:
        pass
