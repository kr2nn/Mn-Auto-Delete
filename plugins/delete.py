# @MrMNTG Or @MusammilN
from pyrogram import Client, filters
import asyncio
from pyrogram.errors import FloodWait
from config import CHATS

# Catch all group messages (including bot messages and admin messages)
all_filters = filters.group

@Client.on_message(all_filters)
async def auto_delete_handler(client, message):
    # Skip if chat is not in the allowed list
    if CHATS.IDS and message.chat.id not in CHATS.IDS:
        return

    delay = CHATS.DELETE_DELAY  # in seconds

    try:
        # Check if sender is an admin
        is_admin = False
        if message.from_user:
            member = await client.get_chat_member(message.chat.id, message.from_user.id)
            is_admin = member.status in ("administrator", "creator")

        # Only proceed if message is not from an admin or if you want to delete admin messages too
        if is_admin or message.from_user is None:
            print(f"Admin/Bot message scheduled: chat {message.chat.id}, message {message.id}")
        else:
            print(f"User message scheduled: chat {message.chat.id}, message {message.id}")

        await asyncio.sleep(delay)

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
