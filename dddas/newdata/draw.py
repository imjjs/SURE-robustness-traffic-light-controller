import matplotlib.pyplot as plt
import numpy as np
xmax = 7000

def float_to_int(f):
    if f > int(f):
        return int(f) + 1
    else:
        return int(f)
def drawLine(file, _color, _label, end):
    x = []
    y = []
    max = 0
    with open(file,'r') as f:
        lns = f.readlines()
        for l in lns:
            st = l[:-1].split(' ')
            if float(st[0]) > xmax:
                if end:
                    x.append(xmax)
                    y.append(max)
                break
            # x.append(float(st[0]))

            if float(st[1]) > max:
                x.append(float(st[0]))
                y.append(float(st[1]))
                max = float(st[1])
    plt.ylim([8.0,10.5])
    return plt.plot(x, y, color = _color, label = _label)

import random
def drawLine2(file, _color, _label):
    x = []
    y = []
    max = 0
    start_point = 0
    with open(file, 'r') as f:
        lns = f.readlines()
        for l in lns:
            st = l[:-1].split(' ')
            if float(st[0]) - start_point > xmax:
                break

            if 0 != start_point:
                x.append(float(st[0]) - start_point)
            if float(st[1]) > max:
                if 0 == start_point:
                    start_point = float(st[0])-180 + random.randint(0,40)
                    x.append(float(st[0]) - start_point)
                y.append(float(st[1]))
                max = float(st[1])
            else:
                if 0 != start_point:
                    y.append(max)




    plt.ylim([8.0,10.5])

    return plt.plot(x, y, color = _color, label = _label)

if __name__ == '__main__':
    lineCD = drawLine('cd301423.data', 'red','CG', True)
    #lineKCD = drawLine('k13scd310046.data', 'blue','sync KCG', True)
    lineAKCD = drawLine('ak13scd312024.data', 'green','sync AKCG', False)
    #lineASYNC_KCD = drawLine('asyncK13scd312339.data','black','async KCG', True)
    lineASYNC_AKCD = drawLine('asyncAK13scd010911.data','orange','async AKCG', False)
    plt.legend(loc = 0)
    plt.xlabel('running time (s)')
    plt.ylabel('average speed (m/s)')

    plt.savefig('big1' + '.png')
    plt.show()
