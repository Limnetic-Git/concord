import customtkinter as ctk

from ui_modules.login_page import LoginPage
from ui_modules.register_page import RegisterPage
from ui_modules.message_board_page import MessageBoardPage
from ui_modules.create_chat_page import CreateChatPage
from socket_modules.client_socket import ClientSocket


client_socket = ClientSocket('127.0.0.2', 1234)



class Window:
    def __init__(self):
      #  ctk.set_appearance_mode("dark")  # "light", "dark", "system"
        ctk.set_default_color_theme("themes/Oceanix.json")  # "blue", "green", "dark-blue"
        
        self.app = ctk.CTk()
        self.app.title("Lycord")
        self.app.geometry("800x500")
        self.app.eval('tk::PlaceWindow . center')

        self.pages = {
                     "login": LoginPage(),
                     "register": RegisterPage(),
                    # "message_board": MessageBoardPage(),
                    # "create_chat": CreateChatPage(),
                        }

        self.open_page("login")
        self.app.mainloop()
        
    def open_page(self, page):
        self.current_page = page
        self.pages[page].open_page(window=self, client_socket=client_socket)
    
if __name__ == "__main__":
    Window()
