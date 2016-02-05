import sys


import multiprocessing
import Queue
from intersection import Intersection
import config
import test
import time



PORT = 41000

CoreNumber = multiprocessing.cpu_count()

que = Queue.Queue()

def mytestWarp(tup):
    return test.mytest(tup[0], tup[1], tup[2], tup[3], tup[4])





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
    testRange = (1, 20)
    stepLength = 2
    for idx in range(len(intersections)):
        pool = multiprocessing.Pool(processes = CoreNumber,
                                initializer = start_process)
        inputList = []
        procID = PORT
        for i in range(testRange[0], testRange[1], stepLength):
            for j in range(testRange[0], testRange[1], stepLength):
                inputList.append((i, j, intersections, idx, procID))
                procID += 1

        result = pool.map(mytestWarp, inputList)
        pool.close()
        pool.join()

        f = open("intersection" + str(idx) + ".txt", "a")
        for i in result:
            print i[0]
            f.write(str(i[0]) + '\n')
        maxSpeed, minWeThreshold, minNsThreshold = max(result, key =
lambda x: x[0])
        f.write("final:"+ str(maxSpeed) + ',' + str(minWeThreshold) + ',' + str(minNsThreshold))
        intersections[idx].setThreshold(minWeThreshold, minNsThreshold)
        f.flush()
        time.sleep(30)
        print "sleeping--------"
