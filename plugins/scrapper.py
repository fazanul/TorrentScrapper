import os
import aiohttp
import asyncio
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pyrogram import Client, filters
from plugins.messages import caption


options = webdriver.ChromeOptions()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-infobars")

driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
driver.maximize_window()
torrent = []


@Client.on_message(filters.regex("index\.php\?/forums/topic"))
async def link_regex(c,m):
    try:
        link = str(m.text)
        txt = await m.reply_text("Scrapping torrent link, Please Wait")
        driver.get(link)
        p = driver.find_element(By.CLASS_NAME, "ipsImage_thumbnailed").get_attribute("src")
        torrent_link = driver.find_elements(By.CLASS_NAME, "ipsAttachLink_block")
        try:
            title = driver.find_element(By.XPATH, '//h1').text
        except NoSuchElementException:
            title = ""
        heading = f"**{title}**\n\n"
        msg = ""
        for link in torrent_link:
            tor = link.get_attribute("href")
            text = link.text
            msg += f"**Name : {text}**\n**Link:** {tor}\n\n-\n\n"
        if msg == "":
            await m.send_message(-1001549256479, "No Torrents Found")
            await m.message.delete()
        elif msg != "":
            reply_text = f"{msg}"
            await c.send_photo(-1001549256479, p, caption=heading)
            await c.send_message(-1001549256479, reply_text)
            await txt.delete()

    except Exception as e:
        print(e)
        await c.send_message(-1001549256479, 'Some error occurred')
        await txt.delete()


@Client.on_message(filters.command('listmv'))
async def listmv(c, m):
    querys = ""
    texts = ""
    length = len(m.command)
    for queryss in m.command[1:length]:
        querys += f"{queryss} "
    if querys == "":
        await m.reply(f'`/listmv [query]`', quote=True)
    elif querys != "":
        link = f"https://www.1tamilmv.com/index.php?/search/&q={querys}&search_and_or=and&search_in=titles&sortby=relevancy"
        txt = await m.reply_text(f"Searching for: {querys} 🔍")
        driver.get(link)
        await asyncio.sleep(5)
        title = driver.title
        links = driver.find_elements(By.CLASS_NAME, "ipsStreamItem_title")
        msg = []
        count = 0

        for link in links:
            text = link.text
            url0 = link.find_element(By.CLASS_NAME, 'ipsType_break')
            url1 = url0.find_element(By.TAG_NAME, 'a').get_attribute("href")
            print(url1)
            count += 1
            msgs = f"{count}. <a href='{url1}'>{text}</a>\n\n"
            msg.append(msgs)

        for text in msg[0:20]:
            texts += text
        reply = f"<b>{title}</b>\n\n{texts}"
        await c.send_message(m.chat.id, reply, disable_web_page_preview=True, parse_mode="html")
        await txt.delete()


@Client.on_message(filters.command('listbl'))
async def lists(c, m):
    querys = ""
    texts = ""
    length = len(m.command)
    for queryss in m.command[1:length]:
        querys += f"{queryss} "
    if querys == "":
        await m.reply(f'`/listbl [query]`', quote=True)
    elif querys != "":
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


@Client.on_message(filters.command('latest'))
async def ss(bot, message):
    # Getting ss of tamilmv
    txt = await bot.send_message(message.chat.id, "Getting screenshot of latest movies of 1TamilMv.com")
    N = 7
    name = ''.join(random.choices(string.ascii_uppercase +
                                  string.digits, k=N))
    driver.get("https://www.1tamilmv.com/")
    photo = name + ".png"
    driver.save_screenshot(photo)

    # Getting ss of tamilblasters
    N = 7
    name = ''.join(random.choices(string.ascii_uppercase +
                                  string.digits, k=N))
    driver.get("https://www.tamilblasters.com/")
    await txt.edit(text="Got Screenshot of 1TamilMv.com. Now Getting screenshot of latest movies of TamilBlasters.com")
    photo1 = name + ".png"
    driver.save_screenshot(photo1)
    await txt.delete()

    # sending captured ss to user
    await message.reply_photo(photo, quote=True, caption="**Screenshot of latest movies of 1TamilMV.com**")
    await message.reply_photo(photo1, quote=True, caption="**Screenshot of latest movies of TamilBlasters.com**")

    # deleting captured from db
    os.remove(photo)
    os.remove(photo1)


# channel post
@Client.on_message(filters.command('post'))
async def post(bot, message):
    try:
        try:
            reply_messages = message.reply_to_message.text
            link = reply_messages
        except AttributeError:
            pass
        try:
            link = str(message.command[1])
        except IndexError:
            await message.reply(f'`/post [movie_url]`', quote=True)
        txt = await message.reply_text("Loading 🔄", quote=True)
        driver.get(link)
        photo = driver.find_element(By.CLASS_NAME, "ipsImage_thumbnailed").get_attribute("src")

        try:
            title = driver.find_element(By.XPATH, '//h1').text
        except NoSuchElementException:
            title = ""
        heading = f"**{title}**\n"
        await message.reply_photo(photo, caption=heading + caption, quote=True)
        await txt.delete()

    except Exception as e:
        await txt.edit_text("Some Error Occurred, Try Again")
