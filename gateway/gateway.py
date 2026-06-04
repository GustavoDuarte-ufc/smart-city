import threading
import time

from gateway.udp_receiver import start_udp_server
from gateway.tcp_server import start_tcp_server
from equipamentos.classe_cidade import CidadeInteligente

stop_event = threading.Event()

udp_thread = threading.Thread(
    target=start_udp_server,
    args=(stop_event,)
)

tcp_thread = threading.Thread(
    target=start_tcp_server,
    args=(stop_event,)
)

udp_thread.start()
tcp_thread.start()

minha_cidade = CidadeInteligente()

try:

    while True:
        minha_cidade.simular_ciclo(5)
        time.sleep(5)
        

except KeyboardInterrupt:

    stop_event.set()

udp_thread.join()
tcp_thread.join()


print("Gateway encerrado.")