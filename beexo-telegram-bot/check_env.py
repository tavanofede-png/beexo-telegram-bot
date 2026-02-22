from dotenv import load_dotenv
import os

load_dotenv(".env")

token = os.getenv("TELEGRAM_BOT_TOKEN")
target_chat = os.getenv("TARGET_CHAT_ID")
memes_chat = os.getenv("MEMES_CHAT_ID")

print("--- ENV CHECK ---")
if token:
    print(f"Token Found: Yes")
    print(f"Length: {len(token)}")
    print(f"Prefix: {token[:10]}...")
    print(f"Has spaces: {' ' in token}")
    print(f"Has quotes embedded: {'\"' in token or '\'' in token}")
else:
    print("Token Found: NO")

print(f"Target Chat: {target_chat}")
print(f"Memes Chat: {memes_chat}")
