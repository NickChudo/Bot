#Class where you can put commands and message respondings
class listener:
    doListen = False
    doRecord = False
    messagelist = {}
    cmd_descriptions = {"Send me voice message" : "Recieve decrypted text message", "/start" : "Starts listener.", "/stop" : "Stops listener.", "/help" : "Get all commands."}

    def disable_listener(self):
        self.doListen = False
        return f"Listener has been disabled, no voice messages will get their response"
    
    def enable_listener(self):
        self.doListen = True
        return f"Listener has been enabled, you can send voice messages now."

    def get_current_commands(self):
        response = ""
        for i in self.cmd_descriptions.keys():
            response += f"{i} : {self.cmd_descriptions[i]} \n"
        return response

    def enable_recorder(self):
        self.doListen = True
        self.doRecord = True
        return f"Recorder has been enabled, voice messages will be sent to disk into training dataset."


    cmdlist = {"/start" : enable_listener, "/stop" : disable_listener, "/help" : get_current_commands, "/record" : enable_recorder}    

    #Приводит поступающие команды в соответствие с ответом
    def get_response_for_text_message(self, message):
        if(message in self.cmdlist.keys()):
            return self.cmdlist[message](self)
        if(message in self.messagelist.keys() and self.doListen):
            return self.messagelist[message]
        return "Неверная команда. Вероятно, стоит сначала сделать /start или обратиться за справкой в /help"
            
