import customtkinter as ctk

class RegisterPage:
    def open_page(self, window, client_socket):
        self.window = window
        self.client_socket = client_socket
        
        self.allowed_alphabet = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890_"
        
        self.frame = ctk.CTkFrame(self.window.app, fg_color="transparent")
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.UNPACK_welcome_text()
        self.UNPACK_login_field()
        self.UNPACK_password_field()
        self.UNPACK_second_password_field()
        self.UNPACK_create_account_button()
        self.UNPACK_back_button()
                 
    def back_action(self):
        self.frame.destroy()
        self.window.open_page("login")
        
    def message_board_page_action(self):
        self.frame.destroy()
        self.window.open_page("message_board") 
        
    def create_account_action(self):
        login, password, second_password = self.login_field.get(), self.password_field.get(), self.second_password_field.get()
        if password == second_password:
            if len(password) >= 8:
                if self.check_login_alphabet_rules(login):
                    self.client_socket.registration_request(login, password)
                    request_answer = self.client_socket.wait_for_request_answer('registration')
                    if request_answer['status'] == 1100:
                        self.client_socket.client_account.id = request_answer['id']
                        self.client_socket.client_account.login = login
                        print(self.client_socket.client_account)
                        self.message_board_page_action()
                    elif request_answer['status'] == 1000:
                        self.login_exists_error()
                    else:
                        print('ОШИБКА!')
                else:
                    self.bad_login_error()
            else:
                self.password_too_short_error()
        else:
            self.passwords_not_same_error()

    def reset_errors_changes(self):
        self.login_field.configure(fg_color=ctk.ThemeManager.theme["CTkEntry"]["fg_color"])
        self.password_field.configure(fg_color=ctk.ThemeManager.theme["CTkEntry"]["fg_color"])
        self.second_password_field.configure(fg_color=ctk.ThemeManager.theme["CTkEntry"]["fg_color"])
        self.welcome_text.configure(text="Рады знакомству!")
        
    def login_exists_error(self):
        self.reset_errors_changes()
        self.login_field.configure(fg_color='#a51f1f')
        self.welcome_text.configure(text="Аккаунт с таким логином уже существует!")
    
    def passwords_not_same_error(self):
        self.reset_errors_changes()
        self.password_field.configure(fg_color='#a51f1f')
        self.second_password_field.configure(fg_color='#a51f1f')
        self.welcome_text.configure(text="Пароли не совпадают!")
        
    def bad_login_error(self):
        self.reset_errors_changes()
        self.login_field.configure(fg_color='#a51f1f')
        self.welcome_text.configure(text='В логине допустимы только a-Z, 0-9 и "_"!')
    
    def password_too_short_error(self):
        self.reset_errors_changes()
        self.password_field.configure(fg_color='#a51f1f')
        self.second_password_field.configure(fg_color='#a51f1f')
        self.welcome_text.configure(text='Пароль должен быть минимум из 8 символов!')
        
    def check_login_alphabet_rules(self, login: str):
        """Проверяет, разрешён ли такой логин"""
        for letter in login:
            if not letter in self.allowed_alphabet:
                return False
        return True
    
    # --- UI элементы на странице: ---
    def UNPACK_welcome_text(self):
        self.welcome_text = ctk.CTkLabel(
            self.frame, 
            text="Рады знакомству!", 
            font=("Arial", 24, "bold")
        )
        self.welcome_text.pack(pady=(0, 20))
        
    def UNPACK_login_field(self):
        self.login_field = ctk.CTkEntry(
            self.frame,
            placeholder_text="Придумайте логин",
            width=300,
            height=40)
        self.login_field.pack(pady=10)
    
    def UNPACK_password_field(self):
        self.password_field = ctk.CTkEntry(
            self.frame,
            placeholder_text="Придумайте пароль",
            show="•",
            width=300,
            height=40)
        self.password_field.pack(pady=10)
        
    def UNPACK_second_password_field(self):
        self.second_password_field = ctk.CTkEntry(
            self.frame,
            placeholder_text="Подтвердите пароль",
            show="•",
            width=300,
            height=40)
        self.second_password_field.pack(pady=10)
        
    def UNPACK_create_account_button(self):
        self.create_account_button = ctk.CTkButton(
            self.frame,
            text="Создать аккаунт",
            command=lambda: self.create_account_action(),
            width=300,
            height=40
        )
        self.create_account_button.pack(pady=20)
    
    def UNPACK_back_button(self):
        self.back_button = ctk.CTkButton(
            self.frame,
            text="← Назад ко Входу",
            command=lambda: self.back_action(),
            width=300,
            height=40
        )
        self.back_button.pack(pady=20)