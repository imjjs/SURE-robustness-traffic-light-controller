import sys


import multiprocessing
import Queue
from intersection import Intersection
import config
import test
import time
import socket
import log
import random

port_que = Queue.Queue()



INPUT_INTERSECTION = config.CompareList



CoreNumber = multiprocessing.cpu_count()

TestPeriod = 36000
testRange = (1, 20)
stepLength = 1

def mytestWarp(tup):
    speed, threshold = test.mytest(tup[0], tup[1], tup[2], tup[3], tup[4])
    return (speed, threshold)





def start_process():
    pass

if __name__ == '__main__':
    log.LogTime = time.time()
    with open('logtime','w') as f:
        f.write(str(log.LogTime))

    paraList = [1,1,1,1,1]

    #idx = random.randint(0,4)
    #priv_idx = -1
    #for idx in range(len(paraList)):
    idx = 0
    while True:
        print idx
        if time.time() - log.LogTime > TestPeriod:
            break
        pool = multiprocessing.Pool(processes = CoreNumber,
                                initializer = start_process)
        inputList = []

        for i in range(testRange[0], testRange[1], stepLength):
            inputList.append((i, paraList, INPUT_INTERSECTION, idx, config.sumoMaps))

        result = pool.map(mytestWarp, inputList)
        #result = map(mytestWarp, inputList)
        pool.close()
        pool.join()

        f = open("intersection" + str(idx) + ".txt", "w")
        for i in result:
            #print i[0], i[1], i[2]
            f.write(str(i[0]) +str(i[1])  + '\n')



        maxSpeed, maxThreshold = max(result, key = lambda x: x[0])
        f.write("final:"+ str(maxSpeed) + ',' + str(maxThreshold))

        #minDuration, minWeThreshold, minNsThreshold = min(result, key = lambda x: x[0])
        #f.write("final:"+ str(minDuration) + ',' + str(minWeThreshold) + ',' + str(minNsThreshold))

        paraList[idx] = maxThreshold
        f.flush()
        idx = (idx + 1) % 5
        time.sleep(10)

        print "sleeping at loot--------"

    print paraList
