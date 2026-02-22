"""Test: genera un meme con IA y lo envía al chat de memes."""
import asyncio
import os
import sys

# Cargar .env
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from crypto_news_meme import generate_news_meme


async def main():
    print("🚀 Generando meme de prueba con IA...")
    path, caption = await generate_news_meme()

    if not path:
        print("❌ No se pudo generar el meme")
        sys.exit(1)

    print(f"✅ Meme generado: {path}")
    print(f"📝 Caption:\n{caption}")

    # Enviar al chat de memes
    from telegram import Bot
    bot = Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
    chat_id = os.environ.get("MEMES_CHAT_ID", os.environ.get("TARGET_CHAT_ID"))

    print(f"\n📤 Enviando al chat {chat_id}...")
    with open(path, "rb") as photo:
        await bot.send_photo(
            chat_id=int(chat_id),
            photo=photo,
            caption=caption,
            parse_mode="Markdown",
        )
    print("✅ ¡Meme enviado!")


if __name__ == "__main__":
    asyncio.run(main())
