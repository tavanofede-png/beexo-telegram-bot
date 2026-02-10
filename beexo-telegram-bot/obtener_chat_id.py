import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

load_dotenv()

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

async def show_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra el ID del chat cuando recibe un mensaje"""
    chat = update.effective_chat
    user = update.effective_user
    
    info = f"""
📋 *Información del Chat*

🆔 Chat ID: `{chat.id}`
👤 Usuario: {user.first_name}
🔢 User ID: `{user.id}`
📝 Tipo: {chat.type}
"""
    
    if chat.title:
        info += f"📛 Nombre del grupo: {chat.title}\n"
    
    info += f"\n✅ Usa este Chat ID en tu archivo .env:\n`TARGET_CHAT_ID={chat.id}`"
    
    await update.message.reply_text(info, parse_mode="Markdown")
    print(f"\nChat ID: {chat.id}")
    print(f"Chat Type: {chat.type}")
    if chat.title:
        print(f"Group Name: {chat.title}")

def main():
    print("🤖 Bot iniciado. Envía un mensaje al bot (privado o en grupo) para ver el Chat ID.")
    print("Presiona Ctrl+C para detener.\n")
    
    app = Application.builder().token(TOKEN).build()
    
    # Captura todos los mensajes de texto
    app.add_handler(MessageHandler(filters.ALL, show_chat_id))
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
