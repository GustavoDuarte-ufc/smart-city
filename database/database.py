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
        
    def get_sensor_readings(self):

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
        
            
    def close(self):
        """Fecha a conexão de forma limpa."""
        if self._connection:
            self._connection.close()
            print("Conexão com o banco de dados fechada.")