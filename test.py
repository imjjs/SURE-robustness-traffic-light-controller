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



def mytest(weThreshold, nsThreshold,
           intersections,
           intersectionIndex, procID, port):


    sumoProcess = subprocess.Popen(
        ["sumo", "-c", "VanderbiltCampus/Vanderbilt.sumo.cfg", "--tripinfo-output", "tripinfo" + str(procID) + ".xml",
         "--remote-port", str(port)], stdout= config.DEVNULL, stderr= config.DEVNULL)
    time.sleep(30)
    traci.init(port)

    ins = intersections[intersectionIndex]
    ins.setThreshold(weThreshold, nsThreshold)


    #time1 = time.time()
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        for ele in intersections[0:intersectionIndex + 1]:
            ele.run()
        for ele in intersections[intersectionIndex + 1:]:
            ele.defaultRun()

    traci.close()
    sumoProcess.wait()
    sumoProcess.kill()
    #time2 = time.time()

    xmlfile = open("tripinfo" + str(procID) + ".xml", 'r')
    xmlTree = ET.parse(xmlfile)
    treeRoot = xmlTree.getroot()
    totalSpeed = 0
    carNumber = len(treeRoot)
    for child in treeRoot:
        totalSpeed += float(child.attrib['routeLength'])/float(child.attrib['duration'])
    avgspeed = totalSpeed * 1.0 / carNumber

    xmlfile.close()
    os.remove("tripinfo" + str(procID) + ".xml")

    time.sleep(30)
    print "sleeping at test--------"
    return avgspeed , weThreshold, nsThreshold
    
if __name__ == '__main__':
    intersections = []
    main.generator_ports()
    for ele in config.IntersectionList:
        intersection = Intersection(ele)
        intersection.loadFromData(config.IN_DATA)
        intersections.append(intersection)
        
    print mytest(2, 2, intersections, 0, 41003)
