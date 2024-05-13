import socket
import threading
import time
from cryptography.fernet import Fernet

def receive_message(client_socket):
    while True:
        # Recebe a mensagem recriptografada do servidor
        encrypted_msg = client_socket.recv(1024)
        # Separa o nome do cliente da mensagem
        name, encrypted_msg = encrypted_msg.split(b': ', 1)
        # Decripta a mensagem
        decrypted_msg = cipher_suite.decrypt(encrypted_msg)
        print(f'\nMensagem de {name.decode()}: {decrypted_msg.decode()}')

# Cria o socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

# Recebe a chave do servidor
key = client_socket.recv(1024)
cipher_suite = Fernet(key)

# Envia o nome para o servidor
name = input('Digite seu nome: ')
client_socket.send(name.encode())

# Cria uma nova thread para receber mensagens do servidor
thread = threading.Thread(target=receive_message, args=(client_socket,))
thread.start()

while True:
    # Lê a mensagem do usuário
    msg = input('\nDigite uma mensagem (ou "sair" para desconectar): ')
    if msg == 'sair':
        break

    start_time = time.perf_counter()  # Inicia o cronômetro

    # Criptografa a mensagem e envia para o servidor
    encrypted_msg = cipher_suite.encrypt(msg.encode())
    client_socket.send(encrypted_msg)

    end_time = time.perf_counter()  # Para o cronômetro
    elapsed_time = end_time - start_time  # Calcula o tempo decorrido
    print(f'Tempo decorrido para enviar a mensagem: {elapsed_time:.12f} segundos')

client_socket.close()
