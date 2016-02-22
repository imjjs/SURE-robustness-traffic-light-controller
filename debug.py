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



def mytest(intersections):
    errorF = open("errorf.txt", 'w')
    port = config.generator_ports()
    sumoProcess = subprocess.Popen(
        ["sumo-gui", "-c", "VanderbiltCampus/Vanderbilt.sumo.cfg", "--tripinfo-output", "tripinfo" + str(port) + ".xml",
         "--remote-port", str(port)], stdout= config.DEVNULL, stderr = config.DEVNULL)
    #time.sleep(30)
    traci.init(port)

    for ele in intersections:
        ele.init()
    #time1 = time.time()
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
       # print intersections[1].name
        for ele in intersections:
            ele.run()
        #for ele in intersections:
        #    ele.run()

    traci.close()
    sumoProcess.wait()
    #sumoProcess.kill()
    #time2 = time.time()
    return test.avgDuration(port)

if __name__ == '__main__':
    intersections = []
    CONFIG = [(2,2),(2,6),(0,0),(0,0), (0,0), (0,0), (0,0), (0,0), (0,0)]
    for ele in config.IntersectionList:
        intersection = Intersection(ele)
        intersection.loadFromData(config.IN_DATA)
        intersections.append(intersection)

    for idx in range(len(intersections)):
        intersections[idx].setThreshold(CONFIG[idx][0], CONFIG[idx][1])

    print mytest(intersections)
