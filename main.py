import asyncio
import unicodedata
from datetime import datetime, timezone
from telethon import TelegramClient, events

api_id = YOUR API ID
api_hash = 'YOUR API HASH'

client = TelegramClient('anon', api_id, api_hash)

KHMER_GREETINGS = [
    'សួស្ដី', 'សួស្តី', 'ហេឡូ', 'អរុណសួស្តី',
    'រាត្រីសួស្តី', 'ទិវាសួស្តី', 'សុខសប្បាយទេ',
    'ជម្រាបសួរ'
]

def has_emoji(text):
    for char in text:
        if unicodedata.category(char) in ('So', 'Sm') or ord(char) > 127:
            return True
    return False

# Track when YOU last sent a message per chat
last_sent = {}

@client.on(events.NewMessage(outgoing=True, func=lambda e: e.is_private))
async def track_my_messages(event):
    last_sent[event.chat_id] = datetime.now(timezone.utc)

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def my_event_handler(event):
    chat_id = event.chat_id
    now = datetime.now(timezone.utc)

    # If you sent a message in last 60 seconds, don't auto reply
    if chat_id in last_sent:
        seconds_since = (now - last_sent[chat_id]).total_seconds()
        if seconds_since < 60:
            return

    text = event.raw_text.lower() if event.raw_text else ""

    has_greeting = 'hello' in text or 'hi' in text
    has_khmer    = any(word in event.raw_text for word in KHMER_GREETINGS) if event.raw_text else False
    has_sticker  = event.sticker is not None
    has_voice    = event.voice is not None
    has_media    = event.photo or event.gif or event.video or event.audio or event.document
    emoji_only   = has_emoji(text) if text else False

    if has_greeting or has_khmer or has_sticker or has_voice or has_media or emoji_only:
        await event.reply('Hello Bong , ជម្រាបសួរបង , ខ្ញុំប្រហែលជារវុលបន្ដិចទៀតខ្ញុំនឹងតបបងវិញ អគុណបង!')

async def main():
    await client.start()
    me = await client.get_me()
    print(f"✅ Logged in as: {me.first_name} (@{me.username})")
    print("👂 Listening for private messages...")
    await client.run_until_disconnected()

asyncio.run(main())
