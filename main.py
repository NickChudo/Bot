import telebot
import soundfile as sf
import listeners
from modelinit import ModelInit

keyfile = open('key.txt', 'r')
key = keyfile.readline()
keyfile.close()

bot = telebot.TeleBot(key)
samplerate = 16000 

model = ModelInit(path='model.pth', device_type='cpu')
listener = listeners.listener()

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, listener.get_response_for_text_message(message.text))

@bot.message_handler(content_types=['voice'])
def solve_voice_message(message):
    if(listener.doListen == False):
        bot.send_message(message.from_user.id, "Activate me with /start first!")
        return
    bot.send_message(message.from_user.id, "Recieved voice message, processing...")
    try:
        file_metadata = bot.get_file(message.voice.file_id)
        file = bot.download_file(file_metadata.file_path)
        with open('buffer.ogg', 'wb') as new_file:
            new_file.write(file)
        data, samplerate = sf.read('buffer.ogg')
        sf.write('buffer.wav',data, samplerate)
        returnal = model.predict('buffer.wav')
        if(len(returnal) == 0):
            bot.send_message(message.from_user.id, "Network has created empty response.")
            return
        bot.send_message(message.from_user.id, returnal)
    except:
        bot.send_message(message.from_user.id, "Error has occurred. Please contact us at https://github.com/NickChudo/Bot/issues")

@bot.message_handler(content_types=['document'])
def solve_audio_message(message):
    if(listener.doListen == False):
        bot.send_message(message.from_user.id, "Activate me with /start first!")
        return
    bot.send_message(message.from_user.id, "Recieved document message, processing...")
    try:
        file_metadata = bot.get_file(message.document.file_id)
        file = bot.download_file(file_metadata.file_path)
        with open('1.wav', 'wb') as new_file:
            new_file.write(file)
        data, samplerate = sf.read('1.wav')
        sf.write('buffer.wav',data, samplerate)
        returnal = model.predict('buffer.wav')
        if(len(returnal) == 0):
            bot.send_message(message.from_user.id, "Network has created empty response.")
            return
        bot.send_message(message.from_user.id, returnal)
    except:
        bot.send_message(message.from_user.id, "Error has occurred. Please contact us at https://github.com/NickChudo/Bot/issues")


bot.infinity_polling(timeout=5, long_polling_timeout = 2)