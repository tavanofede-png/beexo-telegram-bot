import os
import io
import re
import random
import logging
from datetime import time, datetime, timedelta
from zoneinfo import ZoneInfo


from dotenv import load_dotenv
from telegram import Update, BotCommand, ChatMember
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    ChatMemberHandler,
    filters
)


# =========================
# CONFIG
# =========================


# Load .env from the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, '.env')
print(f"📁 Loading .env from: {dotenv_path}")
# Force .env values to override any existing environment variables
load_dotenv(dotenv_path, override=True)
logging.basicConfig(level=logging.INFO)


print(f"🔑 TOKEN starts with: {os.environ.get('TELEGRAM_BOT_TOKEN', 'NOT_SET')[:20]}...")
print(f"💬 TARGET_CHAT_ID (raw): {os.environ.get('TARGET_CHAT_ID', 'NOT_SET')}")


TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TARGET_CHAT_ID = int(os.environ["TARGET_CHAT_ID"])
TZ = ZoneInfo(os.getenv("TZ", "America/Argentina/Buenos_Aires"))


SCAM_ALERT_COOLDOWN_MIN = 5
last_scam_alert_at = None
_recently_welcomed: set[int] = set()  # evita bienvenida doble


# =========================
# CONTENIDO
# =========================


GOOD_MORNING = [
    "☀️ *Buen día Beexers!* Hoy aprendé 1 concepto nuevo de cripto y compartilo 👇",
    "🚀 *Buen día!* Paciencia + criterio > hype.",
    "📈 *Buen día comunidad!* Hoy gana el que gestiona riesgo.",
    "🔥 *Buen día!* Mini desafío: explicá blockchain en 1 frase.",
    "🧠 *Buen día!* Recordá: DYOR antes de invertir."
]


GOOD_NIGHT = [
    "🌙 *Buenas noches Beexo.* Sobrevivir en cripto ya es ganar.",
    "✨ *Buenas noches.* Gestión de riesgo > euforia.",
    "🛌 *Buenas noches!* Nunca compartas tu seed phrase.",
    "🌑 *Buenas noches comunidad.* ¿Qué aprendiste hoy?",
    "🌙 *Buenas noches.* Si hoy fue rojo, fue información."
]


SCAM_ALERT = (
    "⚠️ *ALERTA ANTI-SCAM*\n\n"
    "• Nadie te pedirá tus *12 palabras / seed phrase*\n"
    "• Ningún admin te escribe por privado primero\n"
    "• Pedí ayuda solo en el grupo\n"
)


KEYWORDS_WALLET = [
    # Seed / claves
    "seed", "seed phrase", "12 palabras", "24 palabras", "frase semilla",
    "frase de recuperación", "recovery phrase", "private key", "clave privada",
    "mnemonic", "passphrase",
    # Wallet / billetera
    "wallet", "billetera", "recovery", "restaurar wallet",
    # Contacto sospechoso
    "me escribieron", "me contactaron", "me mandó mensaje",
    "dm", "privado", "por privado", "mensaje privado", "inbox",
    # Soporte falso
    "soporte", "soporte técnico", "support", "ayuda", "help",
    "admin", "administrador", "moderador",
    # Scams clásicos
    "validar wallet", "verificar wallet", "sincronizar", "sync",
    "conectar wallet", "connect wallet", "migrar", "migrate",
    "actualizar wallet", "upgrade",
    # Regalos / airdrops falsos
    "airdrop", "claim", "regalo", "giveaway", "sorteo",
    "token gratis", "gratis", "free", "whitelist",
    # Inversión fraudulenta
    "inversión garantizada", "rendimiento garantizado", "duplicar",
    "enviar para recibir", "ganancia segura", "100% profit",
    # Usuario vulnerable
    "me hackearon", "hackeado", "me robaron", "robaron mis fondos",
    "perdí mis fondos", "no puedo acceder", "fondos bloqueados",
    "desbloquear", "congelaron", "frozen",
    # Phishing
    "formulario", "form", "kyc", "verificar identidad",
    "ingresá tu", "ingresa tu", "completar datos",
]


def time_until(target_time):
    """Calcula los segundos desde ahora hasta un time() dado hoy."""
    now = datetime.now(TZ)
    target_dt = now.replace(hour=target_time.hour, minute=target_time.minute, second=0, microsecond=0)
    if target_dt <= now:
        # Ya pasó la hora, programar para mañana no tendría sentido,
        # pero en schedule_daily_memes se llama a las 00:05 así que no debería pasar
        target_dt += timedelta(days=1)
    delta = (target_dt - now).total_seconds()
    return max(delta, 60)  # Mínimo 60 segundos


# Directorio de imágenes de memes
MEMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memes")


# Cargar 200 memes desde memes_data.py
from memes_data import MEMES_DATA
from ai_chat import ask_ai, DB_PATH
import sqlite3
from image_tools import search_image, generate_image, detect_image_request, _mentions_real_person
MEMES = [(m["file"], f'{m["top"]}... {m["bottom"]}') for m in MEMES_DATA]


from trivias_data import TRIVIAS_DATA as TRIVIAS
from crypto_data import CRYPTO_EPHEMERIDES, CRYPTO_FUN_FACTS


# Mensajes de bienvenida
WELCOME_MESSAGES = [
    "🐝 *¡Bienvenid@ {name}!*\n\nSoy *BeeXy*, el bot de la comunidad Beexo.\n\n"
    "📌 Regla #1: nunca compartas tu seed phrase\n"
    "🤖 Consultame lo que necesites: `BeeXy ¿qué es DeFi?`\n"
    "🎨 También genero imágenes: `BeeXy dibujame un gato astronauta`",
    "👋 *¡Hola {name}!* Bienvenid@ a la comunidad Beexo 🐝\n\n"
    "Acá aprendemos sobre cripto y nos cuidamos entre todos.\n"
    "Escribí `/help` para ver todo lo que puedo hacer.",
    "🎉 *¡{name} se sumó a Beexo!*\n\n"
    "Bienvenid@ a la mejor comunidad cripto de habla hispana.\n"
    "Nunca respondas DMs de \"soporte\". Toda ayuda acá en el grupo. 🛡",
]


# Reacciones emocionales
EMOTION_REACTIONS = {
    "pump": {
        "keywords": ["pump", "pumpeando", "bullish", "bull run",
                     "todo verde", "subiendo fuerte", "para arriba"],
        "responses": [
            "🚀🟢 ¡PUMP MODE ACTIVADO! A la luna vamos 🌕",
            "📈💚 ¡Verde que te quiero verde! Los toros mandan 🐂",
            "🔥 ¡Despegamos! Abróchense los cinturones 🚀",
        ],
        "gif_query": "crypto pump rocket celebration",
    },
    "dump": {
        "keywords": ["dump", "crash", "se desplomó", "todo rojo", "cayó fuerte",
                     "bearish", "liquidado", "liquidaron", "dumpeando"],
        "responses": [
            "📉🔴 F en el chat... Resistamos 💀",
            "🩸 Día rojo. Recordá: el que no vende no pierde",
            "🐻 Los osos atacaron hoy. Paciencia 💪",
        ],
        "gif_query": "crypto crash panic oh no",
    },
    "hodl": {
        "keywords": ["hodl", "diamond hands", "manos de diamante", "no vendo",
                     "aguantamos", "hold fuerte"],
        "responses": [
            "💎🙌 ¡HODL GANG! Las manos de diamante nunca fallan",
            "🗿 Aguantamos como campeones. HODL forever.",
            "💪 El que aguanta, gana. No suelten.",
        ],
        "gif_query": "diamond hands hodl strong",
    },
    "fomo": {
        "keywords": ["fomo", "all in", "compro ya", "yolo", "me lo pierdo"],
        "responses": [
            "⚠️ ¡Cuidado con el FOMO! DYOR siempre 🧠",
            "🎰 FOMO detectado... Respirá hondo primero",
            "💡 No comprés por FOMO, comprá por convicción",
        ],
        "gif_query": "fomo panic buying hurry",
    },
    "moon": {
        "keywords": ["to the moon", "ath", "máximo histórico", "all time high",
                     "nuevo máximo", "mooning"],
        "responses": [
            "🌕 ¡TO THE MOOOON! 🚀🚀🚀",
            "🏔️ ¡Nuevo ATH! Esto es histórico 🎉",
            "🌙 ¡La luna queda chica! Sin frenos 🔥",
        ],
        "gif_query": "to the moon crypto celebration",
    },
}
last_emotion_at = None


POLLS = [
    ("📊 ¿Cómo ves el mercado hoy?", ["Bullish", "Neutral", "Bearish", "Solo observo"]),
    ("📊 ¿Qué querés más en la comunidad?", ["Trivias", "Noticias", "Tutoriales", "AMAs"])
]


# =========================
# FUNCIONES
# =========================


def contains_wallet_keywords(text: str) -> bool:
    t = (text or "").lower()
    return any(k in t for k in KEYWORDS_WALLET)


# =========================
# JOBS AUTOMÁTICOS
# =========================


async def morning_job(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=TARGET_CHAT_ID,
        text=random.choice(GOOD_MORNING),
        parse_mode=ParseMode.MARKDOWN
    )


async def night_job(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=TARGET_CHAT_ID,
        text=random.choice(GOOD_NIGHT),
        parse_mode=ParseMode.MARKDOWN
    )


async def engagement_job(context: ContextTypes.DEFAULT_TYPE):
    if random.random() < 0.6:
        t = random.choice(TRIVIAS)
        await context.bot.send_poll(
            chat_id=TARGET_CHAT_ID,
            question=t["q"],
            options=t["options"],
            type="quiz",
            correct_option_id=t["correct"],
            is_anonymous=False,
            explanation=t["explain"],
        )
    else:
        q, opts = random.choice(POLLS)
        await context.bot.send_poll(
            chat_id=TARGET_CHAT_ID,
            question=q,
            options=opts,
            is_anonymous=False
        )


async def send_meme_job(context: ContextTypes.DEFAULT_TYPE):
    """Envía un meme aleatorio al grupo."""
    meme_file, caption = random.choice(MEMES)
    image_path = os.path.join(MEMES_DIR, meme_file)
    if os.path.exists(image_path):
        with open(image_path, "rb") as photo:
            await context.bot.send_photo(
                chat_id=TARGET_CHAT_ID,
                photo=photo,
                caption=caption,
            )
    else:
        await context.bot.send_message(
            chat_id=TARGET_CHAT_ID,
            text=caption
        )
    print(f"🎭 Meme enviado: {meme_file}")


async def schedule_daily_memes(context: ContextTypes.DEFAULT_TYPE):
    """Planifica 2 memes a horas aleatorias del día (entre 9:00 y 22:00)."""
    # Elegir 2 horarios aleatorios distintos
    hours = sorted(random.sample(range(9, 22), 2))
    for h in hours:
        minute = random.randint(0, 59)
        send_time = time(h, minute, tzinfo=TZ)
        context.job_queue.run_once(
            send_meme_job,
            when=time_until(send_time),
            name=f"meme_diario_{h}_{minute}"
        )
        print(f"🎭 Meme programado para hoy a las {h:02d}:{minute:02d}")


async def crypto_news_meme_job(context: ContextTypes.DEFAULT_TYPE):
    """Busca datos del mercado cripto y genera un meme en vivo."""
    try:
        from crypto_news_meme import fetch_crypto_data, generate_news_meme
        print("📰 Generando meme de noticias cripto...")
        data = await fetch_crypto_data()
        path, caption = generate_news_meme(data)
        if path and os.path.exists(path):
            with open(path, "rb") as photo:
                await context.bot.send_photo(
                    chat_id=TARGET_CHAT_ID,
                    photo=photo,
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN,
                )
            print(f"📰 Meme cripto enviado: {os.path.basename(path)}")
        else:
            print("📰 No se pudo generar meme cripto (sin datos)")
    except Exception as e:
        print(f"⚠️ Error en crypto_news_meme_job: {e}")
    finally:
        next_delay = random.uniform(18, 28) * 3600
        context.job_queue.run_once(crypto_news_meme_job, when=next_delay, name="crypto_meme")
        print(f"📰 Próximo meme cripto en {next_delay/3600:.1f} horas")


async def auto_trivia_job(context: ContextTypes.DEFAULT_TYPE):
    """Envía una trivia al grupo automáticamente cada ~2 días."""
    try:
        t = random.choice(TRIVIAS)
        await context.bot.send_poll(
            chat_id=TARGET_CHAT_ID,
            question=t["q"],
            options=t["options"],
            type="quiz",
            correct_option_id=t["correct"],
            is_anonymous=False,
            explanation=t["explain"],
        )
        print("🧩 Trivia automática enviada")
    except Exception as e:
        print(f"⚠️ Error en auto_trivia_job: {e}")
    finally:
        next_delay = random.uniform(36, 60) * 3600
        context.job_queue.run_once(auto_trivia_job, when=next_delay, name="auto_trivia")
        print(f"🧩 Próxima trivia auto en {next_delay/3600:.1f} horas")


async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Da la bienvenida a nuevos miembros (fallback vía mensaje de servicio)."""
    if not update.message or not update.message.new_chat_members:
        return
    for member in update.message.new_chat_members:
        if member.is_bot or member.id in _recently_welcomed:
            continue
        _recently_welcomed.add(member.id)
        name = member.first_name or "amigo"
        welcome = random.choice(WELCOME_MESSAGES).format(name=name)
        await update.message.reply_text(welcome, parse_mode=ParseMode.MARKDOWN)
        print(f"👋 Bienvenida enviada a {name} (service msg)")
        # Limpiar cache después de 5 min para no acumular memoria
        context.job_queue.run_once(
            lambda ctx, uid=member.id: _recently_welcomed.discard(uid),
            when=300, name=f"welcome_cleanup_{member.id}"
        )


async def track_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Detecta nuevos miembros vía chat_member updates (más confiable en supergrupos)."""
    result = update.chat_member
    if not result:
        return
    old_status = result.old_chat_member.status
    new_status = result.new_chat_member.status


    # ¿Pasó de no-miembro a miembro?
    was_member = old_status in (
        ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.OWNER,
    )
    is_member = new_status in (
        ChatMember.MEMBER, ChatMember.ADMINISTRATOR, ChatMember.OWNER,
    )
    if was_member or not is_member:
        return


    member = result.new_chat_member.user
    if member.is_bot or member.id in _recently_welcomed:
        return


    _recently_welcomed.add(member.id)
    name = member.first_name or "amigo"
    welcome = random.choice(WELCOME_MESSAGES).format(name=name)
    await context.bot.send_message(
        chat_id=result.chat.id,
        text=welcome,
        parse_mode=ParseMode.MARKDOWN,
    )
    print(f"👋 Bienvenida enviada a {name} (chat_member)")
    context.job_queue.run_once(
        lambda ctx, uid=member.id: _recently_welcomed.discard(uid),
        when=300, name=f"welcome_cleanup_{member.id}"
    )


async def daily_crypto_summary_job(context: ContextTypes.DEFAULT_TYPE):
    """Envía resumen diario del mercado cripto a las 10am."""
    import httpx
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={
                    "ids": "bitcoin,ethereum,binancecoin,solana,ripple,cardano,dogecoin,polkadot",
                    "vs_currencies": "usd",
                    "include_24hr_change": "true",
                }
            )
            data = resp.json()
    except Exception as e:
        print(f"⚠️ Error en crypto summary: {e}")
        return


    coins_map = {
        "bitcoin": ("BTC", "₿"), "ethereum": ("ETH", "⟠"), "binancecoin": ("BNB", "🔶"),
        "solana": ("SOL", "◎"), "ripple": ("XRP", "💧"), "cardano": ("ADA", "🔵"),
        "dogecoin": ("DOGE", "🐕"), "polkadot": ("DOT", "⬡"),
    }
    lines = ["📊 *Resumen Diario del Mercado Cripto*\n"]
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
    lines.append(f"\n_Actualizado: {datetime.now(TZ).strftime('%d/%m/%Y %H:%M')}_")
    await context.bot.send_message(
        chat_id=TARGET_CHAT_ID,
        text="\n".join(lines),
        parse_mode=ParseMode.MARKDOWN,
    )
    print("📊 Resumen cripto diario enviado")


async def weekly_fun_fact_job(context: ContextTypes.DEFAULT_TYPE):
    """Envía un dato curioso de cripto una vez por semana."""
    fact = random.choice(CRYPTO_FUN_FACTS)
    await context.bot.send_message(
        chat_id=TARGET_CHAT_ID,
        text=fact,
        parse_mode=ParseMode.MARKDOWN,
    )
    print("🧠 Dato curioso enviado")


async def ephemerides_job(context: ContextTypes.DEFAULT_TYPE):
    """Publica la efeméride cripto del día si existe."""
    today = datetime.now(TZ)
    key = (today.month, today.day)
    if key in CRYPTO_EPHEMERIDES:
        await context.bot.send_message(
            chat_id=TARGET_CHAT_ID,
            text=CRYPTO_EPHEMERIDES[key],
            parse_mode=ParseMode.MARKDOWN,
        )
        print(f"📅 Efeméride enviada: {key[0]}/{key[1]}")


async def weekly_news_job(context: ContextTypes.DEFAULT_TYPE):
    """Envía las 5 noticias cripto más importantes — lunes 11am."""
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.news(
                "criptomonedas bitcoin ethereum crypto noticias",
                region="es-ar",
                max_results=8,
            ))
    except Exception as e:
        print(f"⚠️ Error en weekly news: {e}")
        return


    if not results:
        print("📰 No se encontraron noticias")
        return


    lines = ["📰 *Las 5 noticias cripto de la semana*\n"]
    for i, r in enumerate(results[:5], 1):
        title = r.get("title", "Sin título")
        url = r.get("url", "")
        source = r.get("source", "")
        lines.append(f"*{i}.* [{title}]({url})" + (f" — _{source}_" if source else ""))
    lines.append(f"\n_Resumen semanal — {datetime.now(TZ).strftime('%d/%m/%Y')}_")
    await context.bot.send_message(
        chat_id=TARGET_CHAT_ID,
        text="\n".join(lines),
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
    print("📰 Noticias semanales enviadas")


async def reminder_fire(context: ContextTypes.DEFAULT_TYPE):
    """Dispara un recordatorio personal."""
    data = context.job.data
    mention = f"[{data['user_name']}](tg://user?id={data['user_id']})"
    await context.bot.send_message(
        chat_id=data["chat_id"],
        text=f"⏰ *¡Recordatorio para {mention}!*\n\n{data['text']}",
        parse_mode=ParseMode.MARKDOWN,
    )
    print(f"⏰ Recordatorio enviado a {data['user_name']}")
    # Marcar como disparado en la DB si tenemos reminder_id
    try:
        rid = data.get("reminder_id")
        if rid:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("UPDATE reminders SET fired=1 WHERE id=?", (rid,))
            conn.commit()
    except Exception:
        pass
    finally:
        try:
            conn.close()
        except Exception:
            pass


async def report_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /report — solo admins pueden reportar usuarios.
    Uso:
      - /report @usuario motivo
      - responder el mensaje del usuario y usar `/report motivo`
    """
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
    # Si se responde a un mensaje, tomamos al autor del mensaje
    if msg.reply_to_message and msg.reply_to_message.from_user:
        target_user = msg.reply_to_message.from_user
        reason = " ".join(context.args).strip() if context.args else "(sin motivo especificado)"
    else:
        if not context.args:
            await msg.reply_text("Uso: /report @usuario motivo  — o responde al mensaje y escribe /report motivo")
            return
        # primer arg puede ser @username o id
        first = context.args[0]
        rest = context.args[1:]
        reason = " ".join(rest).strip() if rest else "(sin motivo especificado)"
        if first.startswith("@"):
            uname = first[1:]
            try:
                # intentar resolver username en el chat
                # get_chat_member requiere id; usamos getChatAdministrators? fallback: buscar entre miembros no disponible, así que intentamos get_chat_member con username (no soportado), así que guardamos username textualmente
                target_user = type("U", (), {"id": None, "first_name": uname, "username": uname})()
            except Exception:
                target_user = type("U", (), {"id": None, "first_name": uname, "username": uname})()
        else:
            # Try numeric id
            try:
                uid = int(first)
                # obtener info del usuario en el chat
                try:
                    cu = await context.bot.get_chat_member(chat.id, uid)
                    target_user = cu.user
                except Exception:
                    target_user = type("U", (), {"id": uid, "first_name": str(uid), "username": None})()
            except Exception:
                await msg.reply_text("Usuario inválido. Usa @usuario o responde al mensaje.")
                return

    # Persistir reporte en DB
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO reports (reporter_id, reporter_name, reported_id, reported_name, chat_id, reason, created_at, handled) VALUES (?, ?, ?, ?, ?, ?, ?, 0)",
            (
                user.id,
                user.first_name or "",
                getattr(target_user, "id", None),
                getattr(target_user, "first_name", getattr(target_user, "username", "")),
                chat.id,
                reason,
                datetime.utcnow().isoformat(),
            ),
        )
        conn.commit()
        rid = cur.lastrowid
    except Exception as e:
        print(f"⚠️ Error guardando reporte: {e}")
        await msg.reply_text("⚠️ Error al guardar el reporte.")
        return
    finally:
        try:
            conn.close()
        except Exception:
            pass

    await msg.reply_text(f"✅ Reporte guardado (id={rid}). Los administradores pueden gestionarlo desde el backend.")
    # Avisar en grupo a los administradores (opcional): publicar breve aviso
    try:
        await context.bot.send_message(
            chat_id=chat.id,
            text=(f"🚨 Reporte registrado por [{user.first_name}](tg://user?id={user.id}) contra "
                  f"{getattr(target_user, 'first_name', getattr(target_user, 'username', 'desconocido'))} — id={rid}\n"
                  f"Motivo: {reason}"),
            parse_mode=ParseMode.MARKDOWN,
            disable_notification=True,
        )
    except Exception:
        pass


async def _maybe_react_emotion(msg, text):
    """Detecta emociones en el chat y reacciona con texto + GIF."""
    global last_emotion_at
    now = datetime.now(TZ)
    if last_emotion_at and (now - last_emotion_at) < timedelta(minutes=15):
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
    # 25% de probabilidad para no spamear
    if random.random() > 0.25:
        return


    last_emotion_at = now
    edata = EMOTION_REACTIONS[detected]


    # Enviar texto de reacción
    response = random.choice(edata["responses"])
    await msg.reply_text(response)


    # Intentar enviar un GIF de reacción (bonus, no crítico)
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.images(
                f"{edata['gif_query']} gif",
                max_results=8,
            ))
        gif_urls = [
            r["image"] for r in results
            if r.get("image", "").lower().endswith(".gif")
        ]
        if gif_urls:
            gif_url = random.choice(gif_urls[:5])
            await msg.reply_animation(animation=gif_url)
    except Exception:
        pass  # El texto ya se envió, el GIF es un bonus


# =========================
# COMANDOS
# =========================


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
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
        "⏰ *Utilidades*\n"
        "/recordar — Recordatorio personal\n"
        "  Ej: `/recordar 2h comprar ETH`\n\n"
        "💬 *Mencioname:*\n"
        "`BeeXy ¿qué es DeFi?`\n"
        "`BeeXy dibujame un gato astronauta`\n"
        "`BeeXy buscame una foto de bitcoin`\n\n"
        "🤖 *Automático:* resumen diario 10am, noticias lunes 11am, "
        "efemérides, datos curiosos, memes y trivias.",
        parse_mode=ParseMode.MARKDOWN
    )


async def rules_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡 Nunca compartas tu seed phrase.\n"
        "🛡 Nadie te escribirá por privado primero.",
        parse_mode=ParseMode.MARKDOWN
    )


async def faq_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
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


async def meme_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    meme_file, caption = random.choice(MEMES)
    image_path = os.path.join(MEMES_DIR, meme_file)
    if os.path.exists(image_path):
        with open(image_path, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=caption,
            )
    else:
        await update.message.reply_text(caption)


async def trivia_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = random.choice(TRIVIAS)
    await context.bot.send_poll(
        chat_id=update.effective_chat.id,
        question=t["q"],
        options=t["options"],
        type="quiz",
        correct_option_id=t["correct"],
        is_anonymous=False,
        explanation=t["explain"],
    )


async def poll_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q, opts = random.choice(POLLS)
    await context.bot.send_poll(
        chat_id=update.effective_chat.id,
        question=q,
        options=opts,
        is_anonymous=False
    )


async def ask_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /ask - el usuario hace una pregunta a la IA."""
    if not context.args:
        await update.message.reply_text(
            "🤖 Usá el comando así:\n`/ask ¿qué es una seed phrase?`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    question = " ".join(context.args)
    thinking_msg = await update.message.reply_text("🤖 Pensando...")
    user_name = (update.effective_user.username or update.effective_user.first_name or "")
    answer = await ask_ai(update.effective_user.id, question, user_name)
    await thinking_msg.edit_text(answer)




async def _handle_image_request(msg, action: str, topic: str):
    """Maneja pedidos de búsqueda o generación de imagen."""
    if action == "generate":
        # Si pide generar una persona real → buscar foto real
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
                    photo=photo,
                    caption=f"🔍 Resultado para: _{topic}_",
                    parse_mode=ParseMode.MARKDOWN,
                )
            else:
                await msg.reply_photo(
                    photo=photo,
                    caption=f"🎨 *Generado por BeeXy*\n_{topic}_",
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
            await msg.reply_photo(
                photo=photo,
                caption=f"🔍 {title}",
            )
        else:
            await thinking.edit_text("😕 No encontré imágenes. Probá con otras palabras.")




async def imagen_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /imagen - busca y envía una imagen de la web."""
    if not context.args:
        await update.message.reply_text(
            "🔍 Usá el comando así:\n`/imagen gato con bitcoin`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return
    query = " ".join(context.args)
    await _handle_image_request(update.message, "search", query)




async def generar_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /generar - genera una imagen con IA."""
    if not context.args:
        await update.message.reply_text(
            "🎨 Usá el comando así:\n`/generar un astronauta en la luna con bitcoin`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return
    prompt = " ".join(context.args)
    await _handle_image_request(update.message, "generate", prompt)


async def recordar_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
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


    # Persistir el recordatorio en la base y obtener su id
    try:
        scheduled_at = int(datetime.utcnow().timestamp()) + int(seconds)
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO reminders (user_id, user_name, chat_id, text, scheduled_at, created_at, fired) VALUES (?, ?, ?, ?, ?, ?, 0)",
            (user.id, user_name, chat_id, reminder_text, scheduled_at, datetime.utcnow().isoformat()),
        )
        conn.commit()
        reminder_id = cur.lastrowid
    except Exception:
        reminder_id = None
    finally:
        try:
            conn.close()
        except Exception:
            pass

    context.job_queue.run_once(
        reminder_fire,
        when=seconds,
        data={"chat_id": chat_id, "user_id": user.id, "user_name": user_name, "text": reminder_text, "reminder_id": reminder_id},
        name=f"reminder_{user.id}_{int(datetime.now().timestamp())}",
    )


    await update.message.reply_text(
        f"✅ Te recuerdo en *{display}*:\n_{reminder_text}_",
        parse_mode=ParseMode.MARKDOWN,
    )


# =========================
# MENSAJES
# =========================


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_scam_alert_at


    msg = update.effective_message
    if not msg or not msg.text:
        return


    text = msg.text


    if contains_wallet_keywords(text):
        now = datetime.now(TZ)
        if (last_scam_alert_at is None) or (
            now - last_scam_alert_at > timedelta(minutes=SCAM_ALERT_COOLDOWN_MIN)
        ):
            last_scam_alert_at = now
            await msg.reply_text(
                SCAM_ALERT,
                parse_mode=ParseMode.MARKDOWN
            )


    # Detectar mención por @username o por nombre "beexy"
    me = await context.bot.get_me()
    bot_mention = f"@{me.username}".lower()
    text_lower = text.lower()
    mentioned = bot_mention in text_lower or "beexy" in text_lower
    if mentioned:
        # Extraer la pregunta sin la mención
        question = text_lower.replace(bot_mention, "").replace("beexy", "").strip()
        if len(question) < 3:
            await msg.reply_text(
                "🐝 ¡Hola! Soy *BeeXy*. Preguntame lo que quieras.\n"
                "Ejemplo: `BeeXy ¿qué es DeFi?`\n"
                "También puedo buscar o generar imágenes 🎨",
                parse_mode=ParseMode.MARKDOWN
            )
            return


        # Detectar pedido de imagen
        img_req = detect_image_request(question)
        if img_req:
            action, topic = img_req
            await _handle_image_request(msg, action, topic)
            return


        thinking_msg = await msg.reply_text("🐝 Pensando...")
        user_name = (update.effective_user.username or update.effective_user.first_name or "")
        answer = await ask_ai(update.effective_user.id, question, user_name)
        await thinking_msg.edit_text(answer)
        return


    # Reacciones emocionales (solo para mensajes NO dirigidos al bot)
    await _maybe_react_emotion(msg, text)


# =========================
# MAIN
# =========================


def main():
    print("🐝 Iniciando BeeXy - Beexo Telegram Bot...")
    print(f"📍 Chat ID objetivo: {TARGET_CHAT_ID}")
    print(f"🌍 Zona horaria: {TZ}")
    
    async def post_init(application):
        await application.bot.set_my_commands([
            BotCommand("help", "Menu de ayuda"),
            BotCommand("rules", "Reglas del grupo"),
            BotCommand("faq", "Preguntas frecuentes"),
            BotCommand("ask", "Preguntale a BeeXy"),
            BotCommand("imagen", "Buscar una imagen"),
            BotCommand("generar", "Generar imagen con IA"),
            BotCommand("meme", "Meme random"),
            BotCommand("trivia", "Trivia cripto"),
            BotCommand("poll", "Encuesta"),
            BotCommand("recordar", "Recordatorio personal"),
        ])
        print("Comandos registrados en el menu de Telegram")
        # Reprogramar recordatorios pendientes almacenados en la base
        try:
            now_ts = int(datetime.utcnow().timestamp())
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT id, chat_id, user_id, user_name, text, scheduled_at FROM reminders WHERE fired=0 AND scheduled_at IS NOT NULL")
            rows = cur.fetchall()
            for r in rows:
                rid, chat_id, user_id, user_name, text, scheduled_at = r
                remaining = int(scheduled_at) - now_ts
                if remaining <= 0:
                    remaining = 1
                application.job_queue.run_once(
                    reminder_fire,
                    when=remaining,
                    data={"chat_id": chat_id, "user_id": user_id, "user_name": user_name, "text": text, "reminder_id": rid},
                    name=f"reminder_{rid}",
                )
            if rows:
                print(f"🔁 Reprogramados {len(rows)} recordatorios pendientes")
        except Exception as e:
            print(f"⚠️ Error reprogramando recordatorios: {e}")
        finally:
            try:
                conn.close()
            except Exception:
                pass


    app = Application.builder().token(TOKEN).post_init(post_init).build()


    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("rules", rules_cmd))
    app.add_handler(CommandHandler("faq", faq_cmd))
    app.add_handler(CommandHandler("meme", meme_cmd))
    app.add_handler(CommandHandler("trivia", trivia_cmd))
    app.add_handler(CommandHandler("poll", poll_cmd))
    app.add_handler(CommandHandler("ask", ask_cmd))
    app.add_handler(CommandHandler("imagen", imagen_cmd))
    app.add_handler(CommandHandler("generar", generar_cmd))
    app.add_handler(CommandHandler("recordar", recordar_cmd))
    app.add_handler(CommandHandler("report", report_cmd))


    # Bienvenida a nuevos miembros (doble handler: chat_member + fallback service msg)
    app.add_handler(ChatMemberHandler(track_chat_member, ChatMemberHandler.CHAT_MEMBER))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))


    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))


    # --- Jobs programados ---
    app.job_queue.run_daily(morning_job, time=time(8, 0, tzinfo=TZ))
    app.job_queue.run_daily(night_job, time=time(22, 0, tzinfo=TZ))
    app.job_queue.run_daily(engagement_job, time=time(19, 30, tzinfo=TZ), days=(0,2,4,6))


    # Memes diarios: planificador a las 00:05 elige 2 horarios random por día
    app.job_queue.run_daily(schedule_daily_memes, time=time(0, 5, tzinfo=TZ))
    app.job_queue.run_once(schedule_daily_memes, when=5, name="memes_hoy")


    # Resumen diario de cripto a las 10:00
    app.job_queue.run_daily(daily_crypto_summary_job, time=time(10, 0, tzinfo=TZ))


    # Efemérides cripto: chequea todos los días a las 09:30
    app.job_queue.run_daily(ephemerides_job, time=time(9, 30, tzinfo=TZ))


    # Dato curioso semanal: miércoles a las 15:00
    app.job_queue.run_daily(weekly_fun_fact_job, time=time(15, 0, tzinfo=TZ), days=(2,))


    # Noticias semanales: lunes a las 11:00
    app.job_queue.run_daily(weekly_news_job, time=time(11, 0, tzinfo=TZ), days=(0,))


    # Meme cripto en vivo: primero en 1-6h, luego cada ~24h a hora aleatoria
    crypto_delay = random.uniform(1, 6) * 3600
    app.job_queue.run_once(crypto_news_meme_job, when=crypto_delay, name="crypto_meme")
    print(f"📰 Primer meme cripto en {crypto_delay/3600:.1f} horas")


    # Trivia automática: primera en 6-24h, luego cada ~2 días a hora aleatoria
    trivia_delay = random.uniform(6, 24) * 3600
    app.job_queue.run_once(auto_trivia_job, when=trivia_delay, name="auto_trivia")
    print(f"🧩 Primera trivia auto en {trivia_delay/3600:.1f} horas")


    print("✅ Bot configurado. Iniciando polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
    print("❌ Bot detenido.")


if __name__ == "__main__":
    main()
