import subprocess
import multiprocessing
import config
import dummy
import time
import log
import random
import test


INPUT_INTERSECTION = config.CompareList



CoreNumber = 32
K = 4
TestPeriod = 36000

def equal(a, b):
    return abs(a - b) < 1e-6

def mytestWarp(tup):
    speed, we, ns = test.mytest(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
    return (speed, we, ns,)


if __name__ == '__main__':
    log.LogTime = time.time()
    with open('logtime','w') as f:
        f.write(str(log.LogTime))


    priv_func = 0.0
    paraList = []
    for ele in INPUT_INTERSECTION:
        paraList.append((0,0,))


    while True:
        if time.time() - log.LogTime > TestPeriod:
            break

        outParaLt = []
        for ele in paraList:
            outParaLt.append(str(ele[0]))
            outParaLt.append(str(ele[1]))
        outParaStr = ','.join(outParaLt)
        cores = CoreNumber / K

        KDict = {}
        PDict = {}
        while True:
            ri = random.randint(0, len(paraList)-1)
            if ri not in KDict.keys():
                KDict[ri] = open('inter' + str(ri) +'.txt','w')
            if len(KDict) == K:
                break

        for itID in KDict.keys():
            PDict[itID] = subprocess.Popen(['python', 'dummy.py', '-c', str(cores), '-i', str(itID), '-p', outParaStr], stdout=KDict[itID])
        for itID in PDict.keys():
            PDict[itID].wait()

        RDict = {}
        for itID in KDict.keys():
            f = open('inter' + str(itID)+'.txt','r')
            tmp = f.readline()[0:-1].split(',')
            RDict[itID] = (int(tmp[0]),int(tmp[1]))



        pool = multiprocessing.Pool(processes = CoreNumber)
        inputList = []
        configurations = []
        assert (len(RDict.keys()) == K)
        for i in range(2**K):
            tmp = bin(i)[2:].zfill(K)
            newParaList = paraList[:]
            for idx in range(len(tmp)):
                if tmp[idx] == '1':
                    newParaList[RDict.keys()[idx]] = RDict[RDict.keys()[idx]]
            configurations.append(newParaList)

        for para in configurations:
            inputList.append((para[0][0], para[0][1], para, INPUT_INTERSECTION, 0, config.sumoMaps))

        result = pool.map(mytestWarp, inputList)
        #result = map(mytestWarp, inputList)
        pool.close()
        pool.join()

        maxspeed = result[0][0]
        maxidx = 0
        for idx in range(len(result)):
            if result[idx][0] > maxspeed:
                maxidx = idx
                maxspeed = result[idx][0]
        print configurations
        print result
        paraList = configurations[maxidx]
        if equal(priv_func, maxspeed):
            K = K/2
            if K == 0:
                K = 1
        priv_func = maxspeed