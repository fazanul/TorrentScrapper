# (c) @ask_admin001

import time
import os
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
        heading = f"{title}\n\n"
        msg = ""
        for link in torrent_link:
            tor = link.get_attribute("href")
            text = link.text
            msg += f"**Name : {text}**\n**Torrent:** `{tor}`\n\n-----------------\n\n"
        await message.reply_text(heading + msg)
        await txt.delete()
    except MessageEmpty:
        await message.reply_text('Some error occurred')
        await txt.delete()


print("Bot running...")
bot.run()
