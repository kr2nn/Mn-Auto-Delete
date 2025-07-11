# @MrMNTG Or @MusammilN
from pyrogram import Client, filters
import asyncio
from pyrogram.errors import FloodWait
from config import CHATS

# Define filters for media and bot's own messages
media_filters = filters.video | filters.document | filters.photo | filters.voice | filters.audio
all_filters = filters.group & (filters.text | media_filters | filters.me)

@Client.on_message(all_filters)
async def auto_delete_handler(client, message):
    # Skip if chat is not in the allowed list
    if CHATS.IDS and message.chat.id not in CHATS.IDS:
        return

    delay = CHATS.DELETE_DELAY

    print(f"Scheduling message from chat {message.chat.id} (user {message.from_user.id}) for deletion in {delay} seconds.")

    await asyncio.sleep(delay)

    try:
        await message.delete()
        print(f"Deleted message {message.message_id} from chat {message.chat.id}")
    except FloodWait as fw:
        print(f"FloodWait triggered: sleeping for {fw.value} seconds")
        await asyncio.sleep(fw.value)
        try:
            await message.delete()
        except Exception as e:
            print(f"Second delete attempt failed: {e}")
    except Exception as e:
        print(f"Error deleting message: {e}")
