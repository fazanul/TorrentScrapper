import random
from main import bot, driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pyrogram import filters, Client
from pyrogram.errors.exceptions.bad_request_400 import MessageEmpty


@Client.on_message(filters.regex("index\.php\?/forums/topic"))
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
        await message.reply_text(reply_text)
        await txt.delete()
    except MessageEmpty:
        await message.reply_text('Some error occurred')
        await txt.delete()
