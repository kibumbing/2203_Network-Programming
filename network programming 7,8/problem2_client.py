import random, threading, time, zmq
B = 32

def subscriber(zcontext, url, category):
    isock = zcontext.socket(zmq.SUB)
    isock.connect(url)
    if(category == 'sports'):
        print("Subscribe sports news.")
        isock.setsockopt(zmq.SUBSCRIBE, b'SPO')
    elif (category == 'technology'):
        print("Subscribe technology news.")
        isock.setsockopt(zmq.SUBSCRIBE, b'TEC')
    elif (category == 'science'):
        print("Subscribe science news.")
        isock.setsockopt(zmq.SUBSCRIBE, b'SCI')
    while True:
        print(isock.recv_string())

def start_thread(function, *args):
    thread = threading.Thread(target=function, args=args)
    thread.daemon = True
    thread.start()

def main(zcontext):
    category = input("Choose category[sports, technology, science]>>")
    pubsub = 'tcp://127.0.0.1:6700'
    start_thread(subscriber, zcontext, pubsub, category)
    time.sleep(30)

if __name__ == '__main__':
    main(zmq.Context())