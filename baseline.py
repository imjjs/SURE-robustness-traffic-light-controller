import subprocess
import traci
import config
from intersection import Intersection
import os
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

port = 8431
if __name__ == '__main__':
    sumoProcess = subprocess.Popen(
        ["sumo", "-c", "VanderbiltCampus/Vanderbilt.sumo.cfg", "--tripinfo-output", "tripinfo" + str(port) + ".xml",
         "--remote-port", str(port)], stdout= config.DEVNULL, stderr = config.DEVNULL)

    traci.init(port)


    intersections = []
    for ele in config.IntersectionList:
        intersection = Intersection(ele)
        intersection.loadFromData(config.IN_DATA)
        intersections.append(intersection)


    #time1 = time.time()
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        for ele in intersections:
            ele.defaultRun()

    traci.close()
    sumoProcess.wait()
    sumoProcess.kill()
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

    print avgspeed