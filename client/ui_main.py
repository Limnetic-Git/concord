import customtkinter as ctk
from ui_modules.login_page import LoginPage
from ui_modules.register_page import RegisterPage
from ui_modules.main_page.main import MainMessengerPage
from ui_modules.create_chat_page import CreateChatPage
from socket_modules.client_socket import ClientSocket

client_socket = ClientSocket('127.0.0.2', 1234)#'89.110.90.193', 1234)

class Window:
    def __init__(self):
        #ctk.set_appearance_mode("system")  # "light", "dark", "system"
        theme_name = "Harlequin"
        ctk.set_default_color_theme(f"dark-blue")#themes/{theme_name}.json")  # "blue", "green", "dark-blue"
        
        self.app = ctk.CTk()
        self.app.title("Concord")
        self.app.geometry("900x600")
        self.app.eval('tk::PlaceWindow . center')

        self.pages = {
                     "login": LoginPage(),
                     "register": RegisterPage(),
                     "message_board": MainMessengerPage(),
                     "create_chat": CreateChatPage(),
                        }
        self.open_page("login")
        self.app.mainloop()
        
    def open_page(self, page):
        self.current_page = page
        self.pages[page].open_page(window=self, client_socket=client_socket)
    
if __name__ == "__main__":
    Window()
