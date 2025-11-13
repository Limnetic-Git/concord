import customtkinter as ctk
from datetime import datetime

class MainMessengerPage:
    def __init__(self):
        self.current_chat_id = None
        self.chats = []
        self.chat_buttons = []
        self.message_frames = []
        self.is_page_ready = False  # Флаг готовности страницы (отрисовки)
        
    @staticmethod
    def timestamp_to_datetime(seconds: int) -> str:
        return str(datetime.fromtimestamp(seconds))
    
    def new_handler(self, new: list):
        """Обработчик новых событий от сервера"""
        print(f'DEBUG new_handler: {new}')
        
        ignoring_message_drawing = False
        
        # Проверяем, что мы на правильной странице И страница готова (чтоб не пытаться рисовать если мы не на этой странице)
        if (self.window.current_page != "message_board" or 
            not self.is_page_ready):
            print(f"DEBUG: Ignoring new events, current page is {self.window.current_page}, page ready: {self.is_page_ready}")
            ignoring_message_drawing = True
            
        for action in new:
            if action['type'] == 'message':
                # Ищем чат для этого сообщения
                chat_found = False
                for chat in self.chats:
                    if chat['id'] == action['chat_id']:
                        new_message = {
                            "message_text": action["message_text"],
                            "author_login": action["author_login"],
                            "timestamp": action["timestamp"],
                        }
                        # Добавляем сообщение в чат
                        if 'messages' not in chat:
                            chat['messages'] = []
                        chat['messages'].append(new_message)
                        chat_found = True
                        
                        # Если это текущий открытый чат - показываем сообщение
                        if not ignoring_message_drawing and self.current_chat_id == chat['id']:
                            print(f"Adding message to current chat: {new_message}")
                            self.add_message(new_message)
                        break
                
                # Если чат не найден, релоадим чаты
                if not ignoring_message_drawing and not chat_found:
                    print("Chat not found, reloading chats...")
                    self.load_chats()
                    self.update_chats_list()
                        
            elif action['type'] == 'chat':
                # Добавляем новый чат если его нет
                chat_exists = any(chat['id'] == action['chat']['id'] for chat in self.chats)
                if not chat_exists:
                    print(f"Adding new chat: {action['chat']}")
                    self.chats.append(action['chat'])
                    if not ignoring_message_drawing:
                        self.add_chat_button(action['chat'])
                
    def open_page(self, window, client_socket):
        self.window = window 
        self.client_socket = client_socket
        self.is_page_ready = False 
        
        # Устанавливаем обработчик новых событий (функция которая выполняется при получении инфы о новых соо и чатах реалтайма)
        self.client_socket.new_handler_function = self.new_handler
    
        self.load_chats()
        self.frame = ctk.CTkFrame(self.window.app, fg_color="transparent")
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.create_chats_list()
        self.create_message_area()
        self.show_choose_chat_text()
        
        self.update_chats_list()
        
        self.is_page_ready = True  # Страница готова
        print("DEBUG: Page is ready for events")
    
    def load_chats(self):
        """Загружает чаты с сервера"""
        print("Loading chats from server...")
        self.client_socket.chats_history_request(self.client_socket.client_account.id)
        response = self.client_socket.wait_for_request_answer('chats_history')
        if response and 'chats_history' in response:
            self.chats = response['chats_history']
            print(f"Loaded {len(self.chats)} chats")
        else:
            self.chats = []
            print("No chats loaded")
    
    def create_chats_list(self):
        """Создает область списка чатов"""
        self.chats_frame = ctk.CTkScrollableFrame(
            self.frame, width=250, height=600, corner_radius=15
        )
        self.chats_frame.pack(side='left', anchor="nw", padx=5, pady=5, fill="y")
        
        # Кнопка создания чата
        self.plus_button = ctk.CTkButton(
            self.chats_frame, command=self.create_chat_page,
            text="+ Создать чат", width=182, height=50, 
            font=("Arial", 18, "bold")
        )
        self.plus_button.pack(padx=5, pady=10, fill="x")
    
    def create_message_area(self):
        """Создает область сообщений"""
        self.message_area = ctk.CTkFrame(
            self.frame, width=800, height=600, corner_radius=15
        )
        self.message_area.pack(side='left', padx=10, pady=5, expand=True, fill="both")
        self.message_area.grid_rowconfigure(0, weight=1)
        self.message_area.grid_rowconfigure(1, weight=0) 
        self.message_area.grid_columnconfigure(0, weight=1)
        
        # Область сообщений
        self.messages_frame = ctk.CTkScrollableFrame(
            self.message_area, corner_radius=10
        )
        self.messages_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        
        # Область ввода сообщения
        self.input_frame = ctk.CTkFrame(
            self.message_area, height=100, corner_radius=10
        )
        self.input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
        self.input_frame.grid_propagate(False)
    
    def show_choose_chat_text(self):
        """Показывает текст выбора чата"""
        self.choose_chat_text = ctk.CTkLabel(
            self.messages_frame, 
            text="Выберите чат для начала общения", 
            font=("Arial", 20, "bold")
        )
        self.choose_chat_text.pack(expand=True, pady=30)
    
    def update_chats_list(self):
        """Обновляет список чатов"""
        print("Updating chats list...")
        # Удаляем старые кнопки (кроме кнопки создания чата, она всегда сверху)
        for button in self.chat_buttons:
            button.destroy()
        self.chat_buttons.clear()
        
        # Создаем новые кнопки
        for chat in self.chats:
            self.add_chat_button(chat)
    
    def add_chat_button(self, chat):
        """Добавляет кнопку чата"""
        chat_name = chat['name']
        if chat['type'] == 'PRIVATE':
            for member in chat['members']:
                if member['login'] != self.client_socket.client_account.login:
                    chat_name = member['login']
                    break
                    
        button = ctk.CTkButton(
            self.chats_frame,
            command=lambda cid=chat['id']: self.select_chat(cid),
            text=chat_name,
            width=182,
            height=55,
            font=("Arial", 20, "bold"),
            anchor="w"
        )
        button.pack(padx=5, pady=5, fill="x")
        self.chat_buttons.append(button)
        print(f"Added chat button: {chat_name} (id: {chat['id']})")
    
    def select_chat(self, chat_id):
        """Выбирает чат"""
        print(f"Selecting chat: {chat_id}")
        self.current_chat_id = chat_id
        
        # Убираем текст с просьбой выбора чата
        if hasattr(self, 'choose_chat_text') and self.choose_chat_text.winfo_exists():
            self.choose_chat_text.destroy()
        
        self.clear_messages()
        self.show_messages()
        self.create_input_field()
    
    def clear_messages(self):
        """Очищает сообщения"""
        for frame in self.message_frames:
            frame.destroy()
        self.message_frames.clear()
    
    def show_messages(self):
        """Показывает сообщения выбранного чата"""
        chat = self.find_chat_by_id(self.current_chat_id)
        if chat:
            print(f"Showing messages for chat {chat['id']}, messages count: {len(chat.get('messages', []))}")
            if 'messages' in chat:
                for message in chat['messages']:
                    self.add_message(message)
    
    def find_chat_by_id(self, chat_id):
        """Находит чат по ID"""
        for chat in self.chats:
            if chat['id'] == chat_id:
                return chat
        return None
    
    def add_message(self, message):
        """Добавляет сообщение в список"""
        message_frame = ctk.CTkFrame(self.messages_frame)
        message_frame.pack(fill="x", padx=10, pady=5)
        
        author_text = ctk.CTkLabel(
            message_frame, 
            text=f"{message['author_login']}",
            font=("Arial", 18, 'bold'),
            wraplength=600,
            justify="left"
        )
        author_text.pack(padx=8, pady=5, anchor="w")
        
        message_text = ctk.CTkLabel(
            message_frame, 
            text=f"{message['message_text']}",
            font=("Arial", 16),
            wraplength=600,
            justify="left"
        )
        message_text.pack(padx=10, pady=2, anchor="w")

        timestamp_text = ctk.CTkLabel(
            message_frame, 
            text=f"{self.timestamp_to_datetime(message['timestamp'])}",
            font=("Arial", 9, 'bold'),
            wraplength=600,
            justify="right"
        )
        timestamp_text.pack(padx=8, pady=2, anchor="w")
        
        self.message_frames.append(message_frame)
        print(f"Added message: {message['author_login']}: {message['message_text']}")
        # Автоскролл
        self.messages_frame._parent_canvas.yview_moveto(1.0)
    
    def create_input_field(self):
        """Создает поле ввода сообщения"""
        # Очищаем старые элементы
        for widget in self.input_frame.winfo_children():
            widget.destroy()
            
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=0)  
        
        self.message_input = ctk.CTkTextbox(
            self.input_frame,
            height=80,
            corner_radius=10,
            font=("Arial", 14),
            wrap="word"
        )
        self.message_input.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
    
        self.message_input.insert("1.0", "Введите сообщение...")
        self.message_input.bind("<FocusIn>", self.clear_placeholder)
        self.message_input.bind("<FocusOut>", self.restore_placeholder)
        
        self.send_button = ctk.CTkButton(
            self.input_frame,
            command=self.send_message,
            text="Отправить",
            width=100,
            height=80,
            font=("Arial", 16, "bold"),
        )
        self.send_button.grid(row=0, column=1, sticky="ns", padx=(5, 10), pady=10)
    
    def clear_placeholder(self, event=None):
        """Очищает плейсхолдер при фокусе"""
        if self.message_input.get("1.0", "end-1c") == "Введите сообщение...":
            self.message_input.delete("1.0", "end")
    
    def restore_placeholder(self, event=None):
        """Восстанавливает плейсхолдер если поле пустое"""
        if not self.message_input.get("1.0", "end-1c").strip():
            self.message_input.insert("1.0", "Введите сообщение...")
    
    def send_message(self):
        """Отправляет сообщение"""
        message_text = self.message_input.get("1.0", "end-1c").strip()
        if message_text and message_text != "Введите сообщение...":
            print(f"Sending message to chat {self.current_chat_id}: {message_text}")
            
            # Отправляем на сервер
            self.client_socket.message_request(
                self.current_chat_id, 
                message_text, 
                self.client_socket.client_account.login
            )
            response = self.client_socket.wait_for_request_answer('message')
            
            if response:
                print("Message sent successfully")
                self.message_input.delete("1.0", "end")
            else:
                print("Failed to send message")
    
    def create_chat_page(self):
        """Переходит к созданию чата"""
        self.is_page_ready = False  # Страница больше не готова
        self.frame.destroy()
        self.window.open_page("create_chat")