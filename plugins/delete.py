# @MrMNTG Or @MusammilN
from pyrogram import Client, filters
import asyncio
from pyrogram.errors import FloodWait
from config import CHATS

# Catch all group messages
all_filters = filters.group

@Client.on_message(all_filters)
async def auto_delete_handler(client, message):
    if CHATS.IDS and message.chat.id not in CHATS.IDS:
        return

    delay = CHATS.DELETE_DELAY  # in seconds

    print(f"Scheduling delete: chat {message.chat.id}, message {message.id}, user {message.from_user.id if message.from_user else 'N/A'}")

    await asyncio.sleep(delay)

    try:
        await message.delete()
        print(f"Deleted message {message.id} from chat {message.chat.id}")
    except FloodWait as fw:
        print(f"FloodWait: waiting {fw.value} seconds")
        await asyncio.sleep(fw.value)
        try:
            await message.delete()
        except Exception as e:
            print(f"Retry failed: {e}")
    except Exception as e:
        print(f"Delete error: {e}")
