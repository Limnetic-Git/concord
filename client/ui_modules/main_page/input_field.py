import customtkinter as ctk

class InputField:
    def __init__(self, main_page):
        self.main_page = main_page
    
    def create_input_field(self):
        """Создает поле ввода сообщения"""
        if not hasattr(self.main_page.message_area, 'message_area'):
            return
            
        # Очищаем старые элементы области ввода
        input_frame = self.main_page.message_area.message_area.grid_slaves(row=1, column=0)
        if input_frame:
            input_frame[0].destroy()
            
        self.input_frame = ctk.CTkFrame(
            self.main_page.message_area.message_area, height=100, corner_radius=10
        )
        self.input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
        self.input_frame.grid_propagate(False)
        
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
            print(f"Sending message to chat {self.main_page.current_chat_id}: {message_text}")
            
            self.main_page.client_socket.message_request(
                self.main_page.current_chat_id, 
                message_text, 
                self.main_page.client_socket.client_account.login
            )
            response = self.main_page.client_socket.wait_for_request_answer('message')
            
            if response:
                print("Message sent successfully")
                self.message_input.delete("1.0", "end")
            else:
                print("Failed to send message")