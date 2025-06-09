from telegram import Update
from retriever import Retriever
from gpt_client import ask_gigachat
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown

retriever = Retriever()

async def start(update: Update, _):
    await update.message.reply_text(
        "Привет! Я бот-консультант по СМК.\nЗадайте вопрос."
    )

async def answer(update: Update, _):
    q = update.message.text
    chunks = [txt for txt, _ in retriever.search(q)]
    reply = ask_gigachat(q, chunks)

    safe_reply = escape_markdown(reply, version=2)

    await update.message.reply_text(safe_reply, parse_mode=ParseMode.MARKDOWN_V2)