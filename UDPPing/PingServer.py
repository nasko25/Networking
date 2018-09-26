from socket import *
from time import sleep

serverPort = 12001
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

print("Server is ready to recieve")

while True:
    message, clientAddress = serverSocket.recvfrom(100)
    serverSocket.sendto('pong'.encode(), clientAddress)
    sleep(0.5)
    if(message.decode() == "exit"):
        serverSocket.close()
        break
