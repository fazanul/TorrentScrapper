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
    plugins = dict(root="plugins"),
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
)

print("Bot running...")
await bot.run()
