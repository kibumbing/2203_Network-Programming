import argparse, socket, asyncio
from random import *

@asyncio.coroutine
def handle_conversation(reader, writer):
    address = writer.get_extra_info('peername')
    print('Accepted connection from {}'.format(address))

    count = 0
    x = 0
    while True:
        data = yield from reader.read(4096)
        if not data:
            break

        message = data.decode('utf-8')

        if message != 'start' and message != 'close':
            writer.write(b"Wrong input. Try again.")
            continue
        elif message == 'start':
            count = 0
            x = randint(1, 10)
            print(f"[{address}]Random number is ", x)
            writer.write(b"Guess a number between 1 to 10")
            while True:
                data = yield from reader.read(4096)
                if not data:
                    break

                message = data.decode('utf-8')

                if message == 'end':
                    writer.write(b"Game end.")
                    break
                elif message == 'close':
                    break
                elif not message.isdigit():
                    writer.write(b"Wrong input. Please input a number between 1 to 10 or end or close.")
                    continue

                guess = int(message)
                if x == guess:
                    writer.write(b"Congratulations you did it.")
                    break
                elif x > guess:
                    if count < 4:
                        writer.write(b"You guessed too small!")
                        count += 1
                        continue
                    else:
                        writer.write(b"You guessed too small!\nYou lose.")
                        break
                elif x < guess:
                    if count < 4:
                        writer.write(b"You Guessed too high!")
                        count += 1
                        continue
                    else:
                        writer.write(b"You Guessed too high!\nYou lose.")
                        break
        if message == 'close':
            print(f"Close the connection with {address}")
            writer.write(b"Close the connection.")
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='asyncio server using coroutine')
    parser.add_argument('host', help='IP or hostname')
    parser.add_argument('-p', metavar='port', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    address = (args.host, args.p)
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_conversation, *address)
    server = loop.run_until_complete(coro)
    print('Listening at {}'.format(address))
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.close()