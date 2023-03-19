import os
import telebot
import ai
from dotenv import load_dotenv

load_dotenv()
TG_TOKEN = os.environ.get('TG_TOKEN')

bot = telebot.TeleBot(TG_TOKEN)

@bot.message_handler(commands=["gpt"])
def respond(message):
    response = ai.process(message.text[5:])
    bot.reply_to(message, response)

bot.infinity_polling()

