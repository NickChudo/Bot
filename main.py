import telebot

bot = telebot.TeleBot('6213357069:AAFrHUa2DaU0XdiMOAvibA_Tb3iBuwQin2Y')

@bot.message_handler(content_types=['text'])

def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "Привет, ага":
        bot.send_message(message.from_user.id, "Ахахахахахахахахахахахаха!")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет!")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

@bot.message_handler(content_types=['voice'])
def solve_voice_message(message):
    bot.send_message(message.from_user.id, "Recieved voice message. Nice.")
    
bot.polling(none_stop=True, interval=0)