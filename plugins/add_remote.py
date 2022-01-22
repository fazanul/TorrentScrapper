#t.me/ask_admin001


import aiohttp
from pyrogram import Client, filters
from config import API_KEY


@Client.on_message(filters.command('add_remote'))
async def link_handler(bot, message):
    try:
        reply_message = message.reply_to_message.text
        if reply_message:
            link = reply_message
        elif not reply_message:
            link = str(message.command[1])
        short_link = await get_shortlink(link)
        await message.reply(f"<code>https://videovard.sx/e/{short_link}</code>", quote=True)
    except IndexError as e:
        await message.reply(f'`/add_remote [link]`', quote=True, disable_web_page_preview=True)


async def get_shortlink(link):
    url = 'https://api.videovard.sx/v2/api/remote/add'
    params = {'key': API_KEY, 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
            data = await response.json()
            result = data["result"]
            return result["filecode"]
