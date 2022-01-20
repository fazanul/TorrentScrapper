import aiohttp
from pyrogram import filters, Client
from config import  API_KEY
from main import bot

@Client.on_message(filters.regex(r'https://t2links\.kevin-264\.workers\.dev/0:/'))
async def link_handler(bot, message):
    link = str(message.text)
    try:
        short_link = await get_shortlink(link)
        await message.reply(f"<code>https://videovard.sx/e/{short_link}</code>", quote=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


async def get_shortlink(link):
    url = 'https://api.videovard.sx/v2/api/remote/add'
    params = {'key': API_KEY, 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
            data = await response.json()
            result = data["result"]
            return result["filecode"]
