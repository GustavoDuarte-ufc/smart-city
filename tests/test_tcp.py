import socket

while True:

    print("""
    1. Lista de Sensores
    2. Lista de Atualizações
    3. Sair
    """)

    mensagem = input("Digite a sua opção: ")

    if mensagem == "3":
        print("Teste TCP finalizado...")
        break

    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    client.connect(("127.0.0.1", 6000))

    client.send(
        mensagem.encode()
    )

    response = client.recv(4096)

    print(response.decode())

    client.close()