import traci
import subprocess
import config
from intersection import Intersection


def mytest(weThreshold, nsThreshold,
           intersections,
           intersectionIndex, port):

    sumoProcess = subprocess.Popen(
        ["/opt/local/bin/sumo", "-c", "VanderbiltCampus/Vanderbilt.sumo.cfg", "--tripinfo-output", "tripinfo" + str(port)+ ".xml",
         "--remote-port", str(port)], stdout= config.DEVNULL, stderr= config.DEVNULL)
    traci.init(port)
    print "sumostart"
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
    print "sumoclose"
    #time2 = time.time()
    # print "weThreshold ={we}, nsThreshold = {ns}, avgLatency = {avg}".format(we = weThreshold, ns = nsThreshold, avg = avgLatency)
    return "tripinfo" + str(port) + ".xml", weThreshold, nsThreshold
    
if __name__ == '__main__':
    intersections = []
    for ele in config.IntersectionList:
        intersection = Intersection(ele)
        intersection.loadFromData(config.IN_DATA)
        intersections.append(intersection)
        
    mytest(30, 30, intersections, 0, 8431)
