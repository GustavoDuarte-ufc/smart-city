import socket
from proto import mensagens_pb2
from database.database import Database
import traceback

print(hasattr(mensagens_pb2, "RespostaGateway"))
print(hasattr(mensagens_pb2, "RequisicaoCliente"))

def start_tcp_server(stop_event):

    db = Database()

    HOST = "127.0.0.1"
    PORT = 6000

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind((HOST, PORT))

    server.listen()

    # Verifica periodicamente se deve encerrar
    server.settimeout(1)

    print("Servidor TCP iniciado")

    while not stop_event.is_set():

        try:
            client, addr = server.accept()
            tamanho = int.from_bytes(
                client.recv(4),
                "big"
            )

            dados = client.recv(tamanho)

            request = mensagens_pb2.RequisicaoCliente()
            request.ParseFromString(dados)

            print(f"Tipo recebido: [{request.tipo}]")

            if request.tipo == "listar_sensores":

                sensors = db.get_sensors()

                response = mensagens_pb2.RespostaGateway()

                for sensor in sensors:

                    sensor_info = response.sensores.add()
                    sensor_info.sensor_id = sensor[1]
                    sensor_info.tipo = sensor[2]
                    sensor_info.ip = sensor[3]
                    sensor_info.porta = sensor[4]
                    sensor_info.status = sensor[5]

                response.status = True
                response.mensagem = "Lista de sensores"

                dados = response.SerializeToString()

                tamanho = len(dados).to_bytes(
                    4,
                    "big"
                )

                client.sendall(
                    tamanho + dados
                )

            elif request.tipo == "leituras":
                print("Recebida requisição de leituras")
                readings = db.get_sensor_readings()
                print(f"{len(readings)} leituras encontradas")
                response = mensagens_pb2.RespostaGateway()

                for reading in readings:

                    print(reading)

                    leitura = response.leituras.add()

                    leitura.sensor_id = reading[1]
                    leitura.temperatura = reading[2]
                    leitura.sensacao_termica = reading[3]
                    leitura.temperatura_min = reading[4]
                    leitura.temperatura_max = reading[5]
                    leitura.pressao = reading[6]
                    leitura.umidade = reading[7]

                print("Resposta montada")

                response.status = True
                response.mensagem = "Leituras encontradas"

                dados = response.SerializeToString()

                tamanho = len(dados).to_bytes(
                    4,
                    "big"
                )

                client.sendall(
                    tamanho + dados
                )
            else:
                response = mensagens_pb2.RespostaGateway()
                response.status = False
                response.mensagem = "Comando inválido"
                dados = response.SerializeToString()

                tamanho = len(dados).to_bytes(
                    4,
                    "big"
                )

                client.sendall(
                    tamanho + dados
                )

            client.close()

        except socket.timeout:
            pass

        except Exception as e:
            print("\n===== ERRO TCP =====")
            traceback.print_exc()

    server.close()

    print("Servidor TCP encerrado")