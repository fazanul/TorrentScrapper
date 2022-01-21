# (c) @ask_admin001

from pyrogram import Client

bot = Client(
    "Web Scrapping Bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
)        
        
print("Bot running...")
bot.run()
