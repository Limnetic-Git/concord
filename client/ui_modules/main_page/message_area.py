import customtkinter as ctk

class MessageArea:
    def __init__(self, main_page):
        self.main_page = main_page
        self.message_frames = []
    
    def create_message_area(self):
        """Создает область сообщений"""
        self.message_area = ctk.CTkFrame(
            self.main_page.frame, width=800, height=600, corner_radius=15
        )
        self.message_area.pack(side='left', padx=10, pady=10, expand=True, fill="both")
        self.message_area.grid_rowconfigure(0, weight=1)
        self.message_area.grid_rowconfigure(1, weight=0) 
        self.message_area.grid_columnconfigure(0, weight=1)
        
        self.messages_frame = ctk.CTkScrollableFrame(
            self.message_area, corner_radius=10
        )
        self.messages_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        
        self.messages_frame.bind("<Button-4>", lambda e: self.messages_frame._parent_canvas.yview_scroll(-1, "units"))
        self.messages_frame.bind("<Button-5>", lambda e: self.messages_frame._parent_canvas.yview_scroll(1, "units"))

    def show_choose_chat_text(self):
        """Показывает текст выбора чата"""
        self.choose_chat_text = ctk.CTkLabel(
            self.messages_frame, 
            text="Выберите чат для начала общения", 
            font=("Arial", 20, "bold")
        )
        self.choose_chat_text.pack(expand=True, pady=30)
    
    def select_chat(self):
        """Обрабатывает выбор чата в области сообщений"""
        if hasattr(self, 'choose_chat_text') and self.choose_chat_text.winfo_exists():
            self.choose_chat_text.destroy()
        
        self.clear_messages()
        self.show_messages()
    
    def clear_messages(self):
        """Очищает сообщения"""
        for frame in self.message_frames:
            frame.destroy()
        self.message_frames.clear()
    
    def show_messages(self):
        """Показывает сообщения выбранного чата"""
        chat = self.main_page.find_chat_by_id(self.main_page.current_chat_id)
        if chat:
            print(f"Showing messages for chat {chat['id']}, messages count: {len(chat.get('messages', []))}")
            if 'messages' in chat:
                for message in chat['messages']:
                    self.add_message(message)
    
    def add_message(self, message):
        """Добавляет сообщение в список"""
        message_frame = ctk.CTkFrame(self.messages_frame)
        
        if message['author_login'] == self.main_page.client_socket.client_account.login:
            message_frame.configure(border_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"], border_width=2)
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
            justify="left",
        )
        message_text.pack(padx=13, pady=2, anchor="w")

        timestamp_text = ctk.CTkLabel(
            message_frame, 
            text=f"{self.main_page.timestamp_to_datetime(message['timestamp'])}",
            font=("Arial", 9, 'bold'),
            wraplength=600,
            justify="right"
        )
        timestamp_text.pack(padx=8, pady=2, anchor="w")
        
        self.message_frames.append(message_frame)
        print(f"Added message: {message['author_login']}: {message['message_text']}")
        
        self.messages_frame._parent_canvas.yview_moveto(1.0)

        message_frame.bind("<Button-4>", lambda e: self.messages_frame._parent_canvas.yview_scroll(-1, "units"))
        message_frame.bind("<Button-5>", lambda e: self.messages_frame._parent_canvas.yview_scroll(1, "units"))