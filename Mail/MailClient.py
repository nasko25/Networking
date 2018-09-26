from socket import *
import ssl
import base64

serverName = "smtp.gmail.com"
serverPort = 465 # because SSL
endOfMessage = ".\r\n"

def getMailAndPass():
    email = raw_input("Mail: ")
    password = raw_input("Password: ")
    return [email, password]

def encode64(string):
    return base64.b64encode(string)

def is_end_of_sentence(word):
    return word == "." or word == "?" or word == "-" or word == "!" or word == "--"

# set up the socket connection
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket = ssl.wrap_socket(clientSocket)
clientSocket.connect((serverName, serverPort)) 
serverMessage = clientSocket.recv(2048).decode()
print serverMessage
if serverMessage[:3] != "220":
    print "not 220"

clientSocket.send("EHLO test\r\n".encode())
serverMessage = clientSocket.recv(2048).decode()
print serverMessage
if serverMessage[:3] != "250":
    print "not 250"

while True:
    authentication = getMailAndPass()
    encodedMail = encode64(authentication[0])
    print encodedMail
    encodedPass = encode64(authentication[1])
    print encodedPass
    clientSocket.send("AUTH LOGIN\r\n".encode())
    serverMessage = clientSocket.recv(2048).decode()
    print base64.b64decode(serverMessage[4:]) # for debugging purposes
    if serverMessage[:3] != "334":
        print "not 334"

    clientSocket.send(encodedMail + "\r\n")
    serverMessage = clientSocket.recv(2048).decode()
    print base64.b64decode(serverMessage[4:]) # for debugging purposes
    if serverMessage[3:] != "334":
        print "not 334"

    clientSocket.send(encodedPass + "\r\n")
    serverMessage = clientSocket.recv(2048).decode()
    print serverMessage
    if serverMessage[3:] == "235":
        print "Authentication successful"
        break
    else:
        print "Try again."

while True:
    clientSocket.send(("MAIL FROM: <%s>\r\n" % authentication[0]).encode())
    serverMessage = clientSocket.recv(2048).decode()
    print serverMessage
    if serverMessage[:3] != "250":
        print "not 250"
    
    recipient = raw_input("Who is the recipient of the email? ")
    clientSocket.send(("RCPT TO: <%s>\r\n" % recipient).encode())
    serverMessage = clientSocket.recv(2048).decode()
    print serverMessage
    if serverMessage[:3] != "250":
        print "not 250"
    
    clientSocket.send("DATA\r\n".encode())
    serverMessage = clientSocket.recv(2048).decode()
    print serverMessage
    if serverMessage[:3] != "354":
        print "not 354"

    message = raw_input("What is the message you want to send?")
    messageToSend = ""
    for word in message.split():
        if is_end_of_sentence(word):
            messageToSend += (word + "\r\n")
        else:
            messageToSend += word
    messageToSend += endOfMessage
    clientSocket.send(messageToSend.encode()) # Will it work though?
    serverMessage = clientSocket.recv(2048).decode()
    print serverMessage
    if serverMessage[:3] != "250":
        print "not 250"

    response = raw_input("Do you want to send another email?(y/n)")
    if response != "y" or response != "yes":
        break

clientSocket.send("QUIT\r\n".encode())
serverMessage = clientSocket.recv(2048).decode()
print serverMessage
if serverMessage[:3] != "221":
    print "not 221"

clientSocket.close()
print "The connection has ended"
