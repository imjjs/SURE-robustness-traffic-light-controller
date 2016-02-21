import matplotlib.pyplot as plt
import numpy as np


def float_to_int(f):
    if f > int(f):
        return int(f) + 1
    else:
        return int(f)


intersection_num = 9
Range = 36
BaseLine = 10.521

if __name__ == '__main__':
    x = np.arange(0, intersection_num, 1.0 / Range)
    yList = []
    for i in range(intersection_num * Range):
        yList.append(0)


    for idx in range(intersection_num):
        inputfile = open('intersection'+ str(idx)+'.txt', 'r')
        inputList = inputfile.readlines()
        print idx
        for i in range(idx*Range, (idx+1) *Range):
            print i
            yList[i] = float(inputList[i - idx* Range])

    maximum = max(yList)
    max_idx = yList.index(maximum)
    y = np.array(yList)
    plt.xlabel('inertsection, max = {peak}, {pct}%'.format(peak = maximum, pct = maximum/BaseLine*100))
    plt.ylabel('average speed(m/s)')

    plt.plot([0, intersection_num], [BaseLine, BaseLine], '-')
    plt.plot([0, intersection_num], [maximum, maximum], '-')
    plt.ylim([8,14])
    #plt.plot([0, 10.98], [5, 10.98], 'k-', lw=1)
    plt.plot(x, y)
    plt.savefig("1_7_1_10.png")
    plt.show()
