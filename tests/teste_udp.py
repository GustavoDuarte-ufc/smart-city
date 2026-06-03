import socket

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

while True:

    print("""
    ===== SENSOR UDP =====
    1. Enviar leitura
    2. Sair
    """)

    opcao = input("Escolha uma opção: ")

    if opcao == "2":
        print("Teste UDP finalizado...")
        break

    elif opcao == "1":

        sensor_id = input("Sensor ID: ")

        temperatura = float(
            input("Temperatura: ")
        )

        umidade = float(
            input("Umidade: ")
        )

        mensagem = (
            f"{sensor_id},"
            f"{temperatura},"
            f"{umidade}"
        )

        sock.sendto(
            mensagem.encode(),
            ("127.0.0.1", 5001)
        )

        print("Leitura enviada com sucesso.\n")

    else:
        print("Opção inválida.\n")

sock.close()