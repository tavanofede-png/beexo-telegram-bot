import asyncio
import sys

sys.path.insert(0, './beexo-telegram-bot')
from jobs import beexo_radio_job
from db import init_db

class DummyBot:
    async def send_message(self, chat_id, text, parse_mode):
        print(f"SENDING to {chat_id}:\n{text}")

class DummyContext:
    def __init__(self):
        self.bot = DummyBot()

async def run():
    init_db()
    ctx = DummyContext()
    await beexo_radio_job(ctx)

if __name__ == "__main__":
    asyncio.run(run())
