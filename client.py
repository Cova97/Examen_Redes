import socket
import threading

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = 1234

    def connect(self):
        try:
            self.client.connect((self.host, self.port))
            print(f"Conectado a {self.host}:{self.port}")
        except Exception as e:
            print(str(e))

    def send(self, data):
        try:
            self.client.send(data.encode())
        except Exception as e:
            print(str(e))

    def recv(self):
        try:
            while True:
                data = self.client.recv(1024).decode()
                print(f"Servidor: {data}")
        except Exception as e:
            print(str(e))

    def close(self):
        try:
            self.client.close()
        except Exception as e:
            print(str(e))

# Instanciamos un objeto de la clase Client
client = Client()
# Nos conectamos al servidor
client.connect()

# Creamos un hilo para recibir mensajes del servidor
recv_thread = threading.Thread(target=client.recv)
recv_thread.start()

# Ciclo para enviar mensajes al servidor
try:
    while True:
        message = input()
        if message.startswith("@"):
            # Mensaje privado: @destinatario mensaje
            client.send(message)
        else:
            # Mensaje público
            client.send(message)
except KeyboardInterrupt:
    client.close()
    recv_thread.join()
    print("Conexion cerrada")
finally:
    client.close()
    recv_thread.join()
    print("Conexion cerrada")
