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
                    return 2000 # Аккаунт уже в чате
            else:
                return 2001 # Аккаунт с таким логином не найден
        return 2100 # Успех
        
    def add_member_to_chat(self, chat_id: str, member):
        """Добавляет клиента в указанный чат"""
        if not any(member_obj['id'] == member.id for member_obj in self.chats[chat_id].members):
            self.chats[chat_id].members.append({'id': member.id, 'login': member.login})
            
            member.chats_ids.append(chat_id)
            print(self.chats[chat_id])
            return 2100 # Успех
        
        else:
            return 2000 # Пользователь уже в чате
    
    def chats_history_for_account(self, accounts_manager, account_id: str):
        """Возвращает чаты (целиком) в которых есть указанный аккаунт"""
        chats_ids = accounts_manager.accounts[account_id].chats_ids
        chats_history = []
        for chat_id in chats_ids:
            chats_history.append(self.chats[chat_id].__dict__)
        return chats_history

    def add_message_to_chat(self, chat_id: str, message_text: str, author_login: str):
        self.chats[chat_id].messages.append({
            "message_text": message_text,
            "author_login": author_login,
        })

        


        
