from lib import *


TOKEN = "7150156832:AAGV2P4_ZFB4HSfucnyvTzKNfxeg6_Y89J8"
bot = telebot.TeleBot(TOKEN)


def send_message_to_chat(chat_id, message):
    bot.send_message(chat_id, message)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я ваш бот, я могу подсказать пассажиропоток в метро за какое-то время.')


@bot.message_handler(func=lambda message: True)
def echo(message):
    s = str(message.text)
    chat_id = message.chat.id
    query(s, chat_id)


bot.polling()
