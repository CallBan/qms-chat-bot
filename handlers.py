from telegram import Update
from retriever import Retriever
from gpt_client import ask_gigachat

retriever = Retriever()

async def start(update: Update, _):
    await update.message.reply_text(
        "Привет! Я бот-консультант по СМК.\nЗадайте вопрос."
    )

async def answer(update: Update, _):
    q = update.message.text
    chunks = [txt for txt, _ in retriever.search(q, top_k=5)]
    reply = ask_gigachat(q, chunks)
    await update.message.reply_text(reply)