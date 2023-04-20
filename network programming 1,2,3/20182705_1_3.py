import argparse, socket
from random import *

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('Listening at', sock.getsockname())

    while True:
        print('Waiting to accept a new connection')
        sc, sockname = sock.accept()
        print('We have accepted a connection from', sockname)
        print('Socket name:', sc.getsockname())
        print('Socket peer:', sc.getpeername())

        count = 0
        x = 0
        while True:
            data = sc.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')
            # server get start message: choose a random number between 1 to 10.
            if (message == 'start'):
                count = 0
                x = randint(1, 10)
                print("Random number is ", x)
                sc.sendall(b"Guess a number between 1 to 10")
                continue

            # Send message to client based on difference between client's guessed number and random number x
            # (x = guess) -> "Congratulations you did it."
            # (x > guess) -> "You guessed too small!"
            # (x < guess) -> "You Guessed too high!"
            guess = int(message)
            if(x==guess):
                sc.sendall(b"Congratulations you did it.")
                break
            elif(x>guess):
                if (count < 4):
                    sc.sendall(b"You guessed too small!")
                    count += 1
                    continue
                else:
                    sc.sendall(b"You guessed too small!\nYou lose.")
                    break
            elif(x<guess):
                if (count < 4):
                    sc.sendall(b"You Guessed too high!")
                    count += 1
                    continue
                else:
                    sc.sendall(b"You Guessed too high!\nYou lose.")
                    break
        sc.close()
        print('Socket closed\n')

def client(host, port, bytecount):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())

    while True:
        # Send start message or guess the number
        message = input("input: ")
        message = message.encode('ascii')
        sent = 0
        while sent < bytecount:
            sock.sendall(message)
            sent += len(message)

        # Receive server's message
        reply = sock.recv(42)
        if not reply:
            break
        reply = reply.decode('utf-8')
        print(reply)

        # if guess the correct number or 5 attempts are over, stop the game
        if(reply == 'Congratulations you did it.' or 'You lose.' in reply):
            sock.shutdown(socket.SHUT_RDWR)
            break
    sock.close()

if __name__ == '__main__':
    roles = ('client', 'server')
    parser = argparse.ArgumentParser(description='Get deadlocked over TCP')
    parser.add_argument('role', choices=roles, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('bytecount', type=int, nargs='?', default=1,
                        help='number of bytes for client to send (default 1)')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    if args.role == 'client':
        client(args.host, args.p, args.bytecount)
    else:
        server(args.host, args.p)