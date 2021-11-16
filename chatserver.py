import threading, socket #Need to import this so that we can get the threading and sockets to work

#Get a host and a port so we can bind
host = socket.gethostname()
port = 4000

#create socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen() #queue up to 20 requests

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
            # Broadcasts message received from client
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing and Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f'{username} has left\n'.encode('ascii'))
            usernames.remove(username)
            break


# Receives and Listens for Messages from Cients
def receive():
    while True:
        # Wait for an incoming connection and accept it when it comes in, and then print that a client connected with a specific address
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        #Receive Username 
        client.send('NAME'.encode('ascii'))
        username = client.recv(1024).decode('ascii')

        # Ensures a Maximum of 20 Client Conncections. If greater than 21, so > 20. Print out that we have hit the max, and remove and close the client.
        if (len(usernames) > 20):
            print("Only 20 Connections Allowed")
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f'{username} has been disconnected.'.encode('ascii'))
            usernames.remove(username)
        else: #If not greater than 20
            # Stores New Clients in Lists
            usernames.append(username)
            clients.append(client)
        
        # Displays Username
        print("Username is {}".format(username))
        broadcast("{} has joined the chat! ".format(username).encode('ascii'))
        client.send('You have connected to the server!'.encode('ascii'))

        #Thread Hanling For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening...") #print that the server is listening
receive() #Run receive function