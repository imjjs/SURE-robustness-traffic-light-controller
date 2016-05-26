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

import log
import time


def simulationProcess(weThreshold, nsThreshold, paraList, intersection_name, intersectionIndex, sumoMap):
    port = config.generator_ports()
    sumoProcess = subprocess.Popen(
        ["sumo", "-c", sumoMap, "--tripinfo-output", "tripinfo" + str(port) + ".xml",
         "--remote-port", str(port)], stdout= config.DEVNULL, stderr = config.DEVNULL)
    time.sleep(10)

    traci.init(port)
    intersections = config.generator_intersectionList(intersection_name, paraList)
    ins = intersections[intersectionIndex]
    ins.setThreshold(weThreshold, nsThreshold)

    for ele in intersections:
        ele.init()

    #time1 = time.time()
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        for ele in intersections:
            ele.run()
#        for ele in intersections[intersectionIndex + 1:]:
#            ele.defaultRun()

    traci.close()
    sumoProcess.wait()
    time.sleep(10)

    return durationAndDistance(port)



def mytest(weThreshold, nsThreshold,
           paraList, intersection_name,
           intersectionIndex, sumoMaps):
    totalDistance = 0
    totalDuration = 0

    for map in sumoMaps:
        distance,duration=0.0,0.0
        while True:
            try:
                distance, duration = simulationProcess(weThreshold, nsThreshold, paraList, intersection_name, intersectionIndex, map)
            except Exception , e:
                print e
                continue
            break
        totalDistance += distance
        totalDuration += duration
    log.log(totalDistance/totalDuration)
    return totalDistance/totalDuration, weThreshold, nsThreshold


def avgDuration(port):
    xmlfile = open("tripinfo" + str(port) + ".xml", 'r')
    xmlTree = ET.parse(xmlfile)
    treeRoot = xmlTree.getroot()
    totalDuration = 0
    carNumber = len(treeRoot)
    for child in treeRoot:
        totalDuration += float(child.attrib['duration'])
    res = totalDuration * 1.0 / carNumber

    xmlfile.close()
    os.remove("tripinfo" + str(port) + ".xml")

    return res

def durationAndDistance(port):
    xmlfile = open("tripinfo" + str(port) + ".xml", 'r')
    xmlTree = ET.parse(xmlfile)
    treeRoot = xmlTree.getroot()
    totalDuration = 0
    totalDistance = 0
    carNumber = len(treeRoot)
    for child in treeRoot:
        totalDuration += float(child.attrib['duration'])
        totalDistance += float(child.attrib['routeLength'])
    xmlfile.close()
    os.remove("tripinfo" + str(port) + ".xml")
    return totalDistance, totalDuration


def avgSpeed(port):
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

    return avgspeed

if __name__ == '__main__':
    config.LogTime = time.time()
    paraList = [(0,0), (0,0), (0,0), (0,0), (0,0)]
    print mytest(1, 1, paraList, config.CompareList, 0, config.sumoMaps)
