import socket

from database.database import Database
from gateway.sensor_manager import SensorManager


def start_udp_server(stop_event):

    manager = SensorManager()
    db = Database()

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    sock.bind(("127.0.0.1", 5001))

    # Timeout para verificar periodicamente o stop_event
    sock.settimeout(1)

    print("Servidor UDP iniciado")

    while not stop_event.is_set():

        try:

            data, addr = sock.recvfrom(1024)

            mensagem = data.decode()

            sensor_id, value1, value2 = mensagem.split(",")

            if not manager.sensor_exists(sensor_id):

                novo_sensor = {
                    "id": sensor_id,
                    "tipo": "temperatura",
                    "ip": addr[0],
                    "porta": addr[1],
                    "status": "online"
                }

                manager.register_sensor(novo_sensor)

                db.save_sensor(
                    sensor_id,
                    "temperatura",
                    addr[0],
                    addr[1],
                    "online"
                )

            db.save_reading(
                sensor_id,
                float(value1),
                float(value2)
            )

            print(f"Leitura recebida de {sensor_id}")

        except socket.timeout:
            pass

    sock.close()

    print("Servidor UDP encerrado")