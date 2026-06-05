import socket
from proto import mensagens_pb2

GATEWAY_HOST = "127.0.0.1"
GATEWAY_PORT = 6000

#conectar ao gateway
def conectar():
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cs.connect((GATEWAY_HOST, GATEWAY_PORT))
    return cs

def enviar(socket, requisicao):
    dados = requisicao.SerializeToString()
    tamanho = len(dados).to_bytes(4, 'big')
    socket.sendall(tamanho + dados)

def receber(socket):

    tamanho = int.from_bytes(
        socket.recv(4),
        "big"
    )

    dados = b""

    while len(dados) < tamanho:

        parte = socket.recv(
            tamanho - len(dados)
        )

        if not parte:
            break

        dados += parte

    resposta = mensagens_pb2.RespostaGateway()

    resposta.ParseFromString(dados)

    return resposta

    
""" 
def menu():
    while True:
        print("1 - Listar Sensores")
        print("2 -  Ver leituras")
        print("3 - Enviar comando")
        print("4 - Sair")

        opcao = int(input("Digite a opção desejada: "))

        if opcao == 1:
            req = mensagens_pb2.RequisicaoCliente(tipo="listar_sensores")
        elif opcao == 2:
            mensagens_pb2.RequisicaoCliente(tipo="leituras")
        elif opcao == 3:
            sensor_id = 
        elif opcao == 4:
            break
        else:
            print("Opção inválida")

        sc = conectar()
        enviar(sc, req)
        resp = receber(sc)
        sc.close()





if __name__ == "__main__":
    menu()
"""

def menu():

    while True:

        print("\n===== CLIENTE ANALÍTICO =====")
        print("1 - Listar sensores")
        print("2 - Ver leituras")
        print("3 - Sair")

        opcao = input("Escolha: ")

        if opcao == "3":
            break

        req = mensagens_pb2.RequisicaoCliente()

        if opcao == "1":
            req.tipo = "listar_sensores"

        elif opcao == "2":
            req.tipo = "leituras"
            print("Enviando requisição de leituras...")

        else:
            print("Opção inválida")
            continue

        client = conectar()

        print("Conectado")

        enviar(client, req)

        print("Enviado")

        resposta = receber(client)

        print("Recebido")

        client.close()

        print(f"\nStatus: {resposta.status}")
        print(f"Mensagem: {resposta.mensagem}")

        if opcao == "1":

            for sensor in resposta.sensores:

                print(
                    f"{sensor.sensor_id} | "
                    f"{sensor.tipo} | "
                    f"{sensor.status}"
                )

        elif opcao == "2":
            for leitura in resposta.leituras:

                print(
                    f"\nSensor: {leitura.sensor_id}\n"
                    f"Temperatura: {leitura.temperatura}\n"
                    f"Sensação Térmica: {leitura.sensacao_termica}\n"
                    f"Temperatura Mínima: {leitura.temperatura_min}\n"
                    f"Temperatura Máxima: {leitura.temperatura_max}\n"
                    f"Pressão: {leitura.pressao}\n"
                    f"Umidade: {leitura.umidade}\n"
                    f"Timestamp: {leitura.timestamp}\n"
                )
            


if __name__ == "__main__":
    menu()

'''import socket
from proto import mensagens_pb2

HOST = "127.0.0.1"
PORT = 6000

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client.connect((HOST, PORT))

req = mensagens_pb2.RequisicaoCliente()
req.tipo = "listar_sensores"

dados = req.SerializeToString()

client.sendall(
    len(dados).to_bytes(4, "big") + dados
)

tamanho = int.from_bytes(
    client.recv(4),
    "big"
)

dados = client.recv(tamanho)

resp = mensagens_pb2.RespostaGateway()
resp.ParseFromString(dados)

print(resp)

client.close()'''