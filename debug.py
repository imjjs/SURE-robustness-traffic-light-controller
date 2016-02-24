import sys
sys.path.append("/home/local/VANDERBILT/liy29/sumo-0.24.0/tools/")
import traci
import subprocess
import config
import os
import test
from intersection import Intersection
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import main
import time
import test

if __name__ == '__main__':
    intersections = []
    CONFIG = [(1,1),(0,0),(0,0),(0,0), (0,0), (0,0), (0,0), (0,0), (0,0)]
    for ele in config.smallMap:
        intersection = Intersection(ele)
        intersection.loadFromData(config.IN_DATA)
        intersections.append(intersection)

    # fix_config = [1500,1100,1100,700,1100]
    # for idx in range(len(intersections)):
    #     intersections[idx].lightMax = max([fix_config[idx], 1800 - fix_config[idx]])
    #     intersections[idx].lightMin = min([fix_config[idx], 1800 - fix_config[idx]])

    for idx in range(len(intersections)):
        intersections[idx].setThreshold(CONFIG[idx][0], CONFIG[idx][1])

    print test.mytest(1,1,intersections,0)
