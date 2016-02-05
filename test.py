import traci
import subprocess
import config
import os
from intersection import Intersection
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def mytest(weThreshold, nsThreshold,
           intersections,
           intersectionIndex, port):

    sumoProcess = subprocess.Popen(
        ["sumo", "-c", "VanderbiltCampus/Vanderbilt.sumo.cfg", "--tripinfo-output", "tripinfo" + str(port)+ ".xml",
         "--remote-port", str(port)], stdout= config.DEVNULL, stderr= config.DEVNULL)
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

    xmlfile = open("tripinfo" + str(port) + ".xml", 'a')
    xmlTree = ET.parse(xmlfile)
    treeRoot = xmlTree.getroot()
    totalSpeed = 0
    carNumber = len(treeRoot)
    for child in treeRoot:
        totalSpeed += float(child.attrib['routeLength'])/float(child.attrib['duration'])
    avgspeed = totalSpeed * 1.0 / carNumber

    xmlfile.close()
    os.remove("tripinfo" + str(port) + ".xml")
    return avgspeed , weThreshold, nsThreshold
    
if __name__ == '__main__':
    intersections = []
    for ele in config.IntersectionList:
        intersection = Intersection(ele)
        intersection.loadFromData(config.IN_DATA)
        intersections.append(intersection)
        
    mytest(30, 30, intersections, 0, 8431)
