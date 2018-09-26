from socket import *

serverName = '192.168.56.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM) 
clientSocket.connect((serverName, serverPort))
sentence = raw_input("Input lowercase sentense: ")
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('From server:', modifiedSentence.decode())
clientSocket.close()
