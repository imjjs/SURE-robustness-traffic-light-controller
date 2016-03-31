import sys


import multiprocessing
import Queue
from intersection import Intersection
import config
import test
import time


import socket
def get_open_port(howMany=1):
    """Return a list of n free port numbers on localhost"""
    results = []
    sockets = []
    for x in range(howMany):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        # work out what the actual port number it's bound to is
        addr, port = s.getsockname()
        results.append(port)
        sockets.append(s)

    for s in sockets:
        s.close()

    return results

port_que = Queue.Queue()

def generator_ports():
    ports = get_open_port(84)
    print ports
    for i in ports:
        port_que.put_nowait(i)



PORT = 41000

CoreNumber = multiprocessing.cpu_count()

testRange = (1, 7)
stepLength = 1
CONFIGURE = []


def mytestWarp(tup):
    return test.mytest(tup[0], tup[1], tup[2], tup[3])





def start_process():
    pass

if __name__ == '__main__':
    jobs = []


    intersections = []
    for ele in config.IntersectionList:
        intersection = Intersection(ele)
        intersection.loadFromData(config.IN_DATA)
        intersections.append(intersection)

#    mytest(10,10, intersections,1,41000)
    for idx in range(len(CONFIGURE)):
        intersections[idx].setThreshold(CONFIGURE[idx][0], CONFIGURE[idx][1])

    for idx in range(len(CONFIGURE), len(intersections)):
        pool = multiprocessing.Pool(processes = CoreNumber,
                                initializer = start_process)
        ports = get_open_port(((testRange[1] - testRange[0] + 1)/stepLength)**2 + 10)

        inputList = []
       # procID = PORT
        t = 0
        for i in range(testRange[0], testRange[1], stepLength):
            for j in range(testRange[0], testRange[1], stepLength):
                inputList.append((i, j, intersections, idx, ports[t], ports[t]))
                #procID += 1
                t += 1

        result = pool.map(mytestWarp, inputList)
        pool.close()
        pool.join()

        f = open("intersection" + str(idx) + ".txt", "w")
        for i in result:
            print i[0]
            f.write(str(i[0]) + '\n')
        maxSpeed, minWeThreshold, minNsThreshold = max(result, key =
lambda x: x[0])
        f.write("final:"+ str(maxSpeed) + ',' + str(minWeThreshold) + ',' + str(minNsThreshold))
        intersections[idx].setThreshold(minWeThreshold, minNsThreshold)
        f.flush()
        time.sleep(30)
        print "sleeping at loot--------"
