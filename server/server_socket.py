import pysocknet
from _thread import *

class ServerSocket:
    def __init__(self, accounts_manager, chats_manager, ip='127.0.0.1', port=1234):
        """Инициализация сервера"""
        self.ip = ip
        self.port = port
        
        self.accounts_manager = accounts_manager
        self.chats_manager = chats_manager
        
        self.server = pysocknet.TCPServerConnection(self.ip, self.port)
        self.server.start_client_accepting_loop(self.__client_thread)
        
    def __clear_new_messages(self, account_id: str):
        """Очищает новые сообщения в реал-тайм потоке"""
        self.accounts_manager.accounts[account_id].new = []
        
    def __client_thread(self, connection: tuple):
        """Поток запускаемый для каждого клиента в сети"""
        treading_account_id = None # Если None - аккаунт не авторизован
        
        while True:
            incoming_pack = self.server.receive(connection, 20480, raw=False)
      
            pack = {}
            if 'request' in incoming_pack:
                if incoming_pack['request']['type'] == 'login':
                    status, account_id = self.accounts_manager.authentication_handler(incoming_pack['request']['login'],
                                                                                                                           incoming_pack['request']['password'])
                    pack['request_answer'] = {
                                        'type': 'login',
                                        'status': status,
                                        'id': account_id,
                                        }
                    treading_account_id = account_id
                    if treading_account_id: # Зашел в аккаунт
                        self.__clear_new_messages(treading_account_id)
                        
                    
                elif incoming_pack['request']['type'] == 'registration':
                    status, account_id = self.accounts_manager.create_new_account(incoming_pack['request']['login'],
                                                                                                                        incoming_pack['request']['password'])
                    pack['request_answer'] = {
                                        'type': 'registration',
                                        'status': status,
                                        'id': account_id,
                                        }
                    treading_account_id = account_id
                    if treading_account_id: # Зашел в аккаунт
                        self.__clear_new_messages(treading_account_id)
                    
                elif incoming_pack['request']['type'] == 'create_private_chat':
                    
                    status, chat = self.chats_manager.create_chat(
                                                    self.accounts_manager,
                                                    incoming_pack['request']['chat_type'],
                                                    incoming_pack['request']['chat_name'],
                                                    incoming_pack['request']['members_logins'])
                    pack['request_answer'] = {
                                        'type': 'create_private_chat',
                                        'status': status,
                                        }
                    if chat: # чат создался
                        self.chats_manager.new_chat_registration(self.accounts_manager, chat, account_id)
                        
                elif incoming_pack['request']['type'] == 'chats_history':
                    pack['request_answer'] = {
                                        'type': 'chats_history',
                                        'chats_history': self.chats_manager.chats_history_for_account(
                                                            self.accounts_manager,
                                                            incoming_pack['request']['id']),
                                        }
                elif incoming_pack['request']['type'] == 'message':
                    pack['request_answer'] = {
                        'type': 'message',
                        'status': self.chats_manager.message_registation(
                            self.accounts_manager,
                            incoming_pack['request']['chat_id'],
                            incoming_pack['request']['message_text'],
                            incoming_pack['request']['author_login'],
                            incoming_pack['request']['timestamp']),
                                             }
            if treading_account_id:
                new_pack = []
                
                for i, new_event in enumerate(self.accounts_manager.accounts[treading_account_id].new):
                    new_pack.append(new_event)
                    self.accounts_manager.accounts[treading_account_id].new.pop(i)

            
                pack['new'] = new_pack
                    
            self.server.send(connection, str(pack))



