#Class where you can put commands and message respondings
class listener:
    doListen = False
    messagelist = {"/start" : "Starting listener...", "/help" : "Just throw here voice message"}

    def disable_listener(self):
        self.doListen = False
        return f"Listener disabled, no voice messages will get their response"
    
    def enable_listener(self):
        self.doListen = True
        return f"Listener enabled, you can send voice messages now."

    def get_current_commands(self):
        response = ""


    cmdlist = {"/start" : enable_listener, "/stop" : disable_listener}    

    #Приводит поступающие команды в соответствие с ответом
    def get_response_for_text_message(self, message):
        if(message in self.cmdlist.keys()):
            return self.cmdlist[message](self)
        if(message in self.messagelist.keys() and self.doListen):
            return self.messagelist[message]
        return "Неверная команда. Вероятно, стоит сначала сделать /start или обратиться за справкой в /help"
            
