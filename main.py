import telebot
import soundfile as sf
import listeners
from modelinit import ModelInit
import yadisk

tg_keyfile = open('key.txt', 'r')
key = tg_keyfile.readline()
tg_keyfile.close()

yadisk_keyfile = open('yakey.txt', 'r')
yadisk_key = yadisk_keyfile.readline()
yadisk_keyfile.close()

#disk = yadisk.YaDisk(yadisk_key)
disk = yadisk.YaDisk(id="id", secret="secret",token="token")
#alright, set metadata aquiring into txt file so no one peeks this.
print(disk.get_disk_info())
if not disk.exists("Приложения/voice-db/test"):
    disk.mkdir("Приложения/voice-db/test")
#set this up to use custom application name and test subject
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
        if(listener.doRecord):
            if not disk.exists(f"Приложения/voice-db/dataset/{message.from_user.id}"):
                disk.mkdir(f"Приложения/voice-db/dataset/{message.from_user.id}")
            sendfile('buffer.wav', f'Приложения/voice-db/dataset/{message.from_user.id}/buffer1.wav')
            bot.send_message(message.from_user.id, "File has been successfully sent.")
            return
        returnal = model.predict('buffer.wav')
        if(len(returnal) == 0):
            bot.send_message(message.from_user.id, "Network has created empty response.")
            return
        bot.send_message(message.from_user.id, returnal)
    except:
        bot.send_message(message.from_user.id, "Error has occurred. Please contact us at https://github.com/NickChudo/Bot/issues")

def sendfile(path, path_dir):
    disk.upload(path, path_dir)

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