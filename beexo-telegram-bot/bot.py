"""
BeeXy — Beexo Community Telegram Bot.
Punto de entrada: ensambla handlers, jobs y arranca el bot.
"""

from datetime import time

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ChatMemberHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import TOKEN, TARGET_CHAT_IDS, TZ, logger
from db import init_db, get_pending_reminders
from handlers import (
    on_message,
    welcome_new_member,
    track_chat_member,
    reminder_fire,
)
from commands import (
    help_cmd,
    rules_cmd,
    faq_cmd,
    meme_cmd,
    trivia_cmd,
    poll_cmd,
    ask_cmd,
    imagen_cmd,
    generar_cmd,
    recordar_cmd,
    report_cmd,
    precio_cmd,
    id_cmd,
    top_cmd,
    me_cmd,
)
from jobs import (
    morning_job,
    night_job,
    engagement_job,
    auto_trivia_job,
    time_until,
)


# ═══════════════════════════════════════════════════════════════
# POST INIT — cachear bot_info y preparar la DB
# ═══════════════════════════════════════════════════════════════

async def post_init(app) -> None:
    """Se ejecuta una vez al iniciar el bot."""
    # Cachear get_me() para no llamarlo en cada mensaje
    bot_info = await app.bot.get_me()
    app.bot_data["bot_info"] = bot_info
    logger.info("🤖 Bot info cacheado: @%s (id=%s)", bot_info.username, bot_info.id)

    # Inicializar DB
    init_db()

    # Inicializar pool de memes
    from meme_pool import init_pool
    pool_count = init_pool()
    logger.info("🎭 Pool de memes listo: %d memes disponibles", pool_count)

    # Reprogramar recordatorios pendientes
    import time as time_mod
    now = int(time_mod.time())
    for r in get_pending_reminders():
        delay = r["scheduled_at"] - now
        if delay <= 0:
            delay = 5  # disparar en 5 segundos si ya pasó la hora
        app.job_queue.run_once(
            reminder_fire, when=delay,
            data={
                "chat_id": r["chat_id"], "user_id": r["user_id"],
                "user_name": r["user_name"], "text": r["text"],
                "reminder_id": r["id"],
            },
            name=f"reminder_{r['user_id']}_{r['id']}",
        )
    logger.info("⏰ Recordatorios pendientes reprogramados")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main() -> None:
    logger.info("🚀 Iniciando BeeXy…")

    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    # ── Comandos ──
    app.add_handler(CommandHandler("start", help_cmd))
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
    app.add_handler(CommandHandler("precio", precio_cmd))
    app.add_handler(CommandHandler("id", id_cmd))
    app.add_handler(CommandHandler("top", top_cmd))
    app.add_handler(CommandHandler("me", me_cmd))

    # ── Mensajes ──
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        on_message,
    ))
    app.add_handler(MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS,
        welcome_new_member,
    ))
    app.add_handler(ChatMemberHandler(
        track_chat_member,
        ChatMemberHandler.CHAT_MEMBER,
    ))

    # ── Jobs programados ──
    jq = app.job_queue

    jq.run_daily(morning_job, time=time(8, 30, tzinfo=TZ), name="morning")
    jq.run_daily(night_job, time=time(23, 0, tzinfo=TZ), name="night")
    jq.run_daily(engagement_job, time=time(16, 0, tzinfo=TZ), name="engagement")
    jq.run_daily(daily_crypto_summary_job, time=time(10, 0, tzinfo=TZ), name="crypto_summary")
    jq.run_daily(ephemerides_job, time=time(12, 0, tzinfo=TZ), name="ephemerides")

    jq.run_daily(weekly_news_job, time=time(11, 0, tzinfo=TZ),
                 days=(0,), name="weekly_news")  # 0 = lunes
    jq.run_repeating(weekly_fun_fact_job, interval=5 * 86400,
                     first=time_until(time(15, 0, tzinfo=TZ)), name="fun_fact")

    jq.run_once(auto_trivia_job,
                when=time_until(time(18, 0, tzinfo=TZ)), name="auto_trivia")

    logger.info("✅ BeeXy listo — %d chats configurados", len(TARGET_CHAT_IDS))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
