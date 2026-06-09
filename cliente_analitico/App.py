import socket
from proto import mensagens_pb2

GATEWAY_HOST = "127.0.0.1"
GATEWAY_PORT = 6000

#conectar ao gateway
def conectar():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cs.connect((GATEWAY_HOST, GATEWAY_PORT))
        return cs
    except ConnectionRefusedError:
        print("Erro: Gateway não está rodando.")
        return None

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

          

def menu():

    while True:

        print("\n===== CLIENTE ANALÍTICO =====")
        print("--- Sensores Climáticos ---")
        print("1 - Listar sensores climáticos")
        print("2 - Ver leituras climáticas")
        print("--- Semáforos ---")
        print("3 - Listar semáforos")
        print("4 - Ver leituras de semáforos")
        print("--- Postes ---")
        print("5 - Listar postes")
        print("6 - Ver leituras de postes")
        print("--- Câmeras ---")
        print("7 - Listar câmeras")
        print("8 - Ver leituras de câmeras")
        print("9 - Sair")


        opcao = input("Escolha: ")

        if opcao == "9":
            break

        req = mensagens_pb2.RequisicaoCliente()

        if opcao == "1":
            req.tipo = "listar_sensores"

        elif opcao == "2":
            req.tipo = "leituras"

        elif opcao == "3":
            req.tipo = "listar_semaforos"

        elif opcao == "4":
            req.tipo = "leituras_semaforos"

        elif opcao == "5":
            req.tipo = "listar_postes"

        elif opcao == "6":
            req.tipo = "leituras_postes"

        elif opcao == "7":
            req.tipo = "listar_cameras"

        elif opcao == "8":
            req.tipo = "leituras_cameras"

        else:
            print("Opção inválida")
            continue

        client = conectar()
        if client is None:
            continue

        print("Conectado")

        enviar(client, req)

        print("Enviado")

        resposta = receber(client)

        print("Recebido")

        client.close()

        print(f"\nStatus: {resposta.status}")
        print(f"Mensagem: {resposta.mensagem}\n")

        if not resposta.status:
            print("Erro na resposta do servidor")
            continue

        if opcao in ("1", "3", "5", "7"):
            # Listar dispositivos
            if resposta.sensores:
                for sensor in resposta.sensores:
                    print(
                        f"{sensor.sensor_id} | "
                        f"{sensor.tipo} | "
                        f"{sensor.status}"
                    )
            else:
                print("Nenhum dispositivo encontrado")

        elif opcao == "2":
            # Leituras climáticas
            if resposta.leituras:
                for leitura in resposta.leituras:
                    print(
                        f"\nSensor: {leitura.sensor_id}\n"
                        f"Temperatura: {leitura.temperatura}\n"
                        f"Sensação Térmica: {leitura.sensacao_termica}\n"
                        f"Temperatura Mínima: {leitura.temperatura_min}\n"
                        f"Temperatura Máxima: {leitura.temperatura_max}\n"
                        f"Pressão: {leitura.pressao}\n"
                        f"Umidade: {leitura.umidade}\n"
                    )
            else:
                print("Nenhuma leitura encontrada")

        elif opcao in ("4", "6", "8"):
            # Leituras de semáforos, postes e câmeras
            if opcao == "4":
                # Semáforos
                if resposta.leituras_semaforos:
                    for leitura in resposta.leituras_semaforos:
                        print(
                            f"\nSemáforo: {leitura.semaforo_id}\n"
                            f"Estado: {leitura.estado}\n"
                        )
                else:
                    print("Nenhuma leitura de semáforo encontrada")
            
            elif opcao == "6":
                # Postes
                if resposta.leituras_postes:
                    for leitura in resposta.leituras_postes:
                        print(
                            f"\nPoste: {leitura.poste_id}\n"
                            f"Estado: {leitura.estado}\n"
                        )
                else:
                    print("Nenhuma leitura de poste encontrada")
            
            elif opcao == "8":
                # Câmeras
                if resposta.leituras_cameras:
                    for leitura in resposta.leituras_cameras:
                        print(
                            f"\nCâmera: {leitura.camera_id}\n"
                            f"Período: {leitura.periodo_do_dia}\n"
                            f"Veículos: {leitura.veiculos}\n"
                            f"Pedestres: {leitura.pedestres}\n"
                            f"Densidade: {leitura.densidade_trafego}\n"
                        )
                else:
                    print("Nenhuma leitura de câmera encontrada")
            


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