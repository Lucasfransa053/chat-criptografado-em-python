import socket
import threading
from cryptography.fernet import Fernet

# Gera a chave de criptografia simétrica
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Cria o socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

print('Servidor iniciado. Aguardando conexões...')

# Dicionário para armazenar todas as conexões de clientes
client_connections = {}

def handle_client(client_socket, name):
    while True:
        # Recebe a mensagem do cliente
        encrypted_msg = client_socket.recv(1024)
        if not encrypted_msg:
            break

        # Decriptografa a mensagem
        decrypted_msg = cipher_suite.decrypt(encrypted_msg)
        print(f'\nMensagem recebida de {name}: {decrypted_msg.decode()}')

        # Recriptografa a mensagem e envia para todos os outros clientes conectados
        for client_name, client in client_connections.items():
            if client_name != name:
                client.send(name.encode() + b': ' + encrypted_msg)

    client_socket.close()
    del client_connections[name]
    print(f'Cliente {name} desconectado')

while True:
    client_socket, addr = server_socket.accept()
    print(f'Cliente conectado: {addr}')

    # Envia a chave para o cliente
    client_socket.send(key)

    # Recebe o nome do cliente
    name = client_socket.recv(1024).decode()

    # Adiciona a nova conexão ao dicionário de conexões
    client_connections[name] = client_socket

    # Cria uma nova thread para lidar com a conexão do cliente
    thread = threading.Thread(target=handle_client, args=(client_socket, name))
    thread.start()
