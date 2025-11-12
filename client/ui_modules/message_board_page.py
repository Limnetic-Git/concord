import customtkinter as ctk

class MainMessengerPage:
    def __init__(self):
        self.current_chat_id = None
        self.chats_list = []
        self.messages_list = []
        
    def new_handler(self, new: list):
        print(f'ABOBA: {new}')
        for action in new:
            if action['type'] == 'message':
                for chat in self.chats:
                    if chat['id'] == action['chat_id']:
                        new_message = {
                            "message_text": action["message_text"],
                            "author_login": action["author_login"],
                            "timestamp": action["timestamp"],
                            }
                        chat['messages'].append(new_message)
                        if self.window == "message_board" and self.current_chat_id == chat['id']:
                            self.add_message_to_message_list(new_message)
                        break
            elif action['type'] == 'chat':
                self.chats.append(action['chat'])
                self.add_chat_to_chats_list(action['chat'])
                
                        

        
    
    def open_page(self, window, client_socket):
        self.window = window 
        self.client_socket = client_socket
        
        self.client_socket.chats_history_request(self.client_socket.client_account.id)
        self.chats = self.client_socket.wait_for_request_answer('chats_history')['chats_history']
        print(self.chats)
        
        self.client_socket.new_handler_function = self.new_handler

        self.frame = ctk.CTkFrame(self.window.app, fg_color="transparent")
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)
        self.UNPACK_chats_list_rect()
        self.UNPACK_message_area_rect()
        self.UNPACK_choose_chat_text()
        
        self.UNPACK_plus_button()
        self.update_chats_list()
    
    def create_chat_page_action(self):
        self.frame.destroy()
        self.window.open_page("create_chat")
    
    def send_message_action(self):
        self.client_socket.message_request(self.current_chat_id, self.enter_message_field.get("1.0", "end-1c"), self.client_socket.client_account.login)
        self.client_socket.wait_for_request_answer('message')
        self.enter_message_field.delete("1.0", "end")
    
    # --- UI элементы на странице: ---
    def UNPACK_message_writing_field(self):
        self.UNPACK_enter_message_field()
        self.UNPACK_send_message_button()
        
    def UNPACK_chats_list_rect(self):
        """Создает область списка чатов"""
        self.chats_list_rect = ctk.CTkScrollableFrame(
            self.frame,
            width=250,
            height=600,
            corner_radius=15,
        )
        self.chats_list_rect.pack(side='left', anchor="nw", padx=5, pady=5, fill="y")
        
    def UNPACK_message_area_rect(self):
        """Создает основную область для сообщений и ввода"""
        self.message_area_rect = ctk.CTkFrame(
            self.frame,
            width=800,
            height=600,
            corner_radius=15,
        )
        self.message_area_rect.pack(side='left', padx=10, pady=5, expand=True, fill="both")
        self.message_area_rect.grid_rowconfigure(0, weight=1)
        self.message_area_rect.grid_rowconfigure(1, weight=0) 
        self.message_area_rect.grid_columnconfigure(0, weight=1)
        
        self.message_rect = ctk.CTkScrollableFrame(
            self.message_area_rect,
            corner_radius=10)
        self.message_rect.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        self.enter_message_rect = ctk.CTkFrame(
            self.message_area_rect,
            height=100,
            corner_radius=10)
        self.enter_message_rect.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
        self.enter_message_rect.grid_propagate(False)  

    def UNPACK_enter_message_field(self):
        """Создает поле ввода сообщения"""
        self.enter_message_rect.grid_columnconfigure(0, weight=1)
        self.enter_message_rect.grid_columnconfigure(1, weight=0)  
        
        self.enter_message_field = ctk.CTkTextbox(
            self.enter_message_rect,
            height=80,
            corner_radius=10,
            font=("Arial", 14),
            wrap="word"
        )
        self.enter_message_field.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        self.enter_message_field.insert("1.0", "Введите сообщение...")
        self.enter_message_field.bind("<FocusIn>", lambda e: self.clear_placeholder() if self.enter_message_field.get("1.0", "end-1c") == "Введите сообщение..." else None)
    
    def UNPACK_plus_button(self):
        """Создает кнопку добавления чата"""
        self.plus_button = ctk.CTkButton(
            self.chats_list_rect,
            command=lambda: self.create_chat_page_action(),
            text="+ Создать чат",
            width=182,
            height=50,
            font=("Arial", 18, "bold"))
        self.plus_button.pack(padx=5, pady=10, fill="x")
        
    def UNPACK_send_message_button(self):
        """Создает кнопку отправки сообщения"""
        self.send_message_button = ctk.CTkButton(
            self.enter_message_rect,
            command=lambda: self.send_message_action(),
            text="Отправить",
            width=100,
            height=80,
            font=("Arial", 16, "bold"),
        )
        self.send_message_button.grid(row=0, column=1, sticky="ns", padx=(5, 10), pady=10)
    
    def UNPACK_choose_chat_text(self):
        """Создает текст с просьбой выбора чата"""
        self.choose_chat_text = ctk.CTkLabel(
            self.message_rect, 
            text="Выберите чат для начала общения", 
            font=("Arial", 20, "bold"))
        self.choose_chat_text.pack(expand=True, pady=30)
    
    def change_chat_to(self, chat_id):
        self.current_chat_id = chat_id
        print(f'Chat changed to: {self.current_chat_id}')
        self.choose_chat_text.destroy()
        self.update_messages_list()
        self.UNPACK_message_writing_field()
        
    def _change_chat_handler(self, chat_id):
        """Создает обработчик для кнопки чата"""
        return lambda: self.change_chat_to(chat_id)

    def add_chat_to_chats_list(self, chat: dict):
        """Добавляет кнопку чата в лист чатов"""
        chat_name = chat['name']
        if chat['type'] == 'PRIVATE':
            for member in chat['members']:
                if member['login'] != self.client_socket.client_account.login:
                    chat_name = member['login']
                    
        button = ctk.CTkButton(
            self.chats_list_rect,
            command=self._change_chat_handler(chat['id']),
            text=chat_name,
            width=182,
            height=55,
            font=("Arial", 20, "bold"),
            anchor="w")
        button.pack(padx=5, pady=5, fill="x")
        
    def clear_placeholder(self):
        """Очищает подсказку в поле ввода"""
        if self.enter_message_field.get("1.0", "end-1c") == "Введите сообщение...":
            self.enter_message_field.delete("1.0", "end")

    def update_chats_list(self):
        """Обновляет список чатов"""
        for chat_button in self.chats_list:
            chat_button.destroy()
        for chat in self.chats:
            self.add_chat_to_chats_list(chat)
    
    def update_messages_list(self):
        for message_frame in self.messages_list:
            message_frame.destroy()
            self.messages_list.remove(message_frame)
        current_chat_id = 0
        for i, chat in enumerate(self.messages_list):
            if self.current_chat_id == chat['id']:
                current_chat_id = i
        for message in self.chats[current_chat_id]['messages']:
            self.add_message_to_message_list(message)
    
    def add_message_to_message_list(self, message: dict):
        message_frame = ctk.CTkFrame(self.message_rect)
        message_frame.pack(fill="x", padx=10, pady=5)
        
        message_text = ctk.CTkLabel(
            message_frame, 
            text=f"{message['author_login']}: {message['message_text']}",
            font=("Arial", 14),
            wraplength=600,
            justify="left")
        
        self.messages_list.append(message_frame)
        message_text.pack(padx=10, pady=5, anchor="w")
        
    
    
        
        
