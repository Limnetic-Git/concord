import customtkinter as ctk
from ui_modules.main_page.chats_list import ChatList
from ui_modules.main_page.message_area import MessageArea
from ui_modules.main_page.members_list import MembersList
from ui_modules.main_page.input_field import InputField
from datetime import datetime

class MainMessengerPage:
    def __init__(self):
        self.current_chat_id = None
        self.chats = []
        self.is_page_ready = False
        self.global_init = False
        
    @staticmethod
    def timestamp_to_datetime(seconds: int) -> str:
        """Переводит time.time в время на компьютере"""
        return str(datetime.fromtimestamp(seconds))
    
    def new_handler(self, new: list):
        """Обработчик новых событий от сервера"""
        print(f'DEBUG new_handler: {new}')
        
        ignoring_message_drawing = False
        
        if (self.window.current_page != "message_board" or 
            not self.is_page_ready):
            print(f"DEBUG: Ignoring new events, current page is {self.window.current_page}, page ready: {self.is_page_ready}")
            ignoring_message_drawing = True
            
        for action in new:
            if action['type'] == 'message':
                chat_found = False
                for chat in self.chats:
                    if chat['id'] == action['chat_id']:
                        new_message = {
                            "message_text": action["message_text"],
                            "author_login": action["author_login"],
                            "timestamp": action["timestamp"],
                        }
                        if 'messages' not in chat:
                            chat['messages'] = []
                        chat['messages'].append(new_message)
                        chat_found = True
                        
                        if not ignoring_message_drawing and self.current_chat_id == chat['id']:
                            print(f"DEBUG: Adding message to current chat: {new_message}")
                            self.message_area.add_message(new_message)
                        break

                
                if not ignoring_message_drawing and not chat_found:
                    print("DEBUG: Chat not found, reloading chats...")
                    self.load_chats()
                    self.chat_list.update_chats_list()
                        
            elif action['type'] == 'chat':
                for i, chat in enumerate(self.chats):
                    if chat['id'] == action['chat']['id']:
                        self.chats[i]['members'] = action['chat']['members']
                        if self.is_page_ready:
                            if self.current_chat_id == chat['id']:
                                self.members_list.update_members_list()
                        break
        
                else:
                    print(f"DEBUG: Adding new chat: {action['chat']}")
                    self.chats.append(action['chat'])
                    if not ignoring_message_drawing:
                        self.chat_list.add_chat_button(action['chat'])

                    
    def open_page(self, window, client_socket):
        self.window = window 
        self.client_socket = client_socket
        self.is_page_ready = False 
        
        self.client_socket.new_handler_function = self.new_handler
        
        if not self.global_init:
            self.load_chats()
            
        self.frame = ctk.CTkFrame(self.window.app, fg_color="transparent")
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Инициализация компонентов
        self.chat_list = ChatList(self)
        self.members_list = MembersList(self)
        self.message_area = MessageArea(self)
        self.input_field = InputField(self)
        
        self.chat_list.create_chats_list()
        self.members_list.create_members_list()
        self.message_area.create_message_area()
        self.message_area.show_choose_chat_text()
        
        self.chat_list.update_chats_list()
        
        self.is_page_ready = True
        self.global_init = True
        print("DEBUG: Page is ready for events")
    
    def load_chats(self):
        """Загружает чаты с сервера"""
        print("LOG: Loading chats from server...")
        self.client_socket.chats_history_request(self.client_socket.client_account.id)
        response = self.client_socket.wait_for_request_answer('chats_history')
        if response and 'chats_history' in response:
            self.chats = response['chats_history']
            print(f"LOG: Loaded {len(self.chats)} chats")
        else:
            self.chats = []
            print("LOG: No chats loaded")
    
    def select_chat(self, chat_id):
        """Выбирает чат"""
        print(f"LOG: Selecting chat: {chat_id}")
        self.current_chat_id = chat_id
        
        self.message_area.select_chat()
        self.input_field.create_input_field()
        self.members_list.update_members_list()
    
    def find_chat_by_id(self, chat_id):
        """Находит чат по ID"""
        for chat in self.chats:
            if chat['id'] == chat_id:
                return chat
        return None
    
    def create_chat_page(self):
        """Переходит к созданию чата"""
        self.is_page_ready = False
        self.frame.destroy()
        self.window.open_page("create_chat")