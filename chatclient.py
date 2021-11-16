# Need to import these to use threads, and to use sockets
import threading, socket

# Use this function to easily get the host name for easy connections
host = socket.gethostname() 
# Manually setting our port to 4000
port = 4000
# Letting the current client choose their username
username = input("Choose a username: ") 

#Creating a socket 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connecting to the host and port that we have
client.connect((host, port)) 

# Listens to Server and Sends Username
def receive():
    while True:
        try: #While true receive messages from the server, with a size of 1024 bites and decode
            message = client.recv(1024).decode('ascii')
            if message == 'NAME':
                client.send(username.encode('ascii')) #If message == NAME, then encode the ascii
            else: #else we print out the message
                print(message)
        except:
            # Closes Connection for Error
            print("An error with the client has occurred.")
            client.close() # Throws an exception if there is an issue, and prints out that theres a problem and closes the client.
            break
        
#Sends Messages to Server
def write():
    while True: #While true, output our message in the form of: username > hello there!
        message = '{} > {}'.format(username, input(''))
        client.send(message.encode('ascii')) 

# Threads for Listening and Writing
#This thread receives
receive_t = threading.Thread(target=receive) 
receive_t.start()

#This thread writes
write_t = threading.Thread(target=write)
write_t.start()