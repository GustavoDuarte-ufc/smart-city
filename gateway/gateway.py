import threading

from gateway.udp_receiver import start_udp_server
from gateway.tcp_server import start_tcp_server


udp_thread = threading.Thread(
    target=start_udp_server
)

tcp_thread = threading.Thread(
    target=start_tcp_server
)

udp_thread.start()
tcp_thread.start()

udp_thread.join()
tcp_thread.join()