import socket
import sys
sys.path.insert(0, '../proto')
import mensagens_pb2

GATEWAY_HOST = "127.0.0.1"
GATEWAY_PORT = 6000

#conectar ao gateway

def conectar():
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cs.connect((GATEWAY_HOST, GATEWAY_PORT))
    return cs

def enviar(socket, requisicao):
    dados = requisicao.SerializeToString()
    tamanho = len(dados).to_bytes(4, 'big')
    socket.sendall(tamanho + dados)

def receber(socket):
    tamanho = int.from_bytes(socket.recv(4), 'big')
    dados = socket.recv(tamanho)
    resposta = mensagens_pb2.RespostaGateway()
    resposta.ParseFromString(dados)
    return resposta

    
""" 
def menu():
    while True:
        print("1 - Listar Sensores")
        print("2 -  Ver leituras")
        print("3 - Enviar comando")
        print("4 - Sair")

        opcao = int(input("Digite a opção desejada: "))

        if opcao == 1:
            req = mensagens_pb2.RequisicaoCliente(tipo="listar_sensores")
        elif opcao == 2:
            mensagens_pb2.RequisicaoCliente(tipo="leituras")
        elif opcao == 3:
            sensor_id = 
        elif opcao == 4:
            break
        else:
            print("Opção inválida")

        sc = conectar()
        enviar(sc, req)
        resp = receber(sc)
        sc.close()





if __name__ == "__main__":
    menu()
"""