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
        self.chats = {}
        self.id = 0
    
    def create_chat(self, accounts_manager, chat_type: str, chat_name: str, members_logins: list):
        """Создаёт чат с указанными параметрами"""
        current_chat_id = f'{self.id:09d}'
        self.chats[current_chat_id] = Chats(current_chat_id, chat_type, chat_name, [], [])
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
        if not member.id in self.chats[chat_id].members_ids:
            self.chats[chat_id].members_ids.append(member.id)
            self.chats[chat_id].members_logins.append(member.login)
            member.chats_ids.append(chat_id)
            return 2100 # Успех
        else:
            return 2000 # Пользователь уже в чате
    

        


        