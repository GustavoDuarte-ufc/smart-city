import socket
import time
from equipamentos.equipamentos_poo import *

class CidadeInteligente:
    def __init__(self):

        self.sensores = [SensorClimatico() for _ in range(5)]
        self.postes = [PosteDeLuz(f"poste_{i}") for i in range(10)]
        self.semaforos = [Semaforo(f"semaforo_{i}") for i in range(3)]
        self.cameras = [CameraMonitoramento(f"camera_{i}") for i in range(2)]

        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

    def simular_ciclo(self, tempo_passo_segundos):
        """Roda um ciclo de simulação, atualizando e coletando dados de todos os objetos"""
        print(f"\n--- Coletando dados da cidade (Passo: {tempo_passo_segundos}s) ---")
        
        print("\n[Clima]")
        for sensor in self.sensores:

            dados = sensor.ler_dados()

            mensagem = (
                f"{dados['id']},"
                f"{dados['temperatura']},"
                f"{dados['sensacao_termica']},"
                f"{dados['temperatura_min']},"
                f"{dados['temperatura_max']},"
                f"{dados['pressao']},"
                f"{dados['umidade']}"
            )

            print(mensagem)

            self.sock.sendto(
                mensagem.encode(),
                ("127.0.0.1", 5001)
            )
            
        #print("\n[Trânsito]")
        #for semaforo in self.semaforos:
            #estado_atual = semaforo.atualizar(tempo_passo_segundos)
            # print(f"Semáforo {semaforo.id}: {estado_atual}")
            
        #print("\n[Câmeras]")
        #for camera in self.cameras:
            # print(camera.capturar_fluxo())
