import random
import datetime

class SensorClimatico:

    contador = 1

    def __init__(self, sensor_id=None):
        if sensor_id is None:
            self.id = f"Sensor-{SensorClimatico.contador}"
            SensorClimatico.contador += 1
        else:
            self.id = f"Sensor-{sensor_id}"
        self.dados_atuais = {}

    def ler_dados(self):
        """Gera e atualiza os dados de temperatura do sensor"""
        temperatura = round(random.uniform(25.0, 32.0), 2)
        
        # Lógica de variação e limites
        temp_min = round(temperatura - random.uniform(1.0, 3.0), 2)
        temp_max = round(temperatura + random.uniform(0.5, 2.0), 2)
        
        if temp_min > temperatura:
            temp_min = temperatura - random.uniform(0.5, 1.5)
        if temp_max < temperatura:
            temp_max = temperatura + random.uniform(0.5, 1.5)

        self.dados_atuais = {
            'id': self.id,
            'temperatura': temperatura,
            'sensacao_termica': round(temperatura + random.uniform(2.0, 5.0), 2),
            'temperatura_min': round(temp_min, 2),
            'temperatura_max': round(temp_max, 2),
            'pressao': random.randint(1005, 1020),
            'umidade': random.randint(60, 95)
        }
        return self.dados_atuais


class PosteDeLuz:
    def __init__(self, poste_id):
        self.id = poste_id
        # 99% de chance de começar desligado
        self.estado = random.choices(['on', 'off'], weights=[0.01, 0.99], k=1)[0]

    def alternar_estado(self):
        self.estado = 'off' if self.estado == 'on' else 'on'
        return self.estado


class Semaforo:
    def __init__(self, semaforo_id):
        self.id = semaforo_id
        self.estado = random.choice(['red', 'yellow', 'green'])
        self.tempo_no_estado = 0

    def atualizar(self, tempo_decorrido):
        """Atualiza o estado do semáforo com base no tempo (em segundos)"""
        self.tempo_no_estado += tempo_decorrido
        
        # Corrigido o pequeno erro de digitação de 'grenn' para 'green'
        if self.estado == 'green' and self.tempo_no_estado > 60:
            self.estado = 'yellow'
            self.tempo_no_estado = 0
        elif self.estado == 'yellow' and self.tempo_no_estado > 5: # Amarelo dura menos tempo
            self.estado = 'red'
            self.tempo_no_estado = 0
        elif self.estado == 'red' and self.tempo_no_estado > 60:
            self.estado = 'green'
            self.tempo_no_estado = 0
            
        return self.estado


class CameraMonitoramento:
    def __init__(self, camera_id):
        self.id = camera_id

    def capturar_fluxo(self):
        """Simula os dados de tráfego baseados no horário atual"""
        now = datetime.datetime.now()
        periodo_do_dia = "noite" if 18 <= now.hour or now.hour < 6 else "dia"

        if periodo_do_dia == "dia":
            veiculos = random.randint(50, 500)
            pedestres = random.randint(20, 200)
        else:
            veiculos = random.randint(10, 150)
            pedestres = random.randint(5, 50)

        densidade = random.choices(['baixa', 'media', 'alta'], weights=[0.4, 0.4, 0.2], k=1)[0]

        return {
            'camera_id': self.id,
            'timestamp': now.isoformat(),
            'periodo_do_dia': periodo_do_dia,
            'veiculos': veiculos,
            'pedestres': pedestres,
            'densidade_trafego': densidade
        }