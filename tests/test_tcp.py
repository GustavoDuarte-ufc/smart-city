import socket

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client.connect(("127.0.0.1", 6000))

print(
    """ 
    1. Lista de Sensores 
    2. Lista de Atualizações   
    """)
mensagem = input("Digite a sua opção: ")

client.send(
    mensagem.encode()
)

response = client.recv(4096)

print(response.decode())

client.close()