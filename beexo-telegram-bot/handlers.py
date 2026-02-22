"""
Handlers de mensajes y eventos de BeeXy.
Incluye: on_message, bienvenida de miembros, reminder_fire,
detección emocional, y lógica de mención al bot.
"""

import io
import re
import random
from datetime import datetime, timedelta

from telegram import Update, ChatMember
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from config import TZ, SCAM_ALERT_COOLDOWN_MIN, logger
from content import SCAM_ALERT, WELCOME_MESSAGES, EMOTION_REACTIONS, contains_wallet_keywords
from db import mark_reminder_fired, add_xp
from ai_chat import ask_ai
from image_tools import search_image, generate_image, detect_image_request, _mentions_real_person


async def safe_reply(msg, text: str, **kwargs):
    """reply_text con fallback a send_message si el mensaje original fue borrado."""
    try:
        return await msg.reply_text(text, **kwargs)
    except Exception:
        try:
            return await msg.chat.send_message(text, **kwargs)
        except Exception as e:
            logger.warning("No se pudo responder: %s", e)
            return None


# ═══════════════════════════════════════════════════════════════
# ESTADO (almacenado en bot_data para thread-safety)
# ═══════════════════════════════════════════════════════════════

# Keys para context.bot_data
_KEY_LAST_SCAM = "last_scam_alert_at"
_KEY_LAST_EMOTION = "last_emotion_at"
_KEY_WELCOMED = "recently_welcomed"
_KEY_BOT_INFO = "bot_info"
_KEY_XP_COOLDOWN = "xp_cooldown"


def _get_bot_data(context: ContextTypes.DEFAULT_TYPE) -> dict:
    """Acceso seguro a bot_data."""
    return context.bot_data




# ═══════════════════════════════════════════════════════════════
# REMINDER
# ═══════════════════════════════════════════════════════════════

async def reminder_fire(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Dispara un recordatorio personal."""
    data = context.job.data
    mention = f"[{data['user_name']}](tg://user?id={data['user_id']})"
    await context.bot.send_message(
        chat_id=data["chat_id"],
        text=f"⏰ *¡Recordatorio para {mention}!*\n\n{data['text']}",
        parse_mode=ParseMode.MARKDOWN,
    )
    logger.info("⏰ Recordatorio enviado a %s", data["user_name"])
    rid = data.get("reminder_id")
    if rid:
        mark_reminder_fired(rid)


# ═══════════════════════════════════════════════════════════════
# BIENVENIDA
# ═══════════════════════════════════════════════════════════════

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Da la bienvenida a nuevos miembros (fallback vía mensaje de servicio)."""
    if not update.message or not update.message.new_chat_members:
        return
    bd = _get_bot_data(context)
    welcomed: set = bd.setdefault(_KEY_WELCOMED, set())

    for member in update.message.new_chat_members:
        if member.is_bot or member.id in welcomed:
            continue
        welcomed.add(member.id)
        name = member.first_name or "amigo"
        welcome = random.choice(WELCOME_MESSAGES).format(name=name)
        await update.message.reply_text(welcome, parse_mode=ParseMode.MARKDOWN)
        logger.info("👋 Bienvenida enviada a %s (service msg)", name)
        context.job_queue.run_once(
            lambda ctx, uid=member.id: bd.setdefault(_KEY_WELCOMED, set()).discard(uid),
            when=300, name=f"welcome_cleanup_{member.id}",
        )


async def track_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Detecta nuevos miembros vía chat_member updates (más confiable en supergrupos)."""
    result = update.chat_member
    if not result:
        return
    old_status = result.old_chat_member.status
    new_status = result.new_chat_member.status

    was_member = old_status in (ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.OWNER)
    is_member = new_status in (ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.OWNER)
    if was_member or not is_member:
        return

    member = result.new_chat_member.user
    bd = _get_bot_data(context)
    welcomed: set = bd.setdefault(_KEY_WELCOMED, set())
    if member.is_bot or member.id in welcomed:
        return

    welcomed.add(member.id)
    name = member.first_name or "amigo"
    welcome = random.choice(WELCOME_MESSAGES).format(name=name)
    await context.bot.send_message(
        chat_id=result.chat.id, text=welcome, parse_mode=ParseMode.MARKDOWN,
    )
    logger.info("👋 Bienvenida enviada a %s (chat_member)", name)
    context.job_queue.run_once(
        lambda ctx, uid=member.id: bd.setdefault(_KEY_WELCOMED, set()).discard(uid),
        when=300, name=f"welcome_cleanup_{member.id}",
    )


# ═══════════════════════════════════════════════════════════════
# REACCIONES EMOCIONALES
# ═══════════════════════════════════════════════════════════════

async def _maybe_react_emotion(msg, text: str, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Detecta emociones en el chat y reacciona con texto + GIF."""
    bd = _get_bot_data(context)
    now = datetime.now(TZ)
    last = bd.get(_KEY_LAST_EMOTION)
    if last and (now - last) < timedelta(minutes=15):
        return
    if len(text) < 10:
        return

    text_lower = text.lower()
    detected = None
    for emotion, edata in EMOTION_REACTIONS.items():
        if any(kw in text_lower for kw in edata["keywords"]):
            detected = emotion
            break
    if not detected:
        return
    if random.random() > 0.25:
        return

    bd[_KEY_LAST_EMOTION] = now
    edata = EMOTION_REACTIONS[detected]

    response = random.choice(edata["responses"])
    await msg.reply_text(response)

    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.images(
                f"{edata['gif_query']} gif", max_results=8,
            ))
        gif_urls = [r["image"] for r in results if r.get("image", "").lower().endswith(".gif")]
        if gif_urls:
            gif_url = random.choice(gif_urls[:5])
            await msg.reply_animation(animation=gif_url)
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════
# HANDLER DE IMÁGENES
# ═══════════════════════════════════════════════════════════════

async def handle_image_request(msg, action: str, topic: str) -> None:
    """Maneja pedidos de búsqueda o generación de imagen."""
    if action == "generate":
        is_real_person = _mentions_real_person(topic)
        if is_real_person:
            thinking = await msg.reply_text(
                "🔍 Buscando foto real... (las IAs no pueden replicar "
                "personas reales con precisión)"
            )
        else:
            thinking = await msg.reply_text("🎨 Generando imagen con IA... puede tardar unos segundos")
        result = await generate_image(topic)
        if result:
            img_bytes, enhanced = result
            photo = io.BytesIO(img_bytes)
            photo.name = "beexy_gen.png"
            try:
                await thinking.delete()
            except Exception:
                pass
            if is_real_person:
                await msg.reply_photo(
                    photo=photo, caption=f"🔍 Resultado para: _{topic}_",
                    parse_mode=ParseMode.MARKDOWN,
                )
            else:
                await msg.reply_photo(
                    photo=photo, caption=f"🎨 *Generado por BeeXy*\n_{topic}_",
                    parse_mode=ParseMode.MARKDOWN,
                )
        else:
            await thinking.edit_text("😕 No pude generar la imagen. Intentá con otro prompt.")
    else:  # search
        thinking = await msg.reply_text("🔍 Buscando imagen...")
        result = await search_image(topic)
        if result:
            img_bytes, title = result
            photo = io.BytesIO(img_bytes)
            photo.name = "beexy_search.jpg"
            try:
                await thinking.delete()
            except Exception:
                pass
            await msg.reply_photo(photo=photo, caption=f"🔍 {title}")
        else:
            await thinking.edit_text("😕 No encontré imágenes. Probá con otras palabras.")


# ═══════════════════════════════════════════════════════════════
# ON_MESSAGE PRINCIPAL
# ═══════════════════════════════════════════════════════════════

async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler principal para todos los mensajes de texto."""
    msg = update.effective_message
    if not msg or not msg.text:
        return

    text = msg.text
    logger.info("📩 Mensaje recibido en chat %s (tipo: %s): %s", msg.chat_id, msg.chat.type, text[:20])
    bd = _get_bot_data(context)

    # ── Anti-scam ──
    if contains_wallet_keywords(text):
        now = datetime.now(TZ)
        last = bd.get(_KEY_LAST_SCAM)
        if last is None or (now - last) > timedelta(minutes=SCAM_ALERT_COOLDOWN_MIN):
            bd[_KEY_LAST_SCAM] = now
            await safe_reply(msg, SCAM_ALERT, parse_mode=ParseMode.MARKDOWN)

    # ── Sistema de Experiencia (XP) ──
    user_id = msg.from_user.id
    user_name = msg.from_user.first_name or "Usuario"
    xp_cd = bd.setdefault(_KEY_XP_COOLDOWN, {})
    now = datetime.now(TZ)
    last_xp = xp_cd.get(user_id)
    
    if len(text.strip()) >= 5:
        if not last_xp or (now - last_xp) > timedelta(minutes=1):
            xp_cd[user_id] = now
            gained = random.randint(1, 4)
            _, n_lvl, level_up = add_xp(user_id, user_name, gained)
            if level_up:
                # Opcional: avisar nivel
                await safe_reply(
                    msg, 
                    f"🎉 ¡Felicidades [{user_name}](tg://user?id={user_id})! "
                    f"Has subido al *Nivel {n_lvl}* 🏆", 
                    parse_mode=ParseMode.MARKDOWN
                )

    # ── Mención al bot ──
    bot_info = bd.get(_KEY_BOT_INFO)
    bot_username = (bot_info.username or "").lower() if bot_info else ""
    beexy_pattern = re.compile(r"\bbee[\s\-_]?xy\b", re.IGNORECASE)

    is_reply_to_bot = False
    try:
        if msg.reply_to_message and msg.reply_to_message.from_user and msg.reply_to_message.from_user.is_bot:
            is_reply_to_bot = True
    except Exception:
        pass

    mentioned = (
        is_reply_to_bot
        or (bot_username and f"@{bot_username}" in text.lower())
        or bool(beexy_pattern.search(text))
    )

    if mentioned:
        question = text
        if bot_username:
            question = re.sub(fr"@{re.escape(bot_username)}", "", question, flags=re.IGNORECASE)
        question = beexy_pattern.sub("", question).strip().lower()

        if len(question) < 3:
            await safe_reply(
                msg,
                "🐝 ¡Hola! Soy *BeeXy*. Preguntame lo que quieras.\n"
                "Ejemplo: `BeeXy ¿qué es DeFi?`\n"
                "También puedo buscar o generar imágenes 🎨",
                parse_mode=ParseMode.MARKDOWN,
            )
            return

        # Detectar pedido de imagen
        img_req = detect_image_request(question)
        if img_req:
            action, topic = img_req
            await handle_image_request(msg, action, topic)
            return



        thinking_msg = await safe_reply(msg, "🐝 Pensando...")
        user_name = update.effective_user.username or update.effective_user.first_name or ""
        answer = await ask_ai(update.effective_user.id, question, user_name)
        try:
            await thinking_msg.edit_text(answer)
        except Exception:
            # Si no se puede editar, intentar enviar como mensaje nuevo
            await context.bot.send_message(chat_id=msg.chat_id, text=answer)
        return

    # ── Reacciones emocionales ──
    await _maybe_react_emotion(msg, text, context)
