import customtkinter as ctk

class LoginPage:
    def open_page(self, window, client_socket):
        
        self.window = window 
        self.client_socket = client_socket
        
        self.frame = ctk.CTkFrame(self.window.app, fg_color="transparent")
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.UNPACK_welcome_text()
        self.UNPACK_login_field()
        self.UNPACK_password_field()
        self.UNPACK_login_button()
        self.UNPACK_register_page_button()
        
        
    def login_action(self):
        login, password = self.login_field.get(), self.password_field.get()
        self.client_socket.login_request(login, password)
        request_answer = self.client_socket.wait_for_request_answer('login')
        if request_answer['status'] == 1101:
            self.client_socket.client_account.id = request_answer['id']
            self.client_socket.client_account.login = login
            print(self.client_socket.client_account)
            self.message_board_page_action()
        elif request_answer['status'] == 1001:
            self.wrong_password_error()
        elif request_answer['status'] == 1002:
            self.wrong_login_error()
        else:
            pass
            
            
    def register_page_action(self):
        self.frame.destroy()
        self.window.open_page("register")
        
    def message_board_page_action(self):
        self.frame.destroy()
        self.window.open_page("message_board") 
    
    def reset_errors_changes(self):
        self.login_field.configure(fg_color=ctk.ThemeManager.theme["CTkEntry"]["fg_color"])
        self.password_field.configure(fg_color=ctk.ThemeManager.theme["CTkEntry"]["fg_color"])
        self.welcome_text.configure(text="Добрый день!")
        
    def wrong_password_error(self):
        #self.login_field.configure(fg_color=None, hover_color=None)
        self.reset_errors_changes()
        self.password_field.configure(fg_color='#a51f1f')
        self.welcome_text.configure(text="Неверный пароль!")
        
    def wrong_login_error(self):
        self.reset_errors_changes()
        self.login_field.configure(fg_color='#a51f1f')
        self.welcome_text.configure(text="Аккаунта с таким логином не существует!")
    
    # --- UI элементы на странице: ---
    def UNPACK_welcome_text(self):
        self.welcome_text = ctk.CTkLabel(
            self.frame, 
            text="Добрый день!", 
            font=("Arial", 24, "bold"))
        self.welcome_text.pack(pady=(0, 20))
        
    def UNPACK_login_field(self):
        self.login_field = ctk.CTkEntry(
            self.frame,
            placeholder_text="Ваш логин",
            width=300,
            height=40)
        self.login_field.pack(pady=10)
    
    def UNPACK_password_field(self):
        self.password_field = ctk.CTkEntry(
            self.frame,
            placeholder_text="Ваш пароль",
            show="•",
            width=300,
            height=40)
        self.password_field.pack(pady=10)
    
    def UNPACK_login_button(self):
        self.login_button = ctk.CTkButton(
            self.frame,
            text="Войти",
            command=lambda: self.login_action(),
            width=300,
            height=40
        )
        self.login_button.pack(pady=20)
        
    def UNPACK_register_page_button(self):
        self.register_button = ctk.CTkButton(
            self.frame,
            text="Создать аккаунт",
            command=lambda: self.register_page_action(),
            width=300,
            height=40
        )
        self.register_button.pack(pady=20)

        