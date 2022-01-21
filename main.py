# (c) @ask_admin001

from pyrogram import Client
from config import API_HASH, BOT_TOKEN, API_ID

bot = Client(
    "Web Scrapping Bot",
    plugins = dict(root="plugins"),
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
)        
        
print("Bot running...")
bot.run()
