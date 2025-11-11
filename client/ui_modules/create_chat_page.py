import customtkinter as ctk
import random

class CreateChatPage:
    def __init__(self):
        pass
    
    def open(self, **kwargs):
        
        self.window = kwargs['window']
        self.client_socket = kwargs['client_socket']
        self.account = kwargs['account'] 
        
    
        self.frame = ctk.CTkFrame(self.window.app, fg_color="transparent")
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.UNPACK_enter_nick_field()
        self.UNPACK_create_private_chat_button()
        self.UNPACK_create_chat_button()
        self.UNPACK_back_button()
    
    
    def create_private_chat_action(self):
        self.client_socket.create_chat_request([self.account.login, self.enter_nick_field.get()], 'private')
        while not isinstance(self.client_socket.result, bool):
            pass
        self.client_socket.result = None
        
    def back_action(self):
        self.frame.destroy()
        self.window.open_page("message_board")
        
    def UNPACK_enter_nick_field(self):
        self.enter_nick_field = ctk.CTkEntry(
            self.frame,
            placeholder_text="Никнейм друга",
            width=300,
            height=60)
        self.enter_nick_field.pack(pady=35)
    
    def UNPACK_create_private_chat_button(self):
        self.create_private_chat_button = ctk.CTkButton(
            self.frame,
            text="Создать ЛС",
            command=lambda: self.create_private_chat_action(), 
            width=300,
            height=40
        )
        self.create_private_chat_button.pack(pady=15)
    
    def UNPACK_create_chat_button(self):
        self.create_chat_button = ctk.CTkButton(
            self.frame,
            text="Создать многопользовательский чат",
            command=lambda: print('!'), 
            width=300,
            height=40
        )
        self.create_chat_button.pack(pady=35)
        
    def UNPACK_back_button(self):
        self.back_button = ctk.CTkButton(
            self.frame,
            text="← Назад",
            command=lambda: self.back_action(),
            width=300,
            height=40
        )
        self.back_button.pack(pady=20)
