import os
import urllib
from .commands import encode_string
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import *

IS_BATCH_PROCESSING = False
BATCH = []

#################################### FOR PRIVATE ################################################
@Client.on_message((filters.document | filters.video | filters.audio | filters.photo) & filters.incoming & ~filters.channel)
async def storefile(c, m):
    global IS_BATCH_PROCESSING
    if IS_BATCH_PROCESSING:
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
