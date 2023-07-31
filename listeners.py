import userinfo
import json

#Class where you can put commands and message respondings
class listener:
    doListen = False
    messagelist = {}
    #current_users: structure is (id : user)
    current_users = {}
    cmd_descriptions = {"Send me voice message" : "Recieve decrypted text message",
                         "/start" : "Starts listener.",
                           "/stop" : "Stops listener.",
                             "/help" : "Get all commands.",
                             "/ru" : "Переключить бота на Русский язык",
                             "/en" : "Toggle Bot to English language"}
    responses = {"listener_disabled" : "Listener has been disabled, no voice messages will get their response",
                 "listener_enabled" : "Listener has been enabled, you can send voice messages now"}
    ru_locale = {}
    en_locale = {"help" : cmd_descriptions, "responses" : responses}
    locales_storage = {}

    def disable_listener(self, user):
        user.doListen = False
        return self.locale_request_wrapper(user.locale, 'responses', 'listener_disabled')
    
    def enable_listener(self, user):
        user.doListen = True
        return self.locale_request_wrapper(user.locale, 'responses', 'listener_enabled')

    def get_current_commands(self, user):
        return self.print_dict(self.locale_category_wrapper(user.locale, 'help'))
    
    def print_dict(self, dictionary):
        result = ""
        for i in dictionary.keys():
            result += f"{i} : {dictionary[i]} \n"
        return result

    def locale_request_wrapper(self, locale, category, request):
        return self.locales_storage[locale][category][request]

    def locale_category_wrapper(self, locale, category):
        return self.locales_storage[locale][category]

    def set_ru(self, user):
        user.locale = "ru"
        return f"Бот переключён на русский язык"

    def set_en(self, user):
        user.locale = "en"
        return f"Switched Bot's localization to English."

    def listener(self):
        with open('locale_ru.json', 'r', encoding='utf-8') as f:
            self.ru_locale = json.load(f)
        with open('locale_en.json', 'r', encoding='utf-8') as f:
            self.en_locale = json.load(f)
        
        self.locales_storage["en"] = self.en_locale
        self.locales_storage["ru"] = self.ru_locale

        return self

    cmdlist = {"/start" : enable_listener, "/stop" : disable_listener, "/help" : get_current_commands, "/ru" : set_ru, "/en" : set_en}    

    def handle_user_input(self, message, id): 
        if(not (id in self.current_users.keys())):
            self.current_users[id] = userinfo.user()

    #Приводит поступающие команды в соответствие с ответом
    def get_response_for_text_message(self, message, id):
        user = self.current_users[id]
        if(message in self.cmdlist.keys()):
            return self.cmdlist[message](self, user)
        if(message in self.messagelist.keys() and user.doListen):
            return self.messagelist[message]
        return "Неверная команда. Вероятно, стоит сначала сделать /start или обратиться за справкой в /help"

#cmd_descriptions = {"Send me voice message" : "Recieve decrypted text message", "/start" : "Starts listener.", "/stop" : "Stops listener.", "/help" : "Get all commands."}

#ech = {}
#with open('locale_ru.json', 'r', encoding='utf-8') as f:
#    ech = json.load(f)
#print(ech)

#ech = listener().listener()
#print(ech.locales_storage)
