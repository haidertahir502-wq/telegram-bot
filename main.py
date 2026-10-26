import os, asyncio, logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession

logging.basicConfig(level=logging.INFO)
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
SESSION = os.getenv("SESSION_STRING", "")
SOURCES = [s.strip() for s in os.getenv("SOURCE_CHANNELS", "").split(",") if s.strip()]
TARGET = os.getenv("TARGET_CHANNEL", "")
KEYWORDS = [k.lower() for k in os.getenv("KEYWORDS", "").split(",") if k]

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCES))
async def handler(event):
    text = (event.message.message or "").lower()
    if KEYWORDS and not any(k in text for k in KEYWORDS):
        return
    await client.forward_messages(TARGET, event.message)

async def main():
    await client.start()
    print("Bot started!")
    await client.run_until_disconnected()

asyncio.run(main())
