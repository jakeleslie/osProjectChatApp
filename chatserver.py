import threading
import socket

# Data Needed for Conncection
host = '127.0.0.1'
port = 4444

#Start Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Initializes Lists for Clients and Usernames
clients = []
usernames = []

# Function to Send Messages to All Clients That Connect
def broadcast(message):
    for client in clients:
        client.send(message)


# Handles Messages Sent by Clients
def handle(client):
    while True:
        try:
            # Broadcasts
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing and Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f'{username} has left.'.encode('ascii'))
            usernames.remove(username)
            break


# Receives and Listens for Messages from Cients
def receive():
    while True:
        # Connects
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        #Receive Username
        client.send('NAME'.encode('ascii'))
        username = client.recv(1024).decode('ascii')

        # Ensures a Maximum of 20 Client Conncections
        if (len(usernames) > 19):
            print("Only 20 Connections Allowed")
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f'{username} has been disconnected.'.encode('ascii'))
            usernames.remove(username)
        else:
            # Stores New Clients in Lists
            usernames.append(username)
            clients.append(client)
        
        # Displays Username
        print("Username is {}".format(username))
        broadcast("{} has joined the chat!".format(username).encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        #Thread Hanling For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening...")
receive()