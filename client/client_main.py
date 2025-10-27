from socket_modules.client_socket import ClientSocket
from pprint import pprint
from dataclasses import dataclass


client_socket = ClientSocket('127.0.0.1', 1234)

logged_in = False

my_login = None

def test_console_interface():
    global my_login, logged_in
    action = input('1) Войти; 2) Зарегистрироваться: ')
    if action == '1':
        login = input('Логин: ')
        password = input('Пароль: ')
        
        client_socket.login_request(login, password)
        request_answer = client_socket.wait_for_request_answer('login')
        if request_answer['status'] == 1101:
            logged_in = True
            my_login = login
        else:
            print('ОШИБКА!')
            test_console_interface()
            
    elif action == '2':
        login = input('Логин: ')
        password = input('Пароль: ')
        
        client_socket.registration_request(login, password)
        request_answer = client_socket.wait_for_request_answer('registration')
        if request_answer['status'] == 1100:
            logged_in = True
            my_login = login
        else:
            print('ОШИБКА!')
            test_console_interface()

test_console_interface()
if logged_in:
    action = input('1) Создать ЛС: ')
    if action == '1':
        friend_login = input('Введите логин друга: ')
        client_socket.create_private_chat_request('test', [my_login, friend_login])
        request_answer = client_socket.wait_for_request_answer('create_private_chat')
        print(request_answer)
    

