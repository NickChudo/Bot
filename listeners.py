import userinfo


#Class where you can put commands and message respondings
class listener:
    doListen = False
    messagelist = {}
    #current_users: structure is (id : user)
    current_users = {}
    cmd_descriptions = {"Send me voice message" : "Recieve decrypted text message", "/start" : "Starts listener.", "/stop" : "Stops listener.", "/help" : "Get all commands."}

    def disable_listener(self, user):
        user.doListen = False
        return f"Listener has been disabled, no voice messages will get their response"
    
    def enable_listener(self, user):
        user.doListen = True
        return f"Listener has been enabled, you can send voice messages now."

    def get_current_commands(self, user):
        response = ""
        for i in self.cmd_descriptions.keys():
            response += f"{i} : {self.cmd_descriptions[i]} \n"
        return response


    cmdlist = {"/start" : enable_listener, "/stop" : disable_listener, "/help" : get_current_commands}    

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
            
