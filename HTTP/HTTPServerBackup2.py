from socket import *
from zipfile import *

MAX_PACKET = 32768

def normalize_line_endings(s):
    return ''.join((line + '\n') for line in s.splitlines())

serverPort = 80
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('Server is ready to recieve.')

while True:
    connectionSocket, addr = serverSocket.accept()
    recieved = normalize_line_endings(connectionSocket.recv(MAX_PACKET))
    requestHead, requestBody = recieved.split('\n\n', 1)

    # print requestHead

    requestHead = requestHead.splitlines()
    requestHead_line = requestHead[0]
    response_body = []
    content_type = ''
    possible_requested_files = ['/sth', '/ ', '/main.css', '/logo.png', '/background.jpg', '/image1.jpg', '/image2.jpg', '/image3b.jpg', '/image4b.jpg', '/image5.jpg', '/image6.jpg', '/Squirrel.jpg']
    for file_ in possible_requested_files:
        if file_ in requestHead_line:
            if file_ == '/sth' or file_ == '/ ':
                if file_ == '/ ':
                    response_body = open('../../Responsive/index.html')
                    content_type = 'text/html'
                else: 
                    response_body = [
                            '<html><body><h1> IT WORKS! </h1>', 
                            '</body></html>'
                            ]
                    content_type = 'text/html'
            else: 
                response_body = open('../../Responsive%s' % file_, 'rb').read()
                if '.css' in file_:
                    content_type = 'text/css'
                elif '.png' in file_:
                    content_type = 'image/png'
                elif '.jpg' in file_:
                    content_type = 'image/jpg'
    if not response_body or content_type == '': # checks if response_body is empty array
        if '/favicon.ico' not in requestHead_line:
            print '404 not page not found must be returned'
    # end of testing 

    request_headers = dict(x.split(': ', 1) for x in requestHead[1:])
    request_method, request_uri, request_proto = requestHead_line.split(' ', 3)

    if 'image' not in content_type:
        response_body_raw = ''.join(response_body)
    else:
        response_body_raw = bytes(response_body)

    response_headers = {
            'Content-Type': content_type,
            'Content-Length': len(response_body_raw),
            'Connection': 'close',
            }

    response_headers_raw = ''.join('%s: %s\n' % (k,v) for k, v in response_headers.iteritems())
    response_proto = 'HTTP/1.1'
    response_status = '200' #TODO 404 if no page found
    response_status_text = 'OK'

    connectionSocket.send('%s %s %s\n' % (response_proto, response_status, response_status_text))
    connectionSocket.send(response_headers_raw)
    connectionSocket.send('\r\n')
    connectionSocket.send(response_body_raw)
    # connectionSocket.send(bytes(open('../../Responsive/main.css', 'rb').read()))
    connectionSocket.close()
    # download the stackoverflow answer as well!
