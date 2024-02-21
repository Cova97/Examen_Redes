import socket
import threading

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.client_lock = threading.Lock()
        self.clients = {}

    def add_client(self, conn, add):
        try:
            with self.client_lock:
                self.clients[add] = conn
                print(f"Conectado a {add}")
        except Exception as e:
            print(str(e))

    def remove_client(self, add):
        try:
            with self.client_lock:
                del self.clients[add]
                print(f"Desconectado de {add}")
        except Exception as e:
            print(str(e))

    def broadcast(self, sender_add, data):
        try:
            with self.client_lock:
                for client_add, client_conn in self.clients.items():
                    if client_add != sender_add:
                        client_conn.send(data.encode())
        except Exception as e:
            print(str(e))

    def send_to_client(self, sender_add, recipient_add, data):
        try:
            with self.client_lock:
                if recipient_add in self.clients:
                    self.clients[recipient_add].send(data.encode())
                else:
                    print(f"El cliente {recipient_add} no está conectado.")
        except Exception as e:
            print(str(e))

    def handle_client(self, conn, add):
        try:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                print(f"Cliente {add}: {data}")

                if data.startswith("@"):
                    # Mensaje privado: @destinatario mensaje
                    recipient, private_msg = data.split(" ", 1)
                    recipient_add = recipient[1:]
                    self.send_to_client(add, recipient_add, private_msg)
                else:
                    # Mensaje público
                    self.broadcast(add, data)
        except Exception as e:
            print(str(e))
        finally:
            self.remove_client(add)
            conn.close()

    def start(self):
        try:
            ip = ''
            port = 1234
            self.server.bind((ip, port))
            self.server.listen(1)
            print('Esperando una conexión...')
            while True:
                conn, add = self.server.accept()
                self.add_client(conn, add)
                threading.Thread(target=self.handle_client, args=(conn, add)).start()
        except KeyboardInterrupt:
            print("Servidor desconectado")
        except Exception as e:
            print(str(e))
        finally:
            self.server.close()

if __name__ == '__main__':
    server = Server()
    server.start()
