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

@bot.on_message(filters.command('start'))
async def start(bot, message):
    await message.reply_text("Send Any 1tamilmv.com Link")


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
        await message.reply(f"https://videovard.sx/e/{short_link}", quote=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


async def get_shortlink(link):
    url = 'https://api.videovard.sx/v2/api/remote/add'
    params = {'key': API_KEY, 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True) as response:
            data = await response.json()
            return data["filecode"]      

print("Bot running...")

bot.run()
