from pyrogram import Client, filters

txt = '''
Commands:

/listmv [query] - to search movies in TamilMV

/listbl [query] - to search movies in Tamilblasters

/post [tamilmv link] - makes a post of a given link

/latest - to get screenshot of latest movies in TamilMV and Tamilblasters

Bot Usage:

Send any 1tamilmv.com or tamilblasters.com link to scrap torrents
'''

@Client.on_message(filters.command('start'))
async def start(bot, message):
    await message.reply_text(txt)
