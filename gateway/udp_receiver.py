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

            (
                sensor_id,
                temperatura,
                sensacao_termica,
                temperatura_min,
                temperatura_max,
                pressao,
                umidade
            ) = mensagem.split(",")

            if not manager.sensor_exists(sensor_id):

                novo_sensor = {
                    "id": sensor_id,
                    "tipo": "climatico",
                    "ip": addr[0],
                    "porta": addr[1],
                    "status": "online"
                }

                manager.register_sensor(novo_sensor)

                db.save_sensor(
                    sensor_id,
                    "climatico",
                    addr[0],
                    addr[1],
                    "online"
                )

            db.save_sensor_reading(
                sensor_id,
                float(temperatura),
                float(sensacao_termica),
                float(temperatura_min),
                float(temperatura_max),
                int(pressao),
                int(umidade)
            )

            print(f"Leitura climática recebida de {sensor_id}")

        except socket.timeout:
            pass

        except Exception as e:
            print(f"Erro ao processar mensagem UDP: {e}")

    sock.close()

    print("Servidor UDP encerrado")