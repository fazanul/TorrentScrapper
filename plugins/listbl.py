import asyncio
from main import driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pyrogram import filters, Client


@Client.on_message(filters.command('listbl'))
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
