import sys


import multiprocessing
import Queue
from intersection import Intersection
import config
import test
import time
import socket




port_que = Queue.Queue()





PORT = 41000

CoreNumber = multiprocessing.cpu_count()

testRange = (1, 15)
stepLength = 1

def mytestWarp(tup):

    speed, we, ns = test.mytest(tup[0], tup[1], tup[2], tup[3])
    return (speed, we, ns,)





def start_process():
    pass

if __name__ == '__main__':
    jobs = []


    intersections = []
    for ele in config.CompareList:
        intersection = Intersection(ele)
        intersection.loadFromData(config.IN_DATA)
        intersection.setThreshold(0, 0)
        intersections.append(intersection)
    assert len(intersections) == 5

    fix_config = [1500,1100,1100,700,1100]
    for idx in range(len(intersections)):
        intersections[idx].lightMax = max([fix_config[idx], 1800 - fix_config[idx]])
        intersections[idx].lightMin = min([fix_config[idx], 1800 - fix_config[idx]])

#    mytest(10,10, intersections,1,41000)

    for idx in range(len(intersections)):
        pool = multiprocessing.Pool(processes = CoreNumber,
                                initializer = start_process)
        inputList = []
        inputList.append((0, 0, intersections, idx,))
       # procID = PORT
        t = 0
        for i in range(testRange[0], testRange[1], stepLength):
            for j in range(testRange[0], testRange[1], stepLength):
                inputList.append((i, j, intersections, idx,))
                #procID += 1
                t += 1

        result = pool.map(mytestWarp, inputList)
        pool.close()
        pool.join()

        f = open("intersection" + str(idx) + ".txt", "w")
        for i in result:
            print i[0]
            f.write(str(i[0]) + '\n')



        maxSpeed, minWeThreshold, minNsThreshold = max(result, key = lambda x: x[0])
        f.write("final:"+ str(maxSpeed) + ',' + str(minWeThreshold) + ',' + str(minNsThreshold))

        #minDuration, minWeThreshold, minNsThreshold = min(result, key = lambda x: x[0])
        #f.write("final:"+ str(minDuration) + ',' + str(minWeThreshold) + ',' + str(minNsThreshold))

        intersections[idx].setThreshold(minWeThreshold, minNsThreshold)
        f.flush()
        time.sleep(10)
        print "sleeping at loot--------"
