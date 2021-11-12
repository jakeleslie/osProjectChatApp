import threading, socket

host = socket.gethostname() #use this for the abstraction of getting the host name
port = 4000 #setting port
# Lets Client Choose Username
username = input("Choose a username: ") 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating the socket
client.connect((host, port)) #Connecting to the server by passing in the hostname, and our shared port

# Listens to Server and Sends Username
def receive():
    while True:
        try:
            # Receives Messages From Server
            message = client.recv(1024).decode('ascii')
            if message == 'NAME':
                client.send(username.encode('ascii'))
            else:
                print(message)
        except:
            # Closes Connection for Error
            print("An error with the client has occurred.")
            client.close()
            break
        
#Sends Messages to Server
def write():
    while True:
        message = '{} > {}'.format(username, input(''))
        client.send(message.encode('ascii'))

# Threads for Listening and Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()