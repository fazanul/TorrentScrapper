# (c) @ask_admin001

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import MessageEmpty, MessageNotModified
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
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
reply_markup = InlineKeyboardMarkup(
    [
        [  # First row
            InlineKeyboardButton(  # Generates a callback query when pressed
                "/qbleechfile",
                callback_data="qbleechfile"
            ),
            InlineKeyboardButton(  # Opens a web URL
                "/qbmirror",
                callback_data="qbmirror"
            ),
        ],
        [  # Second row
            InlineKeyboardButton(  # Opens the inline interface
                "/qbleechvideo",
                callback_data="qbleechvideo"
            ),
            InlineKeyboardButton(  # Opens the inline interface in the current chat
                "/qbmirror2",
                callback_data="qbmirror2"
            )
        ],
        [  # Third row
            InlineKeyboardButton(  # Opens the inline interface
                "/qbleechfile2",
                callback_data="qbleechfile2"
            ),
            InlineKeyboardButton(  # Opens the inline interface in the current chat
                "/qbmirror3",
                callback_data="qbmirror3"
            )
        ]
    ]
)


@bot.on_message(filters.command('start'))
async def start(bot, message):
    await message.reply_text("Send Any 1tamilmv.com Link")


@bot.on_message(filters.regex("index\.php\?/forums/topic"))
async def link_regex(bot, message):
    try:
        txt = await bot.send_message(message.chat.id, "Loading... Please Wait !!!")
        link = str(message.text)
        driver.get(link)
        torrent_link = driver.find_elements(By.CLASS_NAME, "ipsAttachLink_block")
        try:
            title = driver.find_element(By.XPATH, '//h1').text
        except NoSuchElementException:
            title = ""
        heading = f"**{title}**\n\n"
        await txt.delete()
        txt = await bot.send_message(message.chat.id, "Select the Command", reply_markup=reply_markup)
        @bot.on_callback_query()
        async def callback(c, m):
            try:
                if m.data == "qbmirror3":                    
                    msg = ""
                    random_command = "/qbmirror3"
                    for link in torrent_link:
                        tor = link.get_attribute("href")
                        text = link.text
                        msg += f"**Name : {text}**\n**Link:** `{random_command} {tor}`\n\n-\n\n"
                    reply_text = f"{heading} + {msg} + **--@T2Links**"
                    await m.message.reply_text(reply_text)

                elif m.data == "qbmirror2":
                    msg = ""
                    random_command = "/qbmirror2"
                    for link in torrent_link:
                        tor = link.get_attribute("href")
                        text = link.text
                        msg += f"**Name : {text}**\n**Link:** `{random_command} {tor}`\n\n-\n\n"
                    reply_text = f"{heading} + {msg} + **--@T2Links**"
                    await message.reply_text(reply_text)
                elif m.data == "qbmirror":
                    msg = ""
                    random_command = "/qbmirror"
                    for link in torrent_link:
                        tor = link.get_attribute("href")
                        text = link.text
                        msg += f"**Name : {text}**\n**Link:** `{random_command} {tor}`\n\n-\n\n"
                    reply_text = f"{heading} + {msg} + **--@T2Links**"
                    await message.reply_text(reply_text)
                elif m.data == "qbleechfile2":
                    msg = ""
                    random_command = "/qbleechfile2"
                    for link in torrent_link:
                        tor = link.get_attribute("href")
                        text = link.text
                        msg += f"**Name : {text}**\n**Link:** `{random_command} {tor}`\n\n-\n\n"
                    reply_text = f"{heading} + {msg} + **--@T2Links**"
                    await message.reply_text(reply_text)
                elif m.data == "qbleechvideo":
                    msg = ""
                    random_command = "/qbleechvideo"
                    for link in torrent_link:
                        tor = link.get_attribute("href")
                        text = link.text
                        msg += f"**Name : {text}**\n**Link:** `{random_command} {tor}`\n\n-\n\n"
                    reply_text = f"{heading} {msg} **--@T2Links**"
                    await message.reply_text(reply_text)
                elif m.data == "qbleechfile":
                    msg = ""
                    random_command = "/qbleechfile"
                    for link in torrent_link:
                        tor = link.get_attribute("href")
                        text = link.text
                        msg += f"**Name : {text}**\n**Link:** `{random_command} {tor}`\n\n-\n\n"
                    reply_text = f"{heading} {msg} **--@T2Links**"
                    await message.reply_text(reply_text)
                await txt.delete()
                driver.back()
            except MessageNotModified:
                await bot.send_message(message.chat.id, "Some error Occurred")

    except MessageEmpty:
        await message.reply_text('Some error occurred')
        await txt.delete()


print("Bot running...")
bot.run()
