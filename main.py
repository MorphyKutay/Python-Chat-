import socket
import threading

HOST = '127.0.0.1' # ipconfig ifconfig
PORT = 9090


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

def brodcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            brodcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)


def receive():
    while True:
        client, adress = server.accept()
        print(f"Baglandi{str(adress)}!")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)

        print(f"Kullanicinin Takma Adi {nickname}")
        brodcast(f"{nickname} Sunucuya Baglandi Hos Geldin\n".encode('utf-8'))
        client.send("Sunucuya Baglandi".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("server Ayakta...")
receive()

