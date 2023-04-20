import json
import zlib
import socket
import ssl


class Solution():
    
    def special_bits(self, L=1, R=2, k=1):
        num = -2
        # Write your code between start and end for solution of problem 1
        # Start
        count = 0
        for i in range(L, R+1):
            cnt = 0
            target = i
            while target != 0:
                cnt += target % 2
                target = int(target / 2)
            if cnt == k:
                num = i
                break
        if num == -2:
            num = -1
        # End
        return num

    def toggle_string(self, S):
        s = ""
        # Write your code between start and end for solution of problem 2
        # Start
        for i in range(0, len(S)):
            alphabet = ord(S[i])
            if alphabet >=65 and alphabet<=90:
                alphabet += 32
            elif alphabet >=97 and alphabet <=122:
                alphabet -= 32
            s = s + chr(alphabet)
        # End
        return s

    def send_message(self, message):
        message = self.to_json(message)
        message = self.encode(message)
        message = self.compress(message)
        return message

    def recv_message(self, message):
        message = self.decompress(message)
        message = self.decode(message)
        message = self.to_python_object(message)
        return message
    
    # String to byte
    def encode(self, message):
        # Write your code between start and end for solution of problem 3
        # Start
        return message.encode("ascii")
        # End
        
    
    # Byte to string
    def decode(self,message):
        # Write your code between start and end for solution of problem 3
        # Start
        return message.decode("utf-8")
        # End 

    # Convert from python object to json string
    def to_json(self, message):
        # Write your code between start and end for solution of problem 3
        # Start
        return json.dumps(message)
        # End 

    # Convert from json string to python object
    def to_python_object(self, message):
        # Write your code between start and end for solution of problem 3
        # Start
        return json.loads(message)
        # End 
    
    # Returns compressed message 
    def compress(self, message):
        # Write your code between start and end for solution of problem 3
        # Start
        return zlib.compress(message)
        # End 

    # Returns decompressed message
    def decompress(self, compressed_message):
        # Write your code between start and end for solution of problem 3
        # Start
        return zlib.decompress(compressed_message)
        # End 


    def client(self, host, port, cafile=None):
        # Write your code between start and end for solution of problem 4
        # Start
        purpose = ssl.Purpose.SERVER_AUTH
        context = ssl.create_default_context(purpose, cafile=cafile)
        context.check_hostname = False

        raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        raw_sock.connect((host, port))
        print("Connected to host {!r} and port {}".format(host, port))
        ssl_sock = context.wrap_socket(raw_sock, server_hostname=host)

        while True:
            data = ssl_sock.recv(1024)
            if not data:
                break
            output = data.decode('utf-8')
        cert = ssl_sock.getpeercert() # Variable to store the certificate received from server
        cipher = ssl_sock.cipher() # Variable to store cipher used for connection
        msg = output # Variable to store message received from server

        ssl_sock.close()
        # End
        return cert, cipher, msg
    
    

    
