import customtkinter as ctk

class MembersList:
    def __init__(self, main_page):
        self.main_page = main_page
        self.member_frames = []
    
    def create_members_list(self):
        """Создает область списка участников чата"""
        self.members_frame = ctk.CTkScrollableFrame(
            self.main_page.frame, width=150, height=600, corner_radius=15
        )
        self.members_frame.pack(side='right', anchor="ne", padx=5, pady=10, fill="y")
        
        self.members_title = ctk.CTkLabel(
            self.members_frame,
            text="Участники",
            font=("Arial", 16, "bold")
        )
        self.members_title.pack(pady=(10, 15))
        
    def update_members_list(self):
        """Обновляет список участников текущего чата"""
        for frame in self.member_frames:
            frame.destroy()
        self.member_frames.clear()
        
        if not self.main_page.current_chat_id:
            no_chat_label = ctk.CTkLabel(
                self.members_frame,
                text="Выберите чат",
                font=("Arial", 14),
                text_color="gray"
            )
            no_chat_label.pack(pady=10)
            self.member_frames.append(no_chat_label)
            return
            
        current_chat = self.main_page.find_chat_by_id(self.main_page.current_chat_id)
        if not current_chat:
            return
            
        for member in current_chat.get('members', []):
            self.add_member_item(member)
    
    def add_member_item(self, member):
        """Добавляет элемент участника в список"""
        member_frame = ctk.CTkFrame(
            self.members_frame, 
            height=40,
            corner_radius=10
        )
        member_frame.pack(fill="x", padx=5, pady=2)
        member_frame.pack_propagate(False)
        
        if member['login'] == self.main_page.client_socket.client_account.login:
            member_frame.configure(border_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"], border_width=2)
        
        member_label = ctk.CTkLabel(
            member_frame,
            text=member['login'],
            font=("Arial", 14),
            anchor="w"
        )
        member_label.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.member_frames.append(member_frame)