from socket import *
import time 

serverName = '192.168.56.1'
serverPort = 12001

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1) # setting a timeout for 1 second, so if the packet does not arrive, the client can abort waiting

for i in range(0, 10):  # you have to send the message 10 times => 0 to 9 (10 times)
    start = time.time()
    clientSocket.sendto("ping".encode(), (serverName, serverPort))
    try:
        message, serverAddress = clientSocket.recvfrom(100)
    except timeout:
        print("1 second has passed with no response")
        continue
    print("{}; elapsed time:{}".format(message, (time.time()-start)))

clientSocket.sendto("exit".encode(), (serverName, serverPort))
clientSocket.close()
