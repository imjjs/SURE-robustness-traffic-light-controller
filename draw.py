import matplotlib.pyplot as plt
import numpy as np


def float_to_int(f):
    if f > int(f):
        return int(f) + 1
    else:
        return int(f)

L = 5
intersection_num = 5
Range = 100
if __name__ == '__main__':
    x = np.arange(0, L, float(L) / intersection_num / Range)
    yList = []
    for i in range(intersection_num * Range):
        yList.append(0)


    for idx in range(L):
        inputfile = open('intersection'+ str(idx)+'.txt', 'r')
        inputList = inputfile.readlines()
        print idx
        for i in range(idx*Range, (idx+1) *Range):
            print i
            yList[i] = float(inputList[i - idx* Range])


    y = np.array(yList)
    plt.xlabel('inertsection')
    plt.ylabel('average speed(m/s)')
    plt.plot([0, 4], [10.521, 10.521], '-')
    plt.plot([0,4], [10.95, 10.95], '-')
    #plt.plot([0, 10.98], [5, 10.98], 'k-', lw=1)
    plt.scatter(x, y)
    plt.savefig("1_20_2.png")
    plt.show()
