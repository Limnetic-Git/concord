import socket_modules.pysocknet as pysocknet
from _thread import *
import time
import hashlib

class ClientSocket:
    def __init__(self, ip='127.0.0.1', port=1234):
        """Инициализация сокета клиента"""
        self.ip = ip
        self.port = port
        
        self.tasks_queue = [] # Список тасков (действий) которые отсылаются серверу (по одному за итерацию потока)
        self.pack = {} # То что бы будем отправлять серверу
        self.incoming_pack = {} # То что мы будем получать от сервера
        self.last_request_answer = None # Ответ сервера на наш последний таск который мы его отсылали
        
        connection = pysocknet.TCPClientConnection(self.ip, self.port)
        start_new_thread(self.__socket_tread, (connection,))
    
    @staticmethod
    def __get_string_hash(string: str) -> str:
        """Возвращает SHA-256 хэш строки"""
        hash_object = hashlib.sha256()
        hash_object.update(string.encode())
        return str(hash_object.hexdigest())

    def __socket_tread(self, connection: pysocknet.TCPClientConnection):
        """Цикл общения клиента с сервером"""
        while True:
            self.pack = {}
            if self.tasks_queue: # Если очередь не пуста
                self.pack['request'] = self.tasks_queue[0]
                self.tasks_queue.pop(0)
                
            connection.send(str(self.pack))
            self.incoming_pack = connection.receive(20480, raw=False)
            if 'request_answer' in self.incoming_pack: # Если сервер отвечает на наш запрос
                self.last_request_answer = self.incoming_pack['request_answer'].copy()
                
    def wait_for_request_answer(self, request_type: str) -> dict:
        """Ждёт пока не получил ответ на заданный запрос и возвращает его"""
        start_time = time.time()
        while True:
            if self.last_request_answer:
                if self.last_request_answer['type'] == request_type:
                    return self.last_request_answer.copy()
            if time.time() - start_time > 5:
                raise TimeoutError(f'Timeout waiting for "{request_type}" response')
            time.sleep(0.01)
            
    def login_request(self, login: str, password: str):
        """Создаёт запрос на логин"""
        self.tasks_queue.append({
            "type": 'login',
            "login": login,
            "password": self.__get_string_hash(password),
            })
        
    def registration_request(self, login: str, password: str):
        """Создаёт запрос на регистрацию"""
        self.tasks_queue.append({
            "type": 'registration',
            "login": login,
            "password": self.__get_string_hash(password),
            })
        
    def create_private_chat_request(self, chat_name: str, members_logins: list):
        """Создаёт запрос на создание приватного чата (ЛС)"""
        self.tasks_queue.append({
            "type": 'create_private_chat',
            "chat_name": chat_name,
            "chat_type": 'PRIVATE',
            "members_logins": members_logins,
            })
    
    def chats_history_request(self, account_id: str):
        """Создаёт запрос на историю текстовых чатов в которых состоит аккаунт"""
        self.tasks_queue.append({
            "type": 'chats_history',
            "id": account_id,
            })
        
    