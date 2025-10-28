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
        
    def __client_thread(self, connection: tuple):
        """Поток запускаемый для каждого клиента в сети"""
        while True:
            incoming_pack = self.server.receive(connection, 20480, raw=False)
      
            pack = {}
            if 'request' in incoming_pack:
                if incoming_pack['request']['type'] == 'login':
                    pack['request_answer'] = {
                                        'type': 'login',
                                        'status': self.accounts_manager.authentication_handler(incoming_pack['request']['login'],
                                                                                                                           incoming_pack['request']['password']),
                                        }
                elif incoming_pack['request']['type'] == 'registration':
                    pack['request_answer'] = {
                                        'type': 'registration',
                                        'status': self.accounts_manager.create_new_account(incoming_pack['request']['login'],
                                                                                                                        incoming_pack['request']['password']),
                                        }
                elif incoming_pack['request']['type'] == 'create_private_chat':
                    pack['request_answer'] = {
                                        'type': 'create_private_chat',
                                        'status':  self.chats_manager.create_chat(
                                                    self.accounts_manager,
                                                    incoming_pack['request']['chat_type'],
                                                    incoming_pack['request']['chat_name'],
                                                    incoming_pack['request']['members_logins'])
                                        }
            self.server.send(connection, str(pack))



