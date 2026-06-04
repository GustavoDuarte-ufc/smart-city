import socket

from database.database import Database


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

            request = client.recv(1024).decode()

            if request == "1":

                sensors = db.get_sensors()

                response = ""

                for sensor in sensors:
                    response += f"{sensor[1]}\n"

                client.send(response.encode())

            elif request == "2":

                readings = db.get_sensor_readings()

                response = ""

                for reading in readings:

                    response += (
                        f"Sensor: {reading[1]}\n"
                        f"Temperatura: {reading[2]}\n"
                        f"Sensação: {reading[3]}\n"
                        f"Mínima: {reading[4]}\n"
                        f"Máxima: {reading[5]}\n"
                        f"Pressão: {reading[6]}\n"
                        f"Umidade: {reading[7]}\n"
                        f"Data: {reading[8]}\n\n"
                    )

                client.send(response.encode())

            else:

                client.send(
                    "Comando inválido".encode()
                )

            client.close()

        except socket.timeout:
            pass

        except Exception as e:
            print(f"Erro ao processar mensagem TCP: {e}")

    server.close()

    print("Servidor TCP encerrado")