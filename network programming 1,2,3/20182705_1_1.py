import socket
from urllib.parse import quote_plus

request_text = """\
GET /iss-pass.json?lat={}&lon={} HTTP/1.1\r\n\
Host: api.open-notify.org\r\n\
User-Agent: kibum\r\n\
Connection: close\r\n\
\r\n\
"""

def issTime(lat, lon):
    sock = socket.socket()  # create socket
    sock.connect(('api.open-notify.org', 80))   # request connection
    request = request_text.format(quote_plus(lat), quote_plus(lon))
    sock.sendall(request.encode('ascii'))   # encode and send data
    raw_reply = b''
    while True:
        more = sock.recv(4096)  # receive data
        if not more:
            break
        raw_reply += more
    print(raw_reply.decode('utf-8'))    # decode and print data

if __name__ == '__main__':
    issTime('45', '180')
