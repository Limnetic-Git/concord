import customtkinter as ctk
import random

class CreateChatPage:
    def open_page(self, window, client_socket):
        self.window = window
        self.client_socket = client_socket
        
        self.frame = ctk.CTkFrame(self.window.app, fg_color="transparent")
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.private_chat_area()
        self.global_chat_area()
        self.UNPACK_back_button()
    
    def create_private_chat_action(self):
        if self.client_socket.client_account.login != self.enter_nick_field.get():
            self.client_socket.create_private_chat_request('NONE', [self.client_socket.client_account.login, self.enter_nick_field.get()])
            request_answer = self.client_socket.wait_for_request_answer('create_private_chat')
            if request_answer['status'] == 2001:
                self.enter_nick_field.configure(fg_color='#a51f1f')
            else:
                self.back_action()
        else:
            self.enter_nick_field.configure(fg_color='#a51f1f')
        
    def back_action(self):
        self.frame.destroy()
        self.window.open_page("message_board")
    
    def private_chat_area(self):
        self.private_chat_frame = ctk.CTkFrame(self.frame)
        self.private_chat_frame.pack(padx=10, pady=15)
        self.UNPACK_enter_nick_field()
        self.UNPACK_create_private_chat_button()
    
    def global_chat_area(self):
        self.global_chat_frame = ctk.CTkFrame(self.frame)
        self.global_chat_frame.pack(padx=10, pady=15)
        self.UNPACK_create_chat_button()
    
    def UNPACK_enter_nick_field(self):
        self.enter_nick_field = ctk.CTkEntry(
            self.private_chat_frame,
            placeholder_text="Никнейм друга",
            width=300,
            height=60)
        self.enter_nick_field.pack(padx=5, pady=5)
    
    def UNPACK_create_private_chat_button(self):
        self.create_private_chat_button = ctk.CTkButton(
            self.private_chat_frame,
            text="Создать ЛС",
            command=lambda: self.create_private_chat_action(), 
            width=300,
            height=40
        )
        self.create_private_chat_button.pack(padx=5, pady=5)
    
    def UNPACK_create_chat_button(self):
        self.create_chat_button = ctk.CTkButton(
            self.global_chat_frame,
            text="Создать многопользовательский чат",
            command=lambda: print('!'), 
            width=300,
            height=40
        )
        self.create_chat_button.pack(padx=5, pady=5)
        
    def UNPACK_back_button(self):
        self.back_button = ctk.CTkButton(
            self.frame,
            text="← Назад",
            command=lambda: self.back_action(),
            width=300,
            height=40
        )
        self.back_button.pack(pady=20)
