import sys


import multiprocessing
import Queue
from intersection import Intersection
import config
import test
import time
import socket
import log


port_que = Queue.Queue()



INPUT_INTERSECTION = config.CompareList



CoreNumber = 8

TestPeriod = 25200
testRange = (1, 10)
stepLength = 1

def mytestWarp(tup):
    speed, we, ns = test.mytest(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
    return (speed, we, ns,)





def start_process():
    pass

if __name__ == '__main__':
    log.LogTime = time.time()
    with open('logtime','w') as f:
        f.write(str(log.LogTime))
    jobs = []
    paraList = []
    for ele in INPUT_INTERSECTION:
        paraList.append((0,0,))


    # fix_config = [1500,1100,1100,700,1100]
    # for idx in range(len(intersections)):
    #     intersections[idx].lightMax = max([fix_config[idx], 1800 - fix_config[idx]])
    #     intersections[idx].lightMin = min([fix_config[idx], 1800 - fix_config[idx]])

#    mytest(10,10, intersections,1,41000)
    idx = 0
    #for idx in range(len(paraList)):
    while True:
        if time.time() - log.LogTime > TestPeriod:
            break
        pool = multiprocessing.Pool(processes = CoreNumber,
                                initializer = start_process)
        inputList = []
        inputList.append((0, 0, paraList, INPUT_INTERSECTION, idx, config.sumoMaps))

        for i in range(testRange[0], testRange[1], stepLength):
            for j in range(testRange[0], testRange[1], stepLength):
                inputList.append((i, j, paraList, INPUT_INTERSECTION, idx, config.sumoMaps))
                #procID += 1




        result = pool.map(mytestWarp, inputList)
        #result = map(mytestWarp, inputList)
        pool.close()
        pool.join()

        f = open("intersection" + str(idx) + ".txt", "w")
        for i in result:
            #print i[0], i[1], i[2]
            f.write(str(i[0]) + '\n')



        maxSpeed, minWeThreshold, minNsThreshold = max(result, key = lambda x: x[0])
        f.write("final:"+ str(maxSpeed) + ',' + str(minWeThreshold) + ',' + str(minNsThreshold))

        #minDuration, minWeThreshold, minNsThreshold = min(result, key = lambda x: x[0])
        #f.write("final:"+ str(minDuration) + ',' + str(minWeThreshold) + ',' + str(minNsThreshold))

        paraList[idx] = (minWeThreshold, minNsThreshold,)
        f.flush()
        idx = (idx + 1) % len(paraList)
        time.sleep(10)

        print "sleeping at loot--------"

    print paraList
