import socket

from database.database import Database


def start_tcp_server():

    db = Database()

    HOST = "127.0.0.1"
    PORT = 6000

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.bind((HOST, PORT))

    server.listen()

    print("Servidor TCP iniciado")

    while True:

        client, addr = server.accept()

        request = client.recv(1024).decode()

        if request == "1":

            sensors = db.get_sensors()

            response = ""

            for sensor in sensors:
                response += f"{sensor[1]}\n"

            client.send(response.encode())

        elif request == "2":

            readings = db.get_readings()

            response = ""

            for reading in readings:

                response += (
                    f"Sensor: {reading[1]} | "
                    f"Valor1: {reading[2]} | "
                    f"Valor2: {reading[3]} | "
                    f"Data: {reading[4]}\n"
                )

            client.send(response.encode())

        else:

            client.send(
                "Comando inválido".encode()
            )

        client.close()