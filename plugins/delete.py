# @MrMNTG Or @MusammilN 
from pyrogram import Client, filters
import asyncio
import os
from config import CHATS, OWNER
from pymongo import MongoClient
from bson import Int64
# @MrMNTG Or @MusammilN 

# MongoDB setup (Koyeb-compatible)
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["auto_delete_bot"]
settings_collection = db["settings"]
# @MrMNTG Or @MusammilN
# @MrMNTG Or @MusammilN
# Initialize default delay if not set
def get_delay(chat_id):
    setting = settings_collection.find_one({"chat_id": Int64(chat_id)})
    return setting["delay"] if setting else CHATS.DELETE_DELAY

# @MrMNTG Or @MusammilN
def set_delay(chat_id, delay):
    settings_collection.update_one(
        {"chat_id": Int64(chat_id)},
        {"$set": {"delay": delay}},
        upsert=True
    )
# @MrMNTG Or @MusammilN
@Client.on_message(filters.group & filters.command("setdelay") & filters.user(OWNER.ID))
async def set_delay_command(client, message):
    if message.chat.id not in CHATS.IDS:
        await message.reply("This chat is not authorized for auto-delete.")
        return
    try:
        delay = int(message.command[1])
        if delay < 0:
            await message.reply("Delay cannot be negative.")
            return
        set_delay(message.chat.id, delay)
        await message.reply(f"Auto-delete delay set to {delay} seconds.")
    except (IndexError, ValueError):
        await message.reply("Usage: /setdelay <seconds>")

# @MrMNTG Or @MusammilN
@Client.on_message(filters.group)
async def auto_delete_handler(client, message):
    if message.chat.id not in CHATS.IDS:
        return
    if message.text and message.text.startswith("/"):
        return
    delay = get_delay(message.chat.id)
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception as e:
        print(f"Failed to delete message: {e}")

# @MrMNTG Or @MusammilN
# @MrMNTG Or @MusammilN
# @MrMNTG Or @MusammilN
