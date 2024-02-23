import socket
import threading

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.client_lock = threading.Lock()
        self.clients = {}
    
    def is_client_connected(self, recipient_id):
        with self.client_lock:
            return recipient_id in self.clients

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


    def add_client(self, conn, addr):
        try:
            with self.client_lock:
                # Convert the address to a string representation or use a unique identifier
                client_id = str(addr[1])  # This is a simplified example; consider a more unique identifier
                self.clients[client_id] = conn
                print(f"Connected to {addr}")
                #self.broadcast(0000,f"{addr} connected")
        except Exception as e:
            print(str(e))

    def send_to_client(self, sender_id, recipient_id, data):
        try:
            with self.client_lock:
                if recipient_id in self.clients:
                    self.clients[recipient_id].send(data.encode())
                else:
                    print(f"The client {recipient_id} is not connected.")
        except Exception as e:
            
            print(str(e))


    def handle_client(self, conn, add):
        try:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                print(f"Cliente {add}: {data}")
                if data.startswith("/connected"):
                    _, friend = data.split(" ", 1)
                    if self.is_client_connected(friend):
                        conn.send(f"Client {friend} is connected.".encode())
                    else:
                        conn.send(f"Client {friend} is not connected.".encode())
                elif data.startswith("/history"):
                    history = self.recover_messages(add)
                    print(history)
                    conn.send(history.encode())
                elif data.startswith("@"):
                    # Mensaje privado: @destinatario mensaje
                    recipient, private_msg = data.split(" ", 1)
                    recipient_add = recipient[1:]
                    self.send_to_client(add, recipient_add, private_msg)
                else:
                    # Mensaje público
                    self.broadcast(add, data)
                self.save_messages(add, data)
        except Exception as e:
            print(str(e))
        finally:
            #self.broadcast(0000,f"{add} disconnected")
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

    # Funcion para guardar los mensajes de un usuario cuando se desconecta
    def save_messages(self, client_id, data):
        filename = f"messages_{client_id}.txt"
        try:
            with self.client_lock:
                with open(filename, "a") as file:
                    file.write(data + "\n")
        except Exception as e:
            print(str(e))

    def recover_messages(self, client_id):
        filename = f"messages_{client_id}.txt"
        try:
            with self.client_lock:
                with open(filename, "r") as file:
                    messages = file.read()
                return messages
        except FileNotFoundError:
            return "No message history found."
        except Exception as e:
            print(str(e))
            return "Error retrieving message history."

    # Funcion para imprimir los mensajes guardados de un usuario cuando se conecta
    def print_messages(self, add):
        try:
            with self.client_lock:
                messages = self.recover_messages(add)
                if messages:
                    print(f"Messages for {add}:")
                    print(messages)
                else:
                    print(f"No messages for {add}")
        except Exception as e:
            print(str(e))

if __name__ == '__main__':
    server = Server()
    server.start()
