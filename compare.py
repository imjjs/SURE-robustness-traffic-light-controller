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
        ["sumo", "-c", "VanderbiltCampus/Vanderbilt.sumo.cfg", "--tripinfo-output", "tripinfo" + str(port) + ".xml",
         "--remote-port", str(port)], stdout= config.DEVNULL, stderr = config.DEVNULL)

    traci.init(port)

    for ele in intersections:
        ele.init()
    #time1 = time.time()
    while traci.simulation.getMinExpectedNumber() > 0:

        for ele in intersections:
            ele.fixRun()
        traci.simulationStep()


    traci.close()
    sumoProcess.wait()

    return test.avgSpeed(port)

if __name__ == '__main__':
    intersections = []
    fix_config = [1500,1100,1100,700,1100]
    for ele in config.CompareList:
        intersection = Intersection(ele)
        intersection.loadFromData(config.IN_DATA)
        intersections.append(intersection)

    for idx in range(len(intersections)):
        intersections[idx].fixRunSetColck(fix_config[idx], 1800-fix_config[idx])

    print mytest(intersections)
