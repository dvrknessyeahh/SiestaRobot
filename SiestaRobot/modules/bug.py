import re
import html

from typing import Optional
from html import escape
from datetime import datetime

from telegram.utils.helpers import mention_html
from telegram.error import BadRequest
from telegram import Message
from telegram.ext import (
    CommandHandler,
    Filters,
)

from SiestaRobot import (
    dispatcher,
    telethn as Client,
    JOIN_LOGGER as log,
)


@Client.on_message()
async def bug (cln:Client, msg:Message):
    if len(msg.text.split()) > 1:
        try:
            datetime_fmt = "%H:%M - %d-%m-%Y"
            bug_report = (
                "<b>#BUG</b>\n"
                f"User: {msg.from_user.mention}\n"
                f"ID: <code>{msg.from_user.id}</code>\n\n"
                "The content of the report:\n"
                f"<code>{html.escape(msg.text.split(None, 1)[1])}</code>\n"
                f"<b>Event Stamp</b>: <code>{datetime.utcnow().strftime(datetime_fmt)}</code>"
            )
            await cln.send_message(
                chat_id=log,
                text=bug_report,
                disable_web_page_preview=True,
            )
            await msg.reply_text(f"The bug was successfully reported to the support group")
        except BadRequest:
            await msg.reply_text(f"The bug was failed reported to the support group")
    else:
        await msg.reply(f"No bug to report")

__mod_name__ = "Bug"

BUG_HANDLER = CommandHandler(["bug"], bug, Filters.command, run_async=True)

dispatcher.add_handler(BUG_HANDLER)