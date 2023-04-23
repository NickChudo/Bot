import telebot
import soundfile as sf
import listeners

bot = telebot.TeleBot('6213357069:AAFrHUa2DaU0XdiMOAvibA_Tb3iBuwQin2Y')

samplerate = 16000 #set this constant to that number which is compatible with network, yep.

messagelist = {"/start" : "Starting listener...", "/help" : "Just throw here voice message"}

is_started = False

listener = listeners.listener()

@bot.message_handler(content_types=['text'])

def get_text_messages(message):
    bot.send_message(message.from_user.id, listener.get_response_for_text_message(message.text))

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