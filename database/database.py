import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db_name="gateway.db"):
        """Inicializa a classe e configura a conexão."""
        self.db_name = db_name
        # O atributo que guarda a conexão começa como None
        self._connection = None 

        # Chama o método (com nome diferente do atributo)
        self.connect()
        self.create_tables()

    def connect(self):
        """Abre uma conexão com o banco de dados SQLite"""
        try:
            self._connection = sqlite3.connect(self.db_name)
            print(f"Conexão com o banco '{self.db_name}' estabelecida com sucesso.")
            return self._connection
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None
    
    def create_tables(self):
        """Cria as tabelas necessárias para o gateway"""
        if self._connection is None:
            print("Erro: Sem conexão ativa para criar tabelas.")
            return
        
        # Ajustado: Adicionado ID auto-incremental para permitir várias leituras do mesmo sensor
        sql_table_sensors = """
        CREATE TABLE IF NOT EXISTS sensors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT NOT NULL UNIQUE,
            sensor_type TEXT NOT NULL,
            ip TEXT NOT NULL,
            port INTEGER NOT NULL,
            status TEXT NOT NULL,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        sql_table_readings = """
        CREATE TABLE IF NOT EXISTS sensors_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT NOT NULL,
            temperatura REAL NOT NULL,
            sensacao_termica REAL NOT NULL,
            temperatura_min REAL NOT NULL,
            temperatura_max REAL NOT NULL,
            pressao REAL NOT NULL,
            umidade REAL NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        sql_table_camera = """
        CREATE TABLE IF NOT EXISTS camera (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cam_id TEXT NOT NULL,
            ip TEXT NOT NULL,
            port INTEGER NOT NULL,
            status TEXT NOT NULL,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );
        """

        sql_camera_readings = """
        CREATE TABLE IF NOT EXISTS camera_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cam_id TEXT NOT NULL
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            periodo_do_dia TEXT NOT NULL,
            veiculos INTEGER NOT NULL,
            pedestres INTEGER NOT NULL,
            densidade_trafego TEXT NOT NULL
        );
        """

        sql_table_poste = """
        CREATE TABLE IF NOT EXISTS poste (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            poste_id TEXT NOT NULL,
            ip TEXT NOT NULL,
            port INTEGER NOT NULL,
            status TEXT NOT NULL,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );
        """

        sql_poste_readings = """
        CREATE TABLE IF NOT EXISTS poste_readings (
            poste_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            estado TEXT NOT NULL,
        );
        """

        sql_table_semaforo = """
        CREATE TABLE IF NOT EXISTS semaforo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            semaforo_id TEXT NOT NULL,
            ip TEXT NOT NULL,
            port INTEGER NOT NULL,
            status TEXT NOT NULL,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );
        """

        sql_semaforo_readings = """
        CREATE TABLE IF NOT EXISTS semaforod_readings (
            semaforo_id TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            estado TEXT NOT NULL
        );
        """

        try:
            cursor = self._connection.cursor()
            cursor.execute(sql_table_sensors)
            cursor.execute(sql_table_readings)
            self._connection.commit()
            print("Tabela inicializada com sucesso.")
        except Error as e:
            print(f"Erro ao criar tabelas: {e}")

    def save_sensor(self, sensor_id, sensor_type, ip, port, status):
        """Salva uma nova leitura de sensor no banco de dados."""
        sql = """
        INSERT INTO sensors (sensor_id, sensor_type, ip, port, status)
        VALUES (?, ?, ?, ?, ?);
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute(sql, (sensor_id, sensor_type, ip, port, status))
            self._connection.commit()
            print(f"Leitura do sensor {sensor_id} salva com sucesso.")
            return True
        except Error as e:
            print(f"Erro ao salvar leitura: {e}")
            return False

    def get_sensors(self):
        """Retorna todas as leituras registradas."""
        sql = "SELECT * FROM sensors ORDER BY last_seen DESC;"
        try:
            cursor = self._connection.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print(f"Erro ao buscar leituras: {e}")
            return []
        

    def save_sensor_reading(
        self,
        sensor_id,
        temperatura,
        sensacao_termica,
        temperatura_min,
        temperatura_max,
        pressao,
        umidade
    ):
        
        sql = """
        INSERT INTO sensors_readings (
            sensor_id,
            temperatura,
            sensacao_termica,
            temperatura_min,
            temperatura_max,
            pressao,
            umidade
        )
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """

        try:
            cursor = self._connection.cursor()

            cursor.execute(
                sql,
                (
                    sensor_id,
                    temperatura,
                    sensacao_termica,
                    temperatura_min,
                    temperatura_max,
                    pressao,
                    umidade
                )
            )

            self._connection.commit()

            return True

        except Error as e:
            print(f"Erro ao salvar leitura: {e}")
            return False
        
    def get_sensor_reading(self):

        sql = """
        SELECT *
        FROM sensors_readings
        ORDER BY timestamp DESC;
        """

        try:

            cursor = self._connection.cursor()

            cursor.execute(sql)

            return cursor.fetchall()

        except Error as e:

            print(f"Erro ao buscar leituras: {e}")

            return []

    def save_camera(self, cam_id, ip, port, status):
        """Salva uma nova leitura de sensor no banco de dados."""
        sql = """
        INSERT INTO cameras (cam_id, ip, port, status)
        VALUES (?, ?, ?, ?);
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute(sql, (cam_id, ip, port, status))
            self._connection.commit()
            print(f"Leitura da câmera {cam_id} salva com sucesso.")
            return True
        except Error as e:
            print(f"Erro ao salvar leitura: {e}")
            return False

    def get_cameras(self):
        """Retorna todas as leituras registradas."""
        sql = "SELECT * FROM cameras ORDER BY last_seen DESC;"
        try:
            cursor = self._connection.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print(f"Erro ao buscar leituras: {e}")
            return []
    
    def save_camera_readings(
            self,
            camera_id,
            timestamp,
            periodo_do_dia,
            veiculos,
            pedestres,
            densidade_trafego
                             ):
            
        sql = """
        INSERT INTO camera_readings (
            camera_id,
            timestamp,
            periodo_do_dia,
            veiculos,
            pedestres,
            densidade_trafego
        )
        VALUES (?, ?, ?, ?, ?, ?);
        """
        
        try:
            cursor = self._connection.cursor()

            cursor.execute(
                sql,
                (
                    camera_id,
                    timestamp,
                    periodo_do_dia,
                    veiculos,
                    pedestres,
                    densidade_trafego
                )
            )

            self._connection.commit()

            return True

        except Error as e:
            print(f"Erro ao salvar leitura: {e}")
            return False
        
    def get_camera_readings(self):

        sql = """
        SELECT *
        FROM camera_readings
        ORDER BY timestamp DESC;
        """

        try:

            cursor = self._connection.cursor()

            cursor.execute(sql)

            return cursor.fetchall()

        except Error as e:

            print(f"Erro ao buscar leituras: {e}")

    def save_poste(self, poste_id, ip, port, status):
        """Salva uma nova leitura de sensor no banco de dados."""
        sql = """
        INSERT INTO postes (poste_id, ip, port, status)
        VALUES (?, ?, ?, ?);
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute(sql, (poste_id, ip, port, status))
            self._connection.commit()
            print(f"Leitura do poste {poste_id} salva com sucesso.")
            return True
        except Error as e:
            print(f"Erro ao salvar leitura: {e}")
            return False

    def get_postes(self):
        """Retorna todas as leituras registradas."""
        sql = "SELECT * FROM postes ORDER BY last_seen DESC;"
        try:
            cursor = self._connection.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print(f"Erro ao buscar leituras: {e}")
            return []
    
    def save_poste_readings(
            self,
            poste_id,
            estado
        ):
            
        sql = """
        INSERT INTO poste_readings (
            poste_id,
            estado
        )
        VALUES (?, ?);
        """
        
        try:
            cursor = self._connection.cursor()

            cursor.execute(
                sql,
                (
                    poste_id,
                    estado
                )
            )

            self._connection.commit()

            return True

        except Error as e:
            print(f"Erro ao salvar leitura: {e}")
            return False
        
    def get_poste_readings(self):

        sql = """
        SELECT *
        FROM poste_readings
        ORDER BY timestamp DESC;
        """

        try:

            cursor = self._connection.cursor()

            cursor.execute(sql)

            return cursor.fetchall()

        except Error as e:

            print(f"Erro ao buscar leituras: {e}")

    def save_semaforo(self, semaforo_id, ip, port, status):
        """Salva uma nova leitura de sensor no banco de dados."""
        sql = """
        INSERT INTO semaforos (semaforo_id, ip, port, status)
        VALUES (?, ?, ?, ?);
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute(sql, (semaforo_id, ip, port, status))
            self._connection.commit()
            print(f"Leitura do semáforo {semaforo_id} salva com sucesso.")
            return True
        except Error as e:
            print(f"Erro ao salvar leitura: {e}")
            return False

    def get_semaforos(self):
        """Retorna todas as leituras registradas."""
        sql = "SELECT * FROM semaforos ORDER BY last_seen DESC;"
        try:
            cursor = self._connection.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print(f"Erro ao buscar leituras: {e}")
            return []
    
    def save_semaforo_readings(
            self,
            semaforo_id,
            estado
        ):
            
        sql = """
        INSERT INTO semaforo_readings (
            semaforo_id,
            estado
        )
        VALUES (?, ?);
        """
        
        try:
            cursor = self._connection.cursor()

            cursor.execute(
                sql,
                (
                    semaforo_id,
                    estado
                )
            )

            self._connection.commit()

            return True

        except Error as e:
            print(f"Erro ao salvar leitura: {e}")
            return False

    def get_semaforo_readings(self):

        sql = """
        SELECT *
        FROM semaforo_readings
        ORDER BY timestamp DESC;
        """

        try:

            cursor = self._connection.cursor()

            cursor.execute(sql)

            return cursor.fetchall()

        except Error as e:

            print(f"Erro ao buscar leituras: {e}")


    def close(self):
        """Fecha a conexão de forma limpa."""
        if self._connection:
            self._connection.close()
            print("Conexão com o banco de dados fechada.")
