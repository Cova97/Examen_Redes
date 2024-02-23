import socket
import threading

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "172.18.59.198"
        self.port = 1234
        self.friends = {}  
        
    def connect(self):
        try:
            self.client.connect((self.host, self.port))
            print(f"Connected to {self.host}:{self.port}")
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
                print(f"Server: {data}")
        except Exception as e:
            print(str(e))

    def add_friend(self, identifier, name):
        self.friends[name] = identifier
        print(f"Added {name} as a friend")

    def remove_friend(self, identifier):
        if identifier in self.friends:
            removed_friend = self.friends.pop(identifier)
            print(f"Removed {removed_friend} from friends")
        else:
            print("Friend not found")

    def list_friends(self):
        if self.friends:
            print("Friends list:")
            for identifier, name in self.friends.items():
                print(f"{identifier}: {name}")
        else:
            print("You have no friends added")

    def close(self):
        try:
            self.client.close()
        except Exception as e:
            print(str(e))


if __name__ == '__main__':
    client = Client()
    client.connect()

    
    recv_thread = threading.Thread(target=client.recv)
    recv_thread.start()
    print(f"/addfriend: Añadir amigos \n /removefriend: Remover amigos\n/listfriends: Mostrar lista de amigos\n/connected: Verificar estado de amigo\n/history: Historial\n/id: Mensaje privado")
    try:
        while True:
            message = input("Enter message or command: ")
            if message.startswith("/addfriend"):
                _, identifier, name = message.split(" ", 2)
                client.add_friend(identifier, name)
            elif message.startswith("/removefriend"):
                _, identifier = message.split(" ", 1)
                client.remove_friend(identifier)
            elif message.startswith("/listfriends"):
                client.list_friends()
            elif message.startswith("/connected"):
                _, friend = message.split(" ", 1)
                id = client.friends[friend]
                client.send("/connected "+id)
            elif message.startswith("/history"):
                client.send(message)
            elif message.startswith("/"):
                recipient, private_msg = message.split(" ", 1)
                recipient = recipient[1:]
                id = client.friends[recipient]
                client.send("@"+id+" "+private_msg)
            else:
                
                client.send(message)
    except KeyboardInterrupt:
        print("Closing connection...")
    finally:
        client.close()
        recv_thread.join()
        print("Connection closed")
