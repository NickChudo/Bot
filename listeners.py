#Class where you can put commands and message respondings
class listener:
    doListen = False
    messagelist = {"/start" : "Starting listener...", "/help" : "Just throw here voice message"}

    def toggle_listener(self):
        self.doListen = not(self.doListen)
        return f"Changed state, now it's {self.doListen}"

    cmdlist = {"/start" : toggle_listener}    

    #Приводит поступающие команды в соответствие с ответом
    def get_response_for_text_message(self, message):
        if(message in self.cmdlist.keys()):
            return self.cmdlist[message](self)
        if(message in self.messagelist.keys() and self.doListen):
            return self.messagelist[message]
        return "Неверная команда. Вероятно, стоит сначала сделать /start или обратиться за справкой в /help"
            
