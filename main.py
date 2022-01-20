# (c) @ask_admin001

import os
import aiohttp
import asyncio
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import MessageEmpty
from config import API_ID, API_HASH, BOT_TOKEN

driver = webdriver.Chrome(executable_path="/Users/kevinnadar/Desktop/chromedriver")

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
        reply_text = f"{heading}{msg}**--@T2Links**"
        await message.reply_text(reply_text)
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


@bot.on_message(filters.command('listmv'))
async def lists(c, m):
    querys = ""
    texts = ""
    length = len(m.command)
    for queryss in m.command[1:length]:
        querys += f"{queryss} "
    link = f"https://www.1tamilmv.com/index.php?/search/&q={querys}&search_and_or=and&search_in=titles&sortby=relevancy"
    txt = await m.reply_text(f"Searching for: {querys} 🔍")
    driver.get(link)
    await asyncio.sleep(5)
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


@bot.on_message(filters.command('listbl'))
async def lists(c, m):
    querys = ""
    texts = ""
    length = len(m.command)
    for queryss in m.command[1:length]:
        querys += f"{queryss} "
    link = f"https://www.tamilblasters.com/index.php?/search/&q={querys}&search_and_or=and&search_in=titles&sortby=relevancy"
    txt = await m.reply_text(f"Searching for: {querys} 🔍")
    driver.get(link)
    await asyncio.sleep(5)
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
