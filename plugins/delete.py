# @MrMNTG Or @MusammilN
from pyrogram import Client, filters
import asyncio
from config import CHATS

@Client.on_message(filters.group)
async def auto_delete_handler(client, message):
    if message.chat.id not in CHATS.IDS:
        return
    delay = CHATS.DELETE_DELAY
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception as e:
        print(f"Failed to delete message: {e}")
