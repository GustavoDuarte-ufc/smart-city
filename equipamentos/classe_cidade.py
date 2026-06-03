from equipamentos_poo import *

class CidadeInteligente:
    def __init__(self):
        self.sensores = [SensorClimatico() for _ in range(5)]
        self.postes = [PosteDeLuz(f"poste_{i}") for i in range(10)]
        self.semaforos = [Semaforo(f"semaforo_{i}") for i in range(3)]
        self.cameras = [CameraMonitoramento(f"camera_{i}") for i in range(2)]

    def simular_ciclo(self, tempo_passo_segundos):
        """Roda um ciclo de simulação, atualizando e coletando dados de todos os objetos"""
        print(f"\n--- Coletando dados da cidade (Passo: {tempo_passo_segundos}s) ---")
        
        print("\n[Clima]")
        for sensor in self.sensores:
            print(sensor.ler_dados())
            
        print("\n[Trânsito]")
        for semaforo in self.semaforos:
            estado_atual = semaforo.atualizar(tempo_passo_segundos)
            print(f"Semáforo {semaforo.id}: {estado_atual}")
            
        print("\n[Câmeras]")
        for camera in self.cameras:
            print(camera.capturar_fluxo())

# Executando a simulação
if __name__ == "__main__":
    minha_cidade = CidadeInteligente()
    # Simula a passagem de 65 segundos
    minha_cidade.simular_ciclo(65)