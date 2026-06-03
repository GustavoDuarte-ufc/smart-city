import threading

from gateway.udp_receiver import start_udp_server
from gateway.tcp_server import start_tcp_server

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

try:

    while True:

        comando = input(
            "\nDigite 'sair' para encerrar o Gateway: "
        )

        if comando.lower() == "sair":
            stop_event.set()
            break

except KeyboardInterrupt:

    stop_event.set()

udp_thread.join()
tcp_thread.join()

print("Gateway encerrado.")