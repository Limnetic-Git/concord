import customtkinter as ctk

class ChatList:
    def __init__(self, main_page):
        self.main_page = main_page
        self.chat_buttons = []
    
    def create_chats_list(self):
        """Создает область списка чатов"""
        self.chats_frame = ctk.CTkScrollableFrame(
            self.main_page.frame, width=200, height=600, corner_radius=15
        )
        self.chats_frame.pack(side='left', anchor="nw", padx=5, pady=10, fill="y")
        
        self.plus_button = ctk.CTkButton(
            self.chats_frame, command=self.main_page.create_chat_page,
            text="+ Создать чат", width=182, height=50, 
            font=("Arial", 18, "bold")
        )
        self.plus_button.pack(padx=5, pady=10, fill="x")
        self.chats_frame.bind("<Button-4>", lambda e: self.chats_frame._parent_canvas.yview_scroll(-1, "units"))
        self.chats_frame.bind("<Button-5>", lambda e: self.chats_frame._parent_canvas.yview_scroll(1, "units"))
    
    def update_chats_list(self):
        """Обновляет список чатов"""
        print("Updating chats list...")
        for button in self.chat_buttons:
            button.destroy()
        self.chat_buttons.clear()
        
        for chat in self.main_page.chats:
            self.add_chat_button(chat)
    
    def add_chat_button(self, chat):
        """Добавляет кнопку чата"""
        chat_name = chat['name']
        if chat['type'] == 'PRIVATE':
            for member in chat['members']:
                if member['login'] != self.main_page.client_socket.client_account.login:
                    chat_name = member['login']
                    break
                    
        button = ctk.CTkButton(
            self.chats_frame,
            command=lambda cid=chat['id']: self.main_page.select_chat(cid),
            text=chat_name,
            width=182,
            height=55,
            font=("Arial", 20, "bold"),
            anchor="w"
        )
        button.pack(padx=5, pady=5, fill="x")
        self.chat_buttons.append(button)
        print(f"Added chat button: {chat_name} (id: {chat['id']})")
        button.bind("<Button-4>", lambda e: self.chats_frame._parent_canvas.yview_scroll(-1, "units"))
        button.bind("<Button-5>", lambda e: self.chats_frame._parent_canvas.yview_scroll(1, "units"))