# @MrMNTG Or @MusammilN
from pyrogram import Client, filters
import asyncio
from pyrogram.errors import FloodWait
from config import CHATS

@Client.on_message(filters.group)
async def auto_delete_handler(client, message):
    # If CHATS.IDS is not empty and this chat ID is not in the list, skip
    if CHATS.IDS and message.chat.id not in CHATS.IDS:
        return

    delay = CHATS.DELETE_DELAY
    await asyncio.sleep(delay)

    try:
        await message.delete()
    except FloodWait as fw:
        print(f"FloodWait hit: sleeping for {fw.value} seconds")
        await asyncio.sleep(fw.value)
        try:
            await message.delete()
        except Exception as e:
            print(f"Second attempt failed: {e}")
    except Exception as e:
        print(f"Failed to delete message: {e}")
