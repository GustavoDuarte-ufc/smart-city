import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

mensagem = "TEMP03,31.5, 65"

sock.sendto(
    mensagem.encode(),
    ("127.0.0.1", 5001)
)

print("Mensagem enviada")

