from pyrogram import Client, filters


@Client.on_message(filters.command('start'))
async def start(bot, message):
    await message.reply_text("Send any 1tamilmv.com or tamilblasters.com link to scrap torrents")
