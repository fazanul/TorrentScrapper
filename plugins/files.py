#t.me/ask_admin001


import aiohttp
from pyrogram import Client, filters
from config import API_KEY


#Latest Files in VideoVard
@Client.on_message(filters.command('files'))
async def files(bot, message):
    if API_KEY:
        async with aiohttp.ClientSession() as session:
            msg = ""
            url = 'https://api.videovard.sx/v2/api/file/list'
            params = {'key': API_KEY,
                      'page': 1,
                      'per_page': 20,
                      }
            async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:

                data = await response.json()
                print(data)
                result = data["result"]
                file1 = result["files"]
                count = 0
                for file in file1:
                    count += 1
                    title = str(file["title"])
                    filecode = file["file_code"]
                    filelink = f"https://videovard.sx/e/{filecode}"
                    title1 = title.replace("'", "")
                    print(title1)
                    msg += f"{count}. <a href={filelink}>{title1}</a> - <code>{filecode}</code>\n\n"
                await message.reply_text(msg, quote=True, disable_web_page_preview=True)
