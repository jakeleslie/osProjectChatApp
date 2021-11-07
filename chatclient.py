import threading
import socket

# Lets Client Choose Username
username = input("Choose a username: ")

# Server Conncection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1',44444))

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
        message = '{}: {}'.format(username, input(''))
        client.send(message.encode('ascii'))

# Threads for Listening and Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()