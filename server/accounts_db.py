from dataclasses import dataclass
from statuses_list import statuses

@dataclass
class Account:
    id: str
    login: str
    password_hash: str
    chats_ids: list #List[str]
    new_messages: list #List[dict]
    
class AccountsManager:
    def __init__(self):
        self.accounts = {}
        self.id = 0
        
    def create_new_account(self, login: str, password_hash: str):
        """Создаёт аккаунт"""
        if self.__check_login_uniqueness(login): # Если аккаунта с таким логином нет
            new_id = f'{self.id:09d}'
            self.accounts[new_id] = Account(new_id, login, password_hash, [], [])
            self.id += 1
            return 1100, new_id# Аккаунт создан
        else: # Если аккаунт с таким логином уже существует
            return 1000, None # Неудача
        
    def __check_login_uniqueness(self, login: str):
        """Проверка на уникальность логина""" #True если уникален, False если нет
        for key in self.accounts:
            account = self.accounts[key]
            if account.login == login:
                return False
        else:
            return True
    
    def authentication_handler(self, login: str, password_hash: str):
        """Проверяет возможность входа в аккаунт"""
        for key in self.accounts:
            account = self.accounts[key]
            if account.login == login:
                if account.password_hash == password_hash:
                    return 1101, key # Успех
                else: # Неверный пароль
                    return 1001, None # Неудача
        else: # Не нашёл аккаунта с таким логином
            return 1002, None # Неудача
    
    def find_account_by_login(self, login: str):
        """Ищет аккаунт с указанным логином и возвращает его id"""
        for key in self.accounts:
            account = self.accounts[key]
            if account.login == login:
                return key  # Успех
        else: # Не нашёл аккаунта с таким логином
            return None # Неудача

