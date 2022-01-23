#t.me/ask_admin001


import aiohttp
from pyrogram import Client, filters
from config import API_KEY


#Rename Files in VideoVard
@Client.on_message(filters.command('rename_file'))
async def get_files(bot, message):
    async with aiohttp.ClientSession() as session:
        try:
            print(len(message.command))
            lens = len(message.command) + 1
            print(lens)
            titles = ""
            for i in message.command[2:lens]:
                titles += i + " "
                print(titles)
            print(titles)
            file_code = str(message.command[1])
            url = 'https://api.videovard.sx/v2/api/file/rename'
            params = {'key': API_KEY,
                      'title': titles,
                      'file_code': file_code
                      }
            info = await file_info(file_code)
            async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
                data = await response.json()
            await message.reply_text(f"{info} renamed to [{titles}](https://videovard.sx/e/{file_code})")
        except Exception:
            await message.reply_text("<code>/rename_file [file_code] [title]</code>", quote=True, disable_web_page_preview=True)


async def file_info(file_code):
    url = 'https://api.videovard.sx/v2/api/file/info'
    params = {'key': API_KEY, 'file_code': file_code}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
            data = await response.json()
            result = data["result"]
            for i in result:
                name = i["name"]
            print(name)

            return name
