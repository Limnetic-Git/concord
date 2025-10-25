from server_socket import ServerSocket
from accounts_db import AccountsManager
from chat import ChatsManager

if __name__ == "__main__":
    accounts_manager = AccountsManager()
    chats_manager = ChatsManager()
    server_socket = ServerSocket(accounts_manager, chats_manager, '127.0.0.2', 1234)
