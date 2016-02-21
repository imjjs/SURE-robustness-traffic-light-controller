import sys
sys.path.append("/home/local/VANDERBILT/liy29/sumo-0.24.0/tools/")
import traci
import subprocess
import config
import os
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
    time.sleep(30)
    traci.init(port)

    #time1 = time.time()
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        print intersections[1].name
        intersections[1].run()
        #for ele in intersections:
        #    ele.run()

    traci.close()
    sumoProcess.wait()
    #sumoProcess.kill()
    #time2 = time.time()

    xmlfile = open("tripinfo" + str(port) + ".xml", 'r')
    xmlTree = ET.parse(xmlfile)
    treeRoot = xmlTree.getroot()
    totalSpeed = 0
    carNumber = len(treeRoot)
    for child in treeRoot:
        totalSpeed += float(child.attrib['routeLength'])/float(child.attrib['duration'])
    avgspeed = totalSpeed * 1.0 / carNumber

    xmlfile.close()
    os.remove("tripinfo" + str(port) + ".xml")

    time.sleep(30)
    print "sleeping at test--------"
    return avgspeed

if __name__ == '__main__':
    intersections = []
    CONFIG = [(1,2),(3,2),(2,1),(1,4), (1,2), (1,2), (1,5), (3,2), (3,3)]
    for ele in config.IntersectionList:
        intersection = Intersection(ele)
        intersection.loadFromData(config.IN_DATA)
        intersections.append(intersection)

    for idx in range(len(intersections)):
        intersections[idx].setThreshold(CONFIG[idx][0], CONFIG[idx][1])

    print mytest(intersections)
