import telebot
import soundfile as sf

bot = telebot.TeleBot('6213357069:AAFrHUa2DaU0XdiMOAvibA_Tb3iBuwQin2Y')

samplerate = 16000 #set this constant to that number which is compatible with network, yep.

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
    file_metadata = bot.get_file(message.voice.file_id)
    file = bot.download_file(file_metadata.file_path)
    #TODO: find a better way to convert ogg's to wav's
    with open('example.ogg', 'wb') as new_file:
        new_file.write(file)
    #TODO: unhardcode this
    # And also for some reason WAV's are heavier than oggs. Oof    
    data, samplerate = sf.read('example.ogg')
    sf.write('example.wav',data, samplerate)

    
bot.polling(none_stop=True, interval=0)