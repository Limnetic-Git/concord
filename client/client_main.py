from socket_modules.client_socket import ClientSocket
from pprint import pprint
from dataclasses import dataclass


client_socket = ClientSocket('127.0.0.2', 1234)

def test_console_interface():
    action = input('1) Войти; 2) Зарегистрироваться: ')
    if action == '1':
        login = input('Логин: ')
        password = input('Пароль: ')
        
        client_socket.login_request(login, password)
        request_answer = client_socket.wait_for_request_answer('login')
        print(request_answer['status'])

            
            
    elif action == '2':
        login = input('Логин: ')
        password = input('Пароль: ')
        
        client_socket.registration_request(login, password)
        request_answer = client_socket.wait_for_request_answer('registration')
        print(request_answer['status'])

test_console_interface()

