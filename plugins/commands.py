import os
import asyncio
import time
import logging
import logging.config
from datetime import datetime

# Get logging configurations
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

import base64
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from database.database import *
from config import *
from bot import main


@Client.on_message(filters.command('start') & filters.incoming & filters.private)
async def start(c, m, cb=False):
    id = m.from_user.id
    try:
        await get_data(id)
    except:
        pass
    if not cb:
        send_msg = await m.reply_text("**Processing...**", quote=True)

    owner = await c.get_users(int(OWNER_ID))
    owner_username = owner.username if owner.username else 'Ns_bot_updates'

    # start text
    text = f"""Hey! {m.from_user.mention(style='md')}

💡 ** I am Telegram File Store Bot**

`You can store your Telegram Media for permanent Link!`


**👲 Maintained By:** {owner.mention(style='md')}
"""

    # Buttons
    buttons = [
        [
            InlineKeyboardButton('My Father 👨‍✈️', url=f"https://t.me/{owner_username}"),
            InlineKeyboardButton('Help 💡', callback_data="help")
        ],
        [
            InlineKeyboardButton('About 📕', callback_data="about")
        ]
    ]

    # when button home is pressed
    if cb:
        return await m.message.edit(
                   text=text,
                   reply_markup=InlineKeyboardMarkup(buttons)
               )

    if len(m.command) > 1: # sending the stored file
        try:
            m.command[1] = await decode(m.command[1])
        except:
            pass

        if 'batch_' in m.command[1]:
            await send_msg.delete()
            cmd, chat_id, message = m.command[1].split('_')
            string = await c.get_messages(int(chat_id), int(message)) if not DB_CHANNEL_ID else await c.get_messages(int(DB_CHANNEL_ID), int(message))

            if string.empty:
                owner = await c.get_users(int(OWNER_ID))
                return await m.reply_text(f"🥴 Sorry bro your file was deleted by file owner or bot owner\n\nFor more help contact my owner 👉 {owner.mention(style='md')}")
            message_ids = (await decode(string.text)).split('-')
            for msg_id in message_ids:
                msg = await c.get_messages(int(chat_id), int(msg_id)) if not DB_CHANNEL_ID else await c.get_messages(int(DB_CHANNEL_ID), int(msg_id))

                if msg.empty:
                    owner = await c.get_users(int(OWNER_ID))
                    return await m.reply_text(f"🥴 Sorry bro your file was deleted by file owner or bot owner\n\nFor more help contact my owner 👉 {owner.mention(style='md')}")
                try:
                    await msg.copy(m.from_user.id, protect_content=PROTECT_CONTENT or cmd == "protectedbatch")
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(m.from_user.id, protect_content=PROTECT_CONTENT or cmd == "protectedbatch")
                except:
                    pass
            return

        *_, chat_id, msg_id = m.command[1].split('_')
        msg = await c.get_messages(int(chat_id), int(msg_id)) if not DB_CHANNEL_ID else await c.get_messages(int(DB_CHANNEL_ID), int(msg_id))

        if msg.empty:
            return await send_msg.edit(f"🥴 Sorry bro your file was deleted by file owner or bot owner\n\nFor more help contact my owner 👉 {owner.mention(style='md')}")
        
        caption = f"{msg.caption.markdown}\n\n\n" if msg.caption else ""
        as_uploadername = (await get_data(str(chat_id))).up_name
        
        if as_uploadername:
            if chat_id.startswith('-100'):
                channel = await c.get_chat(int(chat_id))
                caption += "**--Uploader Details:--**\n" 
                caption += f"**📢 Channel Name:** `{channel.title}`\n" 
                caption += f"**🗣 User Name:** @{channel.username}\n" if channel.username else ""
            else:
                user = await c.get_users(int(chat_id)) 
                caption += "**--Uploader Details:--**\n"
                caption += f"**👁 User Name:** @{user.username}\n" if user.username else "" 
                caption += f"**👤 User Id:** `{user.id}`\n"


        await send_msg.delete()
        await msg.copy(m.from_user.id, caption=caption, protect_content=PROTECT_CONTENT or _)


    else: # sending start message
        await send_msg.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )


@Client.on_message(filters.command('me') & filters.incoming & filters.private)
async def me(c, m):
    """ This will be sent when /me command was used"""

    me = await c.get_users(m.from_user.id)
    text = "--**YOUR DETAILS:**--\n"
    text += f"**🦚 First Name:** `{me.first_name}`\n"
    text += f"**🐧 Last Name:** `{me.last_name}`\n" if me.last_name else ""
    text += f"**👁 User Name:** @{me.username}\n" if me.username else ""
    text += f"**👤 User Id:** `{me.id}`\n"
    text += f"**💬 DC ID:** {me.dc_id}\n" if me.dc_id else ""
    text += f"**✔ Is Verified By TELEGRAM:__ `{me.is_verified}`\n\n" if me.is_verified else ""
    text += f"**👺 Is Fake:** {me.is_fake}\n" if me.is_fake else ""
    text += f"**💨 Is Scam:** {me.is_scam}\n" if me.is_scam else ""
    text += f"**📃 Language Code:** {me.language_code}" if me.language_code else ""

    await m.reply_text(text, quote=True)

@Client.on_message(filters.command('mode') & filters.incoming & filters.private)
async def set_mode(c,m):
    if IS_PRIVATE:
        if m.from_user.id not in AUTH_USERS:
            return
    usr = m.from_user.id
    if len(m.command) > 1:
        usr = m.command[1]
    caption_mode = (await get_data(usr)).up_name
    if caption_mode:
       await update_as_name(str(usr), False)
       text = "Uploader Details in Caption: **Disabled ❌**"
    else:
       await update_as_name(str(usr), True)
       text = "Uploader Details in Caption: **Enabled ✔️**"
    await m.reply_text(text, quote=True)

async def decode(base64_string):
    base64_bytes = base64_string.encode("ascii")
    string_bytes = base64.b64decode(base64_bytes) 
    string = string_bytes.decode("ascii")
    return string

async def encode_string(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

@Client.on_message(filters.private & filters.command('broadcast') & filters.user(OWNER_ID))
async def send_text(client: Client, message: Message):
    if message.reply_to_message:
        query = await query_msg()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for row in query:
            chat_id = int(row[0])
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                blocked += 1
            except InputUserDeactivated:
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply("""<code>Use this command as a replay to any telegram message with out any spaces.</code>""")
        await asyncio.sleep(8)
        await msg.delete()

@Client.on_message(filters.command('users') & filters.private & filters.user(OWNER_ID))
async def get_users(client: Client, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=""""<b>Processing ...</b>""")
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time

@Client.on_message(filters.command('uptime') & filters.private & filters.user(OWNER_ID))
async def uptime(c, app, message: Message):
    UPTIME_TEXT = "<b>BOT UPTIME</b>\n\n{uptime}"
    now = datetime.now()
    delta = now - app.uptime
    time = get_readable_time(delta.seconds)
    await message.reply(UPTIME_TEXT.format(uptime=time))
