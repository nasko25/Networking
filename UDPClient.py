from socket import *

serverName = '192.168.56.1'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

while True:
    message = raw_input('Input lowercase sentence: ')
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048) # 2048 is the buffer size

    print(modifiedMessage.decode())
    if (message == "exit"): 
        clientSocket.close()
        break
