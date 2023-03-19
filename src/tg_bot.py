import os
import telebot
from dotenv import load_dotenv

load_dotenv()
TG_TOKEN = os.environ.get('TG_TOKEN')

bot = telebot.TeleBot(TG_TOKEN)

@bot.message_handler(commands=["gpt"])
def respond(message):
    bot.reply_to(message, "hello!")