import customtkinter as ctk

class MessageBoardPage:
    def __init__(self):
        self.chat = None
        self.chat_index = None
        self.messages = []
        self.chat_buttons = []
        self.current_widgets = []  # Для отслеживания текущих виджетов
    
    def clear_frame(self):
        """Очищает все виджеты на странице"""
        for widget in self.current_widgets:
            widget.destroy()
        self.current_widgets.clear()
    
    def open(self, **kwargs):
        self.window = kwargs['window']
        self.client_socket = kwargs['client_socket']
        self.account = kwargs['account']
        
        self.client_socket.take_message_board_page(self)
        # Очищаем предыдущие виджеты
        self.clear_frame()
        
        # Создаем основной фрейм
        self.frame = ctk.CTkFrame(self.window.app, fg_color="transparent")
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)
        self.current_widgets.append(self.frame)
        
        # Создаем интерфейс
        self.UNPACK_chats_list_rect()
        self.UNPACK_message_area_rect()  # Область для сообщений и ввода
        self.UNPACK_plus_button()
        self.UNPACK_chats_buttons()

        # Обновляем область сообщений в зависимости от выбранного чата
        self.update_message_area()
            
    def create_chat_action(self):
        """Создание нового чата"""
        self.frame.destroy()
        self.window.open_page("create_chat")
    
    def change_chat_to(self, chat_id):
        """Смена активного чата"""
        self.chat = chat_id
        self.update_message_area()
        
    def update_message_area(self):
        """Обновляет область сообщений в зависимости от выбранного чата"""
        # Очищаем message_rect (область сообщений)
        for widget in self.message_rect.winfo_children():
            widget.destroy()
        
        # Очищаем enter_message_rect (область ввода)
        for widget in self.enter_message_rect.winfo_children():
            widget.destroy()
        
        if self.chat:
            self.UNPACK_enter_message_field()
            self.UNPACK_send_message_button()
            # Здесь можно добавить загрузку сообщений для выбранного чата
            self.load_chat_messages()
        else:
            self.UNPACK_choose_chat_text()
            
        canvas = self.message_rect._parent_canvas
        canvas.yview_moveto(1.0)
            
    def load_chat_message(self, message):
        message_frame = ctk.CTkFrame(self.message_rect, fg_color="#2b2b2b")
        message_frame.pack(fill="x", padx=10, pady=5)
        
        message_text = ctk.CTkLabel(
            message_frame, 
            text=f"{message['author']}: {message['text']}",
            font=("Arial", 14),
            wraplength=600,
            justify="left"
        )
        message_text.pack(padx=10, pady=5, anchor="w")
        
    def load_chat_messages(self):
        """Загружает сообщения для выбранного чата"""
        chat_label = ctk.CTkLabel(
            self.message_rect, 
            text=f"Чат {self.chat} - сообщения будут здесь", 
            font=("Arial", 18, "bold")
        )
        chat_label.pack(pady=20)
        
        for i, chat in enumerate(self.account.chats_db):
            if chat['id'] == self.chat:
                self.chat_index = i
                break

        for message in self.account.chats_db[self.chat_index]['messages']:
            self.load_chat_message(message)
        
    def UNPACK_chats_buttons(self):
        """Создает кнопки чатов"""
        self.chat_buttons = []
        
        for chat in self.account.chats_db:
            chat_name = 'None'
            print(self.account.chats_db, type(self.account.chats_db))
            print(chat)
            
            if chat['type'] == "private":
                for name in chat['members_nicks']:
                    if name != self.account.login:
                        chat_name = name; break
            else:
                chat_name = chat['name']
                
            button = ctk.CTkButton(
                self.chats_list_rect,
                command=self._create_chat_handler(chat['id']),
                text=chat_name,
                width=182,
                height=55,
                font=("Arial", 20, "bold"),
                anchor="w"
            )
            button.pack(padx=5, pady=5, fill="x")
            self.chat_buttons.append(button)

    def _create_chat_handler(self, chat_id):
        """Создает обработчик для кнопки чата"""
        return lambda: self.change_chat_to(chat_id)
    
    def UNPACK_chats_list_rect(self):
        """Создает область списка чатов"""
        self.chats_list_rect = ctk.CTkScrollableFrame(
            self.frame,
            width=250,
            height=600,
            corner_radius=15,
            scrollbar_button_color="#2b2b2b",
            scrollbar_button_hover_color="#3b3b3b",
            fg_color="#2b2b2b"
        )
        self.chats_list_rect.pack(side='left', anchor="nw", padx=5, pady=5, fill="y")
        self.current_widgets.append(self.chats_list_rect)
    
    def UNPACK_message_area_rect(self):
        """Создает основную область для сообщений и ввода"""
        self.message_area_rect = ctk.CTkFrame(
            self.frame,
            width=800,
            height=600,
            corner_radius=15,
            fg_color="#1f1f1f"
        )
        self.message_area_rect.pack(side='left', padx=10, pady=5, expand=True, fill="both")
        self.message_area_rect.grid_rowconfigure(0, weight=1)  # Сообщения занимают все доступное пространство
        self.message_area_rect.grid_rowconfigure(1, weight=0)  # Область ввода фиксированной высоты
        self.message_area_rect.grid_columnconfigure(0, weight=1)
        self.current_widgets.append(self.message_area_rect)
        
        # Область сообщений с прокруткой
        self.message_rect = ctk.CTkScrollableFrame(
            self.message_area_rect,
            corner_radius=10,
            fg_color="#1a1a1a",
            scrollbar_button_color="#2b2b2b",
            scrollbar_button_hover_color="#3b3b3b"
        )
        self.message_rect.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        
        # Область ввода сообщения
        self.enter_message_rect = ctk.CTkFrame(
            self.message_area_rect,
            height=100,
            corner_radius=10,
            fg_color="#2b2b2b"
        )
        self.enter_message_rect.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
        self.enter_message_rect.grid_propagate(False)  # Фиксируем высоту
        
    def UNPACK_plus_button(self):
        """Создает кнопку добавления чата"""
        self.plus_button = ctk.CTkButton(
            self.chats_list_rect,
            command=lambda: self.create_chat_action(),
            text="+ Создать чат",
            width=182,
            height=50,
            font=("Arial", 18, "bold"),
            fg_color="#3b8ed0",
            hover_color="#2a6ca6"
        )
        self.plus_button.pack(padx=5, pady=10, fill="x")

    def UNPACK_enter_message_field(self):
        """Создает поле ввода сообщения"""
        self.enter_message_rect.grid_columnconfigure(0, weight=1)  # Поле ввода занимает все пространство
        self.enter_message_rect.grid_columnconfigure(1, weight=0)  # Кнопка фиксированной ширины
        
        self.enter_message_field = ctk.CTkTextbox(
            self.enter_message_rect,
            height=80,
            corner_radius=10,
            font=("Arial", 14),
            wrap="word"
        )
        self.enter_message_field.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        
        # Добавляем подсказку
        self.enter_message_field.insert("1.0", "Введите сообщение...")
        self.enter_message_field.bind("<FocusIn>", lambda e: self.clear_placeholder() if self.enter_message_field.get("1.0", "end-1c") == "Введите сообщение..." else None)
    
    def clear_placeholder(self):
        """Очищает подсказку в поле ввода"""
        if self.enter_message_field.get("1.0", "end-1c") == "Введите сообщение...":
            self.enter_message_field.delete("1.0", "end")
            
    def send_message_action(self):
        self.client_socket.actions.append({"type": "message", "chat_id": self.chat, "text": self.enter_message_field.get("1.0", "end-1c"), "author": self.account.login})
        self.enter_message_field.delete("1.0", "end")
        #self.update_message_area()
        
    def UNPACK_send_message_button(self):
        """Создает кнопку отправки сообщения"""
        self.send_message_button = ctk.CTkButton(
            self.enter_message_rect,
            command=lambda: self.send_message_action(),
            text="Отправить",
            width=100,
            height=80,
            font=("Arial", 16, "bold"),
            fg_color="#28a745",
            hover_color="#218838"
        )
        self.send_message_button.grid(row=0, column=1, sticky="ns", padx=(5, 10), pady=10)
        
    def UNPACK_choose_chat_text(self):
        """Создает текст выбора чата"""
        self.choose_chat_text = ctk.CTkLabel(
            self.message_rect, 
            text="Выберите чат для начала общения", 
            font=("Arial", 20, "bold"),
            text_color="#6c757d"
        )
        self.choose_chat_text.pack(expand=True, pady=30)