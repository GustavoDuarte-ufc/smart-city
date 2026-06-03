import random
import datetime

def generate_random_temp_data():
  """Gera dados de temperatura sintéticos, mas consistentes"""
  temperatura = round(random.uniform(25.0, 32.0), 2)

  temp_min = round(temperatura - random.uniform(1.0, 3.0), 2)
  temp_max = round(temperatura + random.uniform(0.5, 2.0), 2)

  if temp_min > temperatura:
      temp_min = temperatura - random.uniform(0.5, 1.5)
  if temp_max < temperatura:
      temp_max = temperatura + random.uniform(0.5, 1.5)
  
  temp_min = round(temp_min, 2)
  temp_max = round(temp_max, 2)

  sensacao_termica = round(temperatura + random.uniform(2.0, 5.0), 2)

  pressao = random.randint(1005, 1020)

  umidade = random.randint(60, 95)

  random_data = {
      'temperatura': temperatura,
      'sensacao termica': sensacao_termica,
      'temperatura min': temp_min,
      'temperatura max': temp_max,
      'pressao': pressao,
      'umidade': umidade
  }
  return random_data

def get_id():
  """Gera um id aleatório de 10 dígitoss"""
  return random.randint(10**(9), (10**10) - 1)

def get_sensor_data(ids):
  """Gera dados de temperatura e associa a um sensor único"""
  all_sensors = []
  for sensor_id in ids:
    temp_data = generate_random_temp_data()
    # Create a new dictionary with 'id' first
    ordered_sensor_data = {'id': sensor_id}
    ordered_sensor_data.update(temp_data) # Add all other keys from temp_data
    all_sensors.append(ordered_sensor_data)

  return all_sensors

def get_poste_data(qtd):
    """Gera estados de uma quantidade determinada de postes na cidade"""
    estados = ['on', 'off']
    num_estados = [1, 0]
    probabilidades = [0.01, 0.99]
    postes = ['poste ' + str(num) for num in range(qtd)]
    estado_poste = {}

    for poste in postes:
       estado_poste[poste] = estados[random.choices(num_estados, weights=probabilidades, k=1)[0]]
    
    return estado_poste

def set_semaforos(n):
    """Gera uma quantidade de semáforos com estados iniciais aleatórios"""
    estados_s = ['red', 'yellow', 'green']
    semaforos = ['semaforo ' + str(num) for num in range(n)]
    estado_semaforo = {}

    for i in range(len(semaforos)):
        estado_semaforo[semaforos[i]] = estados_s[random.randint(0, 2)]

    return estado_semaforo

def at_estado_semaforo(estado, tempo):
  """Atualiza o estado atual do semáforo com base no tempo 
  decorrido desde o último estado"""
  novo_estado = estado
  if estado == 'grenn' and tempo > 60:
    novo_estado = 'yellow'

  if estado == 'yellow':
    novo_estado = 'red'

  if estado == 'red' and tempo > 60:
    novo_estado = 'green'

  return novo_estado

def simulate_city_camera_data():
  """Simulates data that a city camera might capture."""
  now = datetime.datetime.now()
  hora_do_dia = now.strftime("%H:%M:%S")
  periodo_do_dia = "noite" if 18 <= now.hour or now.hour < 6 else "dia"

  # Simula a contagem de veículos (pode variar de acordo com o período)
  if periodo_do_dia == "dia":
    veiculos = random.randint(50, 500) # Mais veículos durante o dia
    pedestres = random.randint(20, 200) # Mais pedestres durante o dia
  else:
    veiculos = random.randint(10, 150) # Menos veículos à noite
    pedestres = random.randint(5, 50) # Menos pedestres à noite

  # Simula a densidade do tráfego
  densidade_trafego = random.choices(['baixa', 'media', 'alta'], weights=[0.4, 0.4, 0.2], k=1)[0]

  camera_data = {
      'timestamp': now.isoformat(),
      'hora_do_dia': hora_do_dia,
      'periodo_do_dia': periodo_do_dia,
      'veiculos_detectados': veiculos,
      'pedestres_detectados': pedestres,
      'densidade_trafego': densidade_trafego,
  }
  return camera_data