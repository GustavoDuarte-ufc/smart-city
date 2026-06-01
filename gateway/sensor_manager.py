class SensorManager:
    """
    Representa o controle de sensores.
    
    Atributos:
        sensors -> Dicionário de sensores resgistrados
    
    Estrutura dos sensores:
      exemplo:
        sensor = {
            "id": "TEMP01",
            "tipo": "temperatura",
            "ip": "192.168.0.10",
            "porta": 5001,
            "status": "online",
            "last_seen": "2026-06-01 14:30:10",
            "frequency": 15
        }
    
    """

    def __init__(self):
        self.sensors = {}

    def register_sensor(self, sensor):
        self.sensors[sensor["id"]] = sensor

    def get_sensor(self, sensor_id):
        return self.sensors.get(sensor_id)
    
    def get_all_sensors(self):
        return self.sensors
    
    def update_status(self, sensor_id, status):
        if sensor_id in self.sensors:
            self.sensors[sensor_id]["status"] = status

    def sensor_exists(self, sensor_id):
        return sensor_id in self.sensors
    
    def remove_sensor(self, sensor_id):
        if sensor_id in self.sensors:
            del self.sensors[sensor_id]
