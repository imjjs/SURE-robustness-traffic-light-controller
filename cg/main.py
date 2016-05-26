import sys


import multiprocessing
import config
import test
from optparse import OptionParser

INPUT_INTERSECTION = config.CompareList


testRange = (2, 30)
stepLength = 2


def mytestWarp(tup):
    speed, we, ns = test.mytest(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
    return (speed, we, ns,)
def start_process():
    pass

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--cores", dest="cores")
    parser.add_option("-i", "--intersectionID", dest="iid")
    parser.add_option("-p", "--parameter", dest="pm")
    (options, args) = parser.parse_args()
    pstring = options.pm
    pl = pstring.split(',')
    parameterList = []
    for idx in range(0,len(pl),2):
        t = (int(pl[idx]), int(pl[idx + 1]))
        parameterList.append(t)

    pool = multiprocessing.Pool(processes = int(options.cores))
    inputList = []
    inputList.append((0, 0, parameterList, INPUT_INTERSECTION, int(options.iid), config.sumoMaps))

    for i in range(testRange[0], testRange[1], stepLength):
        for j in range(testRange[0], testRange[1], stepLength):
            inputList.append((i, j, parameterList, INPUT_INTERSECTION, int(options.iid), config.sumoMaps))


    result = pool.map(mytestWarp, inputList)
    #result = map(mytestWarp, inputList)
    pool.close()
    pool.join()

    f = open("intersection" + str(options.iid) + ".txt", "w")
    for i in result:
        #print i[0], i[1], i[2]
        f.write(str(i[0]) +str(i[1]) + str(i[2]) + '\n')



    maxSpeed, minWeThreshold, minNsThreshold = max(result, key = lambda x: x[0])
    f.write("final:"+ str(maxSpeed) + ',' + str(minWeThreshold) + ',' + str(minNsThreshold))

    #minDuration, minWeThreshold, minNsThreshold = min(result, key = lambda x: x[0])
    #f.write("final:"+ str(minDuration) + ',' + str(minWeThreshold) + ',' + str(minNsThreshold))

    print str(minWeThreshold) + ',' + str(minNsThreshold)
