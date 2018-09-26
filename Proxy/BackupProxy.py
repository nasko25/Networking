from socket import *
import ssl
import time
from threading import Thread

COUNTER = 0
def get_hostname_and_port(string):
    semicolon_position = 0
    for character in string:
        if character == ":":
            break
        else:
            semicolon_position += 1
    hostname_and_port = [string[:semicolon_position], string[(semicolon_position+1):]]
    return hostname_and_port
    
def recieve_data():
    try:
        response = None
        response = sendingSocket.recv(800000000)
        receivingSocket.send(response)
        return not response
    except timeout:
        print "tout"
        global COUNTER
        COUNTER += 1
        return response
        # break

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

    receivingSocket.settimeout(1)
    sendingSocket.settimeout(2)
    waiting = "..."
    if sendingSocket is not None:
        break_from_loop = False
        while True and sendingSocket is not None and not break_from_loop:
            try:
                request = receivingSocket.recv(2048)
                sendingSocket.send(request)
                print waiting
            except timeout:
                print "timeout"
                break
        #  except timeout:
             #   print "timeout"
            #  break
            # if request.split()[0] != "GET":
                # break
            # TODO establish a TLS connection
            # try:
            checker = recieve_data()
            counter = 0
            COUNTER = 0
            while checker:
                checker = recieve_data()
                print "recieved data"
                counter += 1
            if counter > 0 or COUNTER > 0:
                break_from_loop = True
                break

    receivingSocket.close()
    sendingSocket.close()

