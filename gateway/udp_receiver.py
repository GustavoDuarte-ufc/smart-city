import socket

from database.database import Database
from gateway.sensor_manager import SensorManager


def handle_sensor_data(data, addr, manager, db):
    """Processa dados de sensores climáticos, semáforos, postes e câmeras"""
    try:
        mensagem = data.decode()
        parts = mensagem.split(",")
        
        # Verifica o tipo de dado baseado no número de partes
        if len(parts) == 7:
            # Dados de sensor climático
            (
                sensor_id,
                temperatura,
                sensacao_termica,
                temperatura_min,
                temperatura_max,
                pressao,
                umidade
            ) = parts

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
        
        elif len(parts) == 2:
            # Dados de semáforo ou poste (id,estado)
            device_id, estado = parts
            
            # Diferencia pelo prefixo do ID
            if device_id.startswith("semaforo_"):
                # Semáforo
                if not manager.sensor_exists(device_id):
                    novo_semaforo = {
                        "id": device_id,
                        "tipo": "semaforo",
                        "ip": addr[0],
                        "porta": addr[1],
                        "status": "online"
                    }
                    manager.register_sensor(novo_semaforo)
                    db.save_semaforo(
                        device_id,
                        addr[0],
                        addr[1],
                        "online"
                    )
                
                db.save_semaforo_readings(device_id, estado)
                print(f"Leitura de semáforo recebida de {device_id}: {estado}")
            
            elif device_id.startswith("poste_"):
                # Poste de luz
                if not manager.sensor_exists(device_id):
                    novo_poste = {
                        "id": device_id,
                        "tipo": "poste",
                        "ip": addr[0],
                        "porta": addr[1],
                        "status": "online"
                    }
                    manager.register_sensor(novo_poste)
                    db.save_poste(
                        device_id,
                        addr[0],
                        addr[1],
                        "online"
                    )
                
                db.save_poste_reading(device_id, estado)
                print(f"Leitura de poste recebida de {device_id}: {estado}")
        
        elif len(parts) == 5:
            # Dados de câmera (camera_id,periodo_do_dia,veiculos,pedestres,densidade_trafego)
            camera_id, periodo_do_dia, veiculos, pedestres, densidade_trafego = parts
            
            if not manager.sensor_exists(camera_id):
                nova_camera = {
                    "id": camera_id,
                    "tipo": "camera",
                    "ip": addr[0],
                    "porta": addr[1],
                    "status": "online"
                }
                manager.register_sensor(nova_camera)
                db.save_camera(
                    camera_id,
                    addr[0],
                    addr[1],
                    "online"
                )
            
            db.save_camera_reading(
                camera_id,
                periodo_do_dia,
                int(veiculos),
                int(pedestres),
                densidade_trafego
            )
            print(f"Leitura de câmera recebida de {camera_id}: {periodo_do_dia}")
    
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")


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
            handle_sensor_data(data, addr, manager, db)

        except socket.timeout:
            pass

        except Exception as e:
            print(f"Erro ao processar mensagem UDP: {e}")

    sock.close()

    print("Servidor UDP encerrado")