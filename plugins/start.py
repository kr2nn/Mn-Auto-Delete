from pyrogram import Client, filters

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    await message.reply_text("Hey! This bot only works in its specific groups. Dev @MrMNTG ") # don't remove Dev @MrMNTG 
