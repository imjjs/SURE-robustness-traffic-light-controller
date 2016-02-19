import sys


import multiprocessing
import Queue
from intersection import Intersection
import config
import test3
import time
import socket




port_que = Queue.Queue()




RUN_TIMES = 3
PORT = 41000

CoreNumber = multiprocessing.cpu_count()

testRange = (1, 15)
stepLength = 1

def mytestWarp(input):
    speed = test3.mytest(input)
    return speed





def start_process():
    pass

if __name__ == '__main__':
    jobs = []
    pool = multiprocessing.Pool(processes = CoreNumber,
                                initializer = start_process)
    input = range(24)


    result = pool.map(mytestWarp, input)
    pool.close()
    pool.join()

    f = open("intersection" + ".txt", "w")
    for i in result:
        print i
        f.write(str(i) + '\n')
