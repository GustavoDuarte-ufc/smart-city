import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sensor_id = input("Sensor id: ")
temperatura = float(input("Temperatura: "))
umidade = float(input("Umidade: "))

mensagem = f"{sensor_id},{temperatura},{umidade}"

sock.sendto(
    mensagem.encode(),
    ("127.0.0.1", 5001)
)

print("Mensagem enviada")

