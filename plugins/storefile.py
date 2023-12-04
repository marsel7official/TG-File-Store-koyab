import os
import urllib
import base64
from .commands import encode_string
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import *

BATCH=[]

@Client.on_message(filters.command('batch') & filters.private & filters.incoming)
async def batch(c, m):
    global IS_BATCH_PROCESSING
    """ This is for batch command"""
    if IS_PRIVATE:
        if m.from_user.id not in AUTH_USERS:
            return
    IS_BATCH_PROCESSING = True
    BATCH.append(m.from_user.id)
    files = []
    i = 1

    while m.from_user.id in BATCH:
        if i == 1:
            media = await c.ask(chat_id=m.from_user.id, text='Send me some files or videos or photos or text or audio, if possible send 1 by 1. If you want to cancel the process send /cancel')
            if media.text == "/cancel":
                IS_BATCH_PROCESSING = False
                return await m.reply_text('Cancelled Successfully ✌')
            files.append(media)
        else:
            try:
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Done ✅', callback_data='done')]])
                media = await c.ask(chat_id=m.from_user.id, text='Ok 😉. Now send me some more files Or press done to get shareable link. If you want to cancel the process send /cancel', reply_markup=reply_markup)
                if media.text == "/cancel":
                    IS_BATCH_PROCESSING = False
                    return await m.reply_text('Cancelled Successfully ✌')
                files.append(media)
            except Exception as e:
                print(e)
        i += 1
        
    message = await m.reply_text("Generating shareable link 🔗")
    string = ""
    for file in files:
        if DB_CHANNEL_ID:
            copy_message = await file.copy(int(DB_CHANNEL_ID))
        else:
            copy_message = await file.copy(m.from_user.id)
        string += f"{copy_message.id}-"
        await asyncio.sleep(1)

    string_base64 = await encode_string(string[:-1])
    send = await c.send_message(m.from_user.id, string_base64) if not DB_CHANNEL_ID else await c.send_message(int(DB_CHANNEL_ID), string_base64)
    base64_string1 = await encode_string(f"batch_{m.chat.id}_{send.id}")
    base64_string2 = await encode_string(f"protectedbatch_{m.chat.id}_{send.id}")
    bot = await c.get_me()
    url1 = f"https://t.me/{bot.username}?start={base64_string1}"
    url2 = f"https://t.me/{bot.username}?start={base64_string2}"

    await message.edit(text=f"🔗 Normal Url: {url1}\n🛡️ Protected Url: {url2}")
    IS_BATCH_PROCESSING = False
    

#################################### FOR PRIVATE ################################################
@Client.on_message((filters.document | filters.video | filters.audio | filters.photo) & filters.incoming & ~filters.channel)
async def storefile(c, m):
    if BATCH:
        return
    if IS_PRIVATE:
        if m.from_user.id not in AUTH_USERS:
            return
    send_message = await m.reply_text("**Processing...**", quote=True)
    media = m.document or m.video or m.audio or m.photo
    # text
    text = ""
    if not m.photo:
        text = "--**🗃️ File Details:**--\n"
        text += f"📂 **File Name:** `{media.file_name}`\n" if media.file_name else ""
        text += f"📊 **File Size:** `{humanbytes(media.file_size)}`\n" if media.file_size else ""
        if not m.document:
            text += f"🎞 **Duration:** `{TimeFormatter(media.duration * 1000)}`\n" if media.duration else ""
            if m.audio:
                text += f"🎵 **Title:** `{media.title}`\n" if media.title else ""
                text += f"🎙 **Performer:** `{media.performer}`\n" if media.performer else ""
    text += "**--Uploader Details:--**\n\n"
    text += f"**🦚 First Name:** `{m.from_user.first_name}`\n"
    text += f"**👤 User Id:** `{m.from_user.id}`\n"

    # if databacase channel exist forwarding message to channel
    if DB_CHANNEL_ID:
        msg = await m.copy(int(DB_CHANNEL_ID))
        await msg.reply(text)

    # creating urls
    bot = await c.get_me()
    base64_string1 = await encode_string(f"{m.chat.id}_{msg.id}")
    base64_string2 = await encode_string(f"protect_{m.chat.id}_{msg.id}")
    url1 = f"https://t.me/{bot.username}?start={base64_string1}"
    url2 = f"https://t.me/{bot.username}?start={base64_string2}"
    txt = urllib.parse.quote(text.replace('--', ''))
    share_url = f"tg://share?url={txt}File%20Link%20👉%20{url1}"

    # making buttons
    buttons = [[
        InlineKeyboardButton(text="Open Url 🔗", url=url1),
        InlineKeyboardButton(text="Share Link 👤", url=share_url)
        ],
        [
        InlineKeyboardButton("Protected Url 🛡️", url=url2),
        ],
        [
        InlineKeyboardButton(text="Delete 🗑", callback_data=f"delete+{msg.id}")
    ]]

    # sending message
    await send_message.edit(
        text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

#################################### FOR CHANNEL################################################

@Client.on_message((filters.document|filters.video|filters.audio|filters.photo) & filters.incoming & filters.channel & ~filters.forwarded)
async def storefile_channel(c, m):
    global IS_BATCH_PROCESSING
    if IS_BATCH_PROCESSING:
        return
    if IS_PRIVATE:
        if m.chat.id not in AUTH_USERS:
            return
    media = m.document or m.video or m.audio or m.photo

    # text
    text = ""
    if not m.photo:
        text = "--**🗃️ File Details:**--\n\n\n"
        text += f"📂 **File Name:** `{media.file_name}`\n" if media.file_name else ""
        text += f"📊 **File Size:** `{humanbytes(media.file_size)}`\n" if media.file_size else ""
        if not m.document:
            text += f"🎞 **Duration:** `{TimeFormatter(media.duration * 1000)}`\n" if media.duration else ""
            if m.audio:
                text += f"🎵 **Title:** `{media.title}`\n" if media.title else ""
                text += f"🎙 **Performer:** `{media.performer}`\n" if media.performer else ""
    text += f"**✏ Caption:** `{m.caption}`\n" if m.caption else ""
    text += "**Uploader Details:**\n\n"
    text += f"**📢 Channel Name:** `{m.chat.title}`\n"
    text += f"**🗣 User Name:** @{m.chat.username}\n" if m.chat.username else ""

    # if databacase channel exist forwarding message to channel
    if DB_CHANNEL_ID:
        msg = await m.copy(int(DB_CHANNEL_ID))
        await msg.reply(text)

    # creating urls
    bot = await c.get_me()
    base64_string1 = await encode_string(f"{m.chat.id}_{msg.id}")
    base64_string2 = await encode_string(f"protect_{m.chat.id}_{msg.id}")
    url1 = f"https://t.me/{bot.username}?start={base64_string1}"
    url2 = f"https://t.me/{bot.username}?start={base64_string2}"
    txt = urllib.parse.quote(text.replace('--', ''))
    share_url = f"tg://share?url={txt}File%20Link%20👉%20{url1}"

    # making buttons
    buttons = [[
        InlineKeyboardButton(text="Open Url 🔗", url=url1),
        InlineKeyboardButton(text="Share Link 👤", url=share_url)
    ],
       [InlineKeyboardButton("Protected Url 🛡️", url=url2)]
    ]

    # Editing and adding the buttons
    await m.edit_reply_markup(InlineKeyboardMarkup(buttons))


def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " days, ") if days else "") + \
        ((str(hours) + " hrs, ") if hours else "") + \
        ((str(minutes) + " min, ") if minutes else "") + \
        ((str(seconds) + " sec, ") if seconds else "") + \
        ((str(milliseconds) + " millisec, ") if milliseconds else "")
    return tmp[:-2]
