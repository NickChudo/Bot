import telebot
import soundfile as sf
import listeners
from modelinit import ModelInit

keyfile = open('key.txt', 'r')
key = keyfile.readline()
keyfile.close()

bot = telebot.TeleBot(key)
samplerate = 16000 #set this constant to that number which is compatible with network, yep.

messagelist = {"/start" : "Starting listener...", "/help" : "Just throw here voice message"}

is_started = False
model = ModelInit(path='model.pth', device_type='cuda')
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
    returnal = model.predict('example.wav')
    bot.send_message(message.from_user.id, returnal)

@bot.message_handler(content_types=['document'])
def solve_audio_message(message):
    bot.send_message(message.from_user.id, "Recieved audio message. Nice.")
    file_metadata = bot.get_file(message.document.file_id)
    file = bot.download_file(file_metadata.file_path)
    #TODO: find a better way to convert ogg's to wav's
    with open('1.wav', 'wb') as new_file:
        new_file.write(file)
    #TODO: unhardcode this
    # And also for some reason WAV's are heavier than oggs. Oof    
    data, samplerate = sf.read('1.wav')
    sf.write('example.wav',data, samplerate)
    returnal = model.predict('example.wav')
    bot.send_message(message.from_user.id, returnal)

@bot.message_handler(content_types=['video'])
def solve_audio_message(message):
    bot.send_message(message.from_user.id, "Recieved video message. Nice.")
    file_metadata = bot.get_file(message.video.file_id)
    file = bot.download_file(file_metadata.file_path)
    #TODO: find a better way to convert ogg's to wav's
    with open('1.wav', 'wb') as new_file:
        new_file.write(file)
    #TODO: unhardcode this
    # And also for some reason WAV's are heavier than oggs. Oof    
    data, samplerate = sf.read('1.wav')
    sf.write('example.wav',data, samplerate)
    returnal = model.predict('example.wav')
    bot.send_message(message.from_user.id, returnal)

bot.polling(none_stop=True, interval=0)