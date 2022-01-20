# (c) @ask_admin001

import random
import os
import aiohttp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import MessageEmpty
from config import API_ID, API_HASH, BOT_TOKEN
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

options = webdriver.ChromeOptions()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-infobars")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)

bot = Client(
    "Web Scrapping Bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
)

torrent = []
API_KEY = "3239u7cq042faca6z1m5"

reply_markup = InlineKeyboardMarkup(
    [
        [  # First row
            InlineKeyboardButton(  # Generates a callback query when pressed
                "1TamilMV",
                callback_data="1tamilmv"
            ),
            InlineKeyboardButton(  # Opens a web URL
                "TamilBlasters",
                callback_data="tamilblasters"
            ),
        ]
    ]
)


@bot.on_message(filters.command('start'))
async def start(bot, message):
    await message.reply_text("Send any 1tamilmv.com or tamilblasters.com link to scrap torrents")


@bot.on_message(filters.regex("index\.php\?/forums/topic"))
async def link_regex(bot, message):
    try:
        txt = await message.reply_text("Scrapping torrent link, Please Wait")
        link = str(message.text)
        driver.get(link)
        torrent_link = driver.find_elements(By.CLASS_NAME, "ipsAttachLink_block")
        try:
            title = driver.find_element(By.XPATH, '//h1').text
        except NoSuchElementException:
            title = ""
        heading = f"**{title}**\n\n"
        msg = ""
        command = ['/qbleechfile', '/qbleechfile2', "/qbleechvideo"]
        random_command = random.choice(command)
        for link in torrent_link:
            tor = link.get_attribute("href")
            text = link.text
            msg += f"**Name : {text}**\n**Link:** `{random_command} {tor}`\n\n-\n\n"
        reply_text = f"{heading} + {msg} + **--@T2Links**"
        await message.reply_text(heading+msg)
        await txt.delete()
    except MessageEmpty:
        await message.reply_text('Some error occurred')
        await txt.delete()

        
        
@bot.on_message(filters.regex(r'https://t2links\.kevin-264\.workers\.dev/0:/'))
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

        
@bot.on_message(filters.command('list'))
async def lists(c, m):
    querys = ""
    length = len(m.command)
    for query in m.command[1:length]:
        querys += f"{query} "
    txt = await m.reply_text(m.chat.id, "Choose the website you want to search!", reply_markup=reply_markup)

    @bot.on_callback_query()
    async def cb_handler(client, query):
        await query.message.edit_text(f"Searching For: {querys}")
        texts = ""
        command = ""
        if query.data == "1tamilmv":
            await query.answer()
            command += "1tamilmv"
        elif query.data == "tamilblasters":
            await query.answer()
            command += "tamilblasters"
        link = f"https://www.{command}.com/index.php?/search/&q={querys}&search_and_or=and&search_in=titles&sortby=relevancy"
        driver.get(link)
        await asyncio.sleep(10)
        title = driver.title
        links = driver.find_elements(By.TAG_NAME, "h2")
        msg = []
        count = 0
        try:
            for link in links:
                text = link.text
                url = driver.find_element(By.LINK_TEXT, text).get_attribute("href")
                count += 1
                msgs = f"{count}. [{text}]({url})\n\n"
                msg.append(msgs)
        except NoSuchElementException:
            pass

        for text in msg[0:20]:
            texts += text
        reply = f"**{title}**\n\n{texts}"
        await c.send_message(m.chat.id, reply, disable_web_page_preview=True)
        await txt.delete() 
    
   

print("Bot running...")
bot.run()
