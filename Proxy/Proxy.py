from socket import *
import ssl
import time
from threading import Thread

def get_hostname_and_port(string):
    semicolon_position = 0
    for character in string:
        if character == ":":
            break
        else:
            semicolon_position += 1
    hostname_and_port = [string[:semicolon_position], string[(semicolon_position+1):]]
    return hostname_and_port


PORT = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", PORT))
serverSocket.listen(1)
print "Proxy is ready for a connection (only 1 at the moment)!!!"
threads = []
# receivingSocket...
# TODO interesting challenge: https://stackoverflow.com/questions/4495176/nth-word-in-a-text
while True:
    Thread().start()
    receivingSocket, addr = serverSocket.accept()
    request = receivingSocket.recv(2048)
    print request
    sendingSocket = socket(AF_INET, SOCK_STREAM)
    # TODO put it in a try except: 
    if request.split()[0] == "CONNECT":
        connect_to = request.split()[1]
        print connect_to
   
        hostname_and_port = get_hostname_and_port(connect_to)
        hostname = gethostbyname(hostname_and_port[0])
        port = int(hostname_and_port[1])
        print "Hostname: {0} and port: {1}".format(hostname, port)

        # sendingSocket = socket(AF_INET, SOCK_STREAM)
        # sendingSocket = ssl.wrap_socket(sendingSocket)
        sendingSocket.connect((hostname, port))
        receivingSocket.send("HTTP/1.1 200 Connection Established\r\nProxy-agent: Pyx\r\n\r\n".encode())
        # while True:
          #  try:

    receivingSocket.settimeout(0.05)
    sendingSocket.settimeout(0.05)
    waiting = "..."
    
    should_break = False
    counter = 0
    while not should_break:
        try:
            request = receivingSocket.recv(2048)
            sendingSocket.send(request)
        except:
            if not request:
                should_break = True
            print "timeout"
        try:
            response = sendingSocket.recv(800000000)
            receivingSocket.send(response)
            if not response:
                break
        except:
            if not response or counter > 0:
                should_break = True
            counter += 1
            print "tout"

    receivingSocket.close()
    sendingSocket.close()
