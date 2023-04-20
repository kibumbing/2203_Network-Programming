import argparse, random, socket

def client(address, cause_error=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)

    start = 0
    while True:
        # Send start message or guess the number
        message = input("input: ")

        if message != 'start' and message != 'end' and message != 'close':
            if message.isdigit():
                if int(message)<1 or int(message)>10:
                    print("Wrong input. Try again.")
                    continue
            else:
                print("Wrong input. Try again.")
                continue

        message = message.encode('ascii')
        sock.sendall(message)

        # Receive server's message
        reply = sock.recv(128)
        if not reply:
            break
        reply = reply.decode('utf-8')
        print(reply)

        # if guess the correct number or 5 attempts are over, stop the game
        if message == b'close':
            sock.shutdown(socket.SHUT_RDWR)
            break
    sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Example client')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-e', action='store_true', help='cause an error')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    address = (args.host, args.p)
    client(address, args.e)