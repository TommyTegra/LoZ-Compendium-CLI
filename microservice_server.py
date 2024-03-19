import random
import zmq

#test3

def microservice(toop=None):
    global random_num
    if toop is None:
        random_num = 0
        return random_num
    else:
        if toop[0] == 1:
            random_num = random.randrange(1, 390)
            print(random_num)
        elif toop[0] == 2:
            random_num = random.randrange(1, 510)
        else:
            random_num = "Invalid input. Please try again."
        return random_num

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv()
    print("Received request: %s" % message)
    decoded = message.decode()
    toop = eval(decoded)

    print(toop)
    print(type(toop))
    print(toop[0])
    message = microservice(toop)
    random_num_encoded = str(message).encode()

    socket.send(random_num_encoded)

