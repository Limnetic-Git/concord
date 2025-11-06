from dataclasses import dataclass

@dataclass
class Chat:
    id: str
    type: str
    name: str
    members: list #List[dict] 
    messages: list #List[dict]
    
class ChatsManager:
    def __init__(self):
        """Инициализация менеджера чатов"""
        self.chats = {}
        self.id = 0
    
    def create_chat(self, accounts_manager, chat_type: str, chat_name: str, members_logins: list):
        """Создаёт чат с указанными параметрами"""
        current_chat_id = f'{self.id:09d}'
        self.chats[current_chat_id] = Chat(current_chat_id, chat_type, chat_name, [], [])
        self.id += 1
        
        members = []
        for login in members_logins:
            account_id = accounts_manager.find_account_by_login(login)
            if account_id:
                members.append(accounts_manager.accounts[account_id])
                if self.add_member_to_chat(current_chat_id, members[-1]) == 2000:
                    return 2000, None # Аккаунт уже в чате
            else:
                return 2001, None # Аккаунт с таким логином не найден
        return 2100, self.chats[current_chat_id]  # Успех
        
    def add_member_to_chat(self, chat_id: str, member):
        """Добавляет клиента в указанный чат"""
        if not any(member_obj['id'] == member.id for member_obj in self.chats[chat_id].members):
            self.chats[chat_id].members.append({'id': member.id, 'login': member.login})
            
            member.chats_ids.append(chat_id)
            print(self.chats[chat_id])
            return 2100 # Успех
        
        else:
            return 2000 # Пользователь уже в чате
        
    def __get_chat_history(self, chat_id: str, number: int):
        answer = self.chats[chat_id].__dict__
        answer['messages'] = answer['messages'][:number]
        return answer
    
        
    def chats_history_for_account(self, accounts_manager, account_id: str):
        """Возвращает чаты (целиком) в которых есть указанный аккаунт"""
        chats_ids = accounts_manager.accounts[account_id].chats_ids
        chats_history = []
        for chat_id in chats_ids:
            chats_history.append(self.__get_chat_history(chat_id, 30))
        return chats_history
    
    

    def message_registation(self, accounts_manager, chat_id: str, message_text: str, author_login: str):
        """Добавляет сообщение в чат и рассылает конкретно это новое сообщение всем участникам чата в сети"""
        new_message = {
            "message_text": message_text,
            "author_login": author_login,
        }
        self.chats[chat_id].messages.append(new_message.copy())
        new_message['chat_id'] = chat_id
        new_message['type'] = "message"
        for account in self.chats[chat_id].members:
            account_id = account['id']
            accounts_manager.accounts[account_id].new.append(new_message)
        
    def new_chat_registration(self, accounts_manager, chat, account_id):
        new_chat = {
            "type": 'chat',
            "chat": chat.__dict__,
            }
        for account in chat.members:
            accounts_manager.accounts[account['id']].new.append(new_chat)

        


        
