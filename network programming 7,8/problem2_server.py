import random, threading, time, zmq, string
B = 32

def string_generator(digits):
    news = ''.join(random.choice(string.ascii_letters) for _ in range(int(digits/8-3)))
    if ord(news[0])>=65 and ord(news[0])<=82:
        gen_str = 'SPO' + news
    elif (ord(news[0])>=83 and ord(news[0])<=90) or (ord(news[0])>=97 and ord(news[0])<=105):
        gen_str = 'TEC' + news
    elif ord(news[0])>=106 and ord(news[0])<=122:
        gen_str = 'SCI' + news
    print(gen_str)
    return gen_str

def publisher(zcontext, url):
    zsock = zcontext.socket(zmq.PUB)
    zsock.bind(url)
    while True:
        zsock.send_string(string_generator(B * 2))
        time.sleep(0.1)

def start_thread(function, *args):
    thread = threading.Thread(target=function, args=args)
    thread.daemon = True  # so you can easily Ctrl-C the whole program
    thread.start()

def main(zcontext):
    pubsub = 'tcp://127.0.0.1:6700'
    start_thread(publisher, zcontext, pubsub)
    time.sleep(30)

if __name__ == '__main__':
    main(zmq.Context())