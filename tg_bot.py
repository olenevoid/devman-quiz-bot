import os
import random

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import BOT_PROXY, BOT_TOKEN, QUIZ_DIR, USE_PROXY
from parse_quiz import parse_quiz_file

NEW_QUESTION = "Новый вопрос"
GIVE_UP = "Сдаться"
SCORE = "Мой счет"

KEYBOARD = ReplyKeyboardMarkup(
    [[NEW_QUESTION, GIVE_UP], [SCORE]],
    resize_keyboard=True,
)


async def start(update: Update, context):
    await update.message.reply_text(
        "Привет! Я бот для викторин.",
        reply_markup=KEYBOARD,
    )


async def handle_button(update: Update, context):
    text = update.message.text

    if text == NEW_QUESTION:
        question = get_random_question()
        if question:
            await update.message.reply_text(question["question"])
        else:
            await update.message.reply_text("Не удалось загрузить вопрос.")
    elif text == GIVE_UP:
        await update.message.reply_text("Сдаёшься? Нажми 'Новый вопрос'.")
    elif text == SCORE:
        await update.message.reply_text("Пока 0 очков.")


def get_random_question():
    files = [
        os.path.join(QUIZ_DIR, f)
        for f in os.listdir(QUIZ_DIR)
        if f.endswith(".txt")
    ]
    if not files:
        return None
    filename = random.choice(files)
    questions = parse_quiz_file(filename)
    if not questions:
        return None
    return random.choice(questions)


def main():
    builder = Application.builder().token(BOT_TOKEN)
    if USE_PROXY:
        builder = builder.proxy(BOT_PROXY).get_updates_proxy(BOT_PROXY)
    app = builder.build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button)
    )
    app.run_polling()


if __name__ == "__main__":
    main()
