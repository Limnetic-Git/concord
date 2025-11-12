import customtkinter as ctk
import random

class CreateChatPage:
    def open_page(self, window, client_socket):
        self.window = window
        self.client_socket = client_socket
        
        self.frame = ctk.CTkFrame(self.window.app, fg_color="transparent")
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.UNPACK_enter_nick_field()
        self.UNPACK_create_private_chat_button()
        self.UNPACK_create_chat_button()
        self.UNPACK_back_button()
    
    def create_private_chat_action(self):
        self.client_socket.create_private_chat_request('NONE', [self.client_socket.client_account.login, self.enter_nick_field.get()])
        self.client_socket.wait_for_request_answer('create_private_chat')
        self.back_action()
        
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
