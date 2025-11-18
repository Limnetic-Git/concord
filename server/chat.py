from dataclasses import dataclass
import random

@dataclass
class Chat:
    id: str
    type: str
    name: str
    members: list #List[dict] 
    messages: list #List[dict]
    invite_codes: list #List[str]
    
class ChatsManager:
    def __init__(self):
        """Инициализация менеджера чатов"""
        self.chats = {}
        self.id = 0
        self.alphabet_for_invite_codes = "qwertyuiopasdfghjklzxcvbnm1234567890"
        
    def generate_invite_code(self) -> str:
        """Генерирует уникальный инвайт-код (ВНИМАНИЕ! РЕКУРСИЯ!)"""
        code = ''
        for _ in range(6): code = code + random.choice(self.alphabet_for_invite_codes)
        if self.check_invite_code_unique(code):
            return code
        else:
            return self.generate_invite_code()
        
    def check_invite_code_unique(self, invite_code: str) -> bool:
        """Проверяет уникальность кода-приглашения (True - уникален, False - нет)"""
        for chat_id in self.chats:
            chat = self.chats[chat_id]
            if chat.type == 'GROUP':
                for ic in chat.invite_codes:
                    if ic == invite_code:
                        return False
        else: return True
        
    def create_chat(self, accounts_manager, chat_type: str, chat_name: str, members_logins: list):
        """Создаёт чат с указанными параметрами"""
        for member_login in members_logins:
            if not accounts_manager.find_account_by_login(member_login):
                return 2001, None # Аккаунт с таким логином не найден
        
        current_chat_id = f'{self.id:09d}'
        self.chats[current_chat_id] = Chat(current_chat_id, chat_type, chat_name, [], [], [])
        self.id += 1
        
        if chat_type == 'GROUP':
            self.chats[current_chat_id].invite_codes.append(self.generate_invite_code())
        
        members = []
        for login in members_logins:
            account_id = accounts_manager.find_account_by_login(login)
            if account_id:
                members.append(accounts_manager.accounts[account_id])
                if self.add_member_to_chat(current_chat_id, members[-1]) == 2000:
                    return 2000, None # Аккаунт уже в чате
            else:
                return 2001, None # Аккаунт с таким логином не найден
        print(self.chats[current_chat_id])
        return 2100, self.chats[current_chat_id]  # Успех
        
    def add_member_to_chat(self, chat_id: str, account):
        """Добавляет клиента в указанный чат"""
        if not any(member_obj['id'] == account.id for member_obj in self.chats[chat_id].members):
            self.chats[chat_id].members.append({'id': account.id, 'login': account.login})
            
            account.chats_ids.append(chat_id)
            print(self.chats[chat_id])
            return 2100 # Успех
        
        else:
            return 2000 # Пользователь уже в чате
        
    def __get_chat_history(self, chat_id: str, number: int) -> dict:
        """Возвращает последние number сообщений в чате"""
        answer = self.chats[chat_id].__dict__
        answer['messages'] = answer['messages'][-number:]
        return answer
    
    def chats_history_for_account(self, accounts_manager, account_id: str) -> list:
        """Возвращает чаты (последние 30 соо) в которых есть указанный аккаунт"""
        chats_ids = accounts_manager.accounts[account_id].chats_ids
        chats_history = []
        for chat_id in chats_ids:
            chats_history.append(self.__get_chat_history(chat_id, 30))
        return chats_history
    
    def message_registation(self, accounts_manager, chat_id: str, message_text: str, author_login: str, timestamp: int):
        """Добавляет сообщение в чат и рассылает конкретно это новое сообщение всем участникам чата в сети"""
        new_message = {
            "message_text": message_text,
            "author_login": author_login,
            "timestamp": timestamp,
        }
        self.chats[chat_id].messages.append(new_message.copy())
        new_message['chat_id'] = chat_id
        new_message['type'] = "message"
        for account in self.chats[chat_id].members:
            account_id = account['id']
            accounts_manager.accounts[account_id].new.append(new_message)
        
    def new_chat_registration(self, accounts_manager, chat, account_id):
        """Присылает всем реал-таймам инфу о создании нового чата с ними"""
        new_chat = {
            "type": 'chat',
            "chat": chat.__dict__,
            }
        for account in chat.members:
            accounts_manager.accounts[account['id']].new.append(new_chat)
    
    def join_to_group_by_invite_code(self, accounts_manager, account_id: str, invite_code: str):
        for chat_id in self.chats:
            chat = self.chats[chat_id]
            if chat.type == 'GROUP':
                for ic in chat.invite_codes:
                    if ic == invite_code:
                        return self.add_member_to_chat(chat.id, accounts_manager.accounts[account_id])
        return 2002 # Инвайт код не действителен
                        



        
