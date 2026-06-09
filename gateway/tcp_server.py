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
                print("-> Listando sensores climáticos")
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
                print("-> Buscando leituras de sensores")
                print("Recebida requisição de leituras")
                readings = db.get_sensor_reading()
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
            
            elif request.tipo == "listar_semaforos":
                print("-> Listando semáforos")
                try:
                    semaforos = db.get_semaforos()
                    response = mensagens_pb2.RespostaGateway()

                    if semaforos:
                        for semaforo in semaforos:
                            sensor_info = response.sensores.add()
                            sensor_info.sensor_id = semaforo[1]
                            sensor_info.tipo = "semaforo"
                            sensor_info.ip = semaforo[2]
                            sensor_info.porta = semaforo[3]
                            sensor_info.status = semaforo[4]
                    
                    response.status = True
                    response.mensagem = f"Lista de semáforos ({len(semaforos)} encontrados)" if semaforos else "Nenhum semáforo registrado"

                    dados = response.SerializeToString()
                    tamanho = len(dados).to_bytes(4, "big")
                    client.sendall(tamanho + dados)
                except Exception as e:
                    print(f"Erro ao listar semáforos: {e}")
                    response = mensagens_pb2.RespostaGateway()
                    response.status = False
                    response.mensagem = f"Erro ao listar semáforos: {str(e)}"
                    dados = response.SerializeToString()
                    tamanho = len(dados).to_bytes(4, "big")
                    client.sendall(tamanho + dados)

            elif request.tipo == "listar_postes":
                print("-> Listando postes")
                try:
                    postes = db.get_postes()
                    response = mensagens_pb2.RespostaGateway()

                    if postes:
                        for poste in postes:
                            sensor_info = response.sensores.add()
                            sensor_info.sensor_id = poste[1]
                            sensor_info.tipo = "poste"
                            sensor_info.ip = poste[2]
                            sensor_info.porta = poste[3]
                            sensor_info.status = poste[4]
                    
                    response.status = True
                    response.mensagem = f"Lista de postes ({len(postes)} encontrados)" if postes else "Nenhum poste registrado"

                    dados = response.SerializeToString()
                    tamanho = len(dados).to_bytes(4, "big")
                    client.sendall(tamanho + dados)
                except Exception as e:
                    print(f"Erro ao listar postes: {e}")
                    response = mensagens_pb2.RespostaGateway()
                    response.status = False
                    response.mensagem = f"Erro ao listar postes: {str(e)}"
                    dados = response.SerializeToString()
                    tamanho = len(dados).to_bytes(4, "big")
                    client.sendall(tamanho + dados)

            elif request.tipo == "listar_cameras":
                print("-> Listando câmeras")
                try:
                    cameras = db.get_cameras()
                    response = mensagens_pb2.RespostaGateway()

                    if cameras:
                        for camera in cameras:
                            sensor_info = response.sensores.add()
                            sensor_info.sensor_id = camera[1]
                            sensor_info.tipo = "camera"
                            sensor_info.ip = camera[2]
                            sensor_info.porta = camera[3]
                            sensor_info.status = camera[4]
                    
                    response.status = True
                    response.mensagem = f"Lista de câmeras ({len(cameras)} encontradas)" if cameras else "Nenhuma câmera registrada"

                    dados = response.SerializeToString()
                    tamanho = len(dados).to_bytes(4, "big")
                    client.sendall(tamanho + dados)
                except Exception as e:
                    print(f"Erro ao listar câmeras: {e}")
                    response = mensagens_pb2.RespostaGateway()
                    response.status = False
                    response.mensagem = f"Erro ao listar câmeras: {str(e)}"
                    dados = response.SerializeToString()
                    tamanho = len(dados).to_bytes(4, "big")
                    client.sendall(tamanho + dados)

            elif request.tipo == "leituras_semaforos":
                print("-> Buscando leituras de semáforos")
                try:
                    readings = db.get_semaforo_readings()
                    response = mensagens_pb2.RespostaGateway()

                    if readings:
                        for reading in readings:
                            leitura = response.leituras_semaforos.add()
                            leitura.semaforo_id = reading[1]
                            leitura.estado = reading[2]
                    
                    response.status = True
                    response.mensagem = f"Leituras de semáforos ({len(readings)} encontradas)" if readings else "Nenhuma leitura de semáforo"

                    dados = response.SerializeToString()
                    tamanho = len(dados).to_bytes(4, "big")
                    client.sendall(tamanho + dados)
                except Exception as e:
                    print(f"Erro ao buscar leituras de semáforos: {e}")
                    response = mensagens_pb2.RespostaGateway()
                    response.status = False
                    response.mensagem = f"Erro ao buscar leituras: {str(e)}"
                    dados = response.SerializeToString()
                    tamanho = len(dados).to_bytes(4, "big")
                    client.sendall(tamanho + dados)

            elif request.tipo == "leituras_postes":
                print("-> Buscando leituras de postes")
                try:
                    readings = db.get_poste_readings()
                    response = mensagens_pb2.RespostaGateway()

                    if readings:
                        for reading in readings:
                            leitura = response.leituras_postes.add()
                            leitura.poste_id = reading[1]
                            leitura.estado = reading[2]
                    
                    response.status = True
                    response.mensagem = f"Leituras de postes ({len(readings)} encontradas)" if readings else "Nenhuma leitura de poste"

                    dados = response.SerializeToString()
                    tamanho = len(dados).to_bytes(4, "big")
                    client.sendall(tamanho + dados)
                except Exception as e:
                    print(f"Erro ao buscar leituras de postes: {e}")
                    response = mensagens_pb2.RespostaGateway()
                    response.status = False
                    response.mensagem = f"Erro ao buscar leituras: {str(e)}"
                    dados = response.SerializeToString()
                    tamanho = len(dados).to_bytes(4, "big")
                    client.sendall(tamanho + dados)

            elif request.tipo == "leituras_cameras":
                print("-> Buscando leituras de câmeras")
                try:
                    readings = db.get_camera_readings()
                    response = mensagens_pb2.RespostaGateway()

                    if readings:
                        for reading in readings:
                            leitura = response.leituras_cameras.add()
                            leitura.camera_id = reading[1]
                            leitura.periodo_do_dia = reading[2]
                            leitura.veiculos = reading[3]
                            leitura.pedestres = reading[4]
                            leitura.densidade_trafego = reading[5]
                    
                    response.status = True
                    response.mensagem = f"Leituras de câmeras ({len(readings)} encontradas)" if readings else "Nenhuma leitura de câmera"

                    dados = response.SerializeToString()
                    tamanho = len(dados).to_bytes(4, "big")
                    client.sendall(tamanho + dados)
                except Exception as e:
                    print(f"Erro ao buscar leituras de câmeras: {e}")
                    response = mensagens_pb2.RespostaGateway()
                    response.status = False
                    response.mensagem = f"Erro ao buscar leituras: {str(e)}"
                    dados = response.SerializeToString()
                    tamanho = len(dados).to_bytes(4, "big")
                    client.sendall(tamanho + dados)
            
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