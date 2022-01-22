
#t.me/ask_admin001


import aiohttp
from pyrogram import Client, filters
from config import API_KEY


# Search Files in VideoVard
@Client.on_message(filters.command('get_files'))
async def get_files(bot, message):
    async with aiohttp.ClientSession() as session:
        try:
            try:
                reply_messages = message.reply_to_message.text
                title = reply_messages
            except AttributeError:
                title = str(message.command[1])
            msg = ""
            url = 'https://api.videovard.sx/v2/api/file/list'
            params = {'key': API_KEY,
                      'page': 1,
                      'per_page': 20,
                      'title': title,
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
                if msg == "":
                    await message.reply_text("No Movies Found", quote=True)
                elif msg != "":
                    await message.reply_text(msg, quote=True, disable_web_page_preview=True)
        except IndexError:
            await message.reply_text("<code>/get_files [query]</code>", quote=True, disable_web_page_preview=True)
