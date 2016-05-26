import sys
sys.path.append("/home/local/VANDERBILT/liy29/sumo-0.24.0/tools/")
import traci


class Direction(object):
    def __init__(self, name, lanes_num):
        self.name = name
        self.lanesNum = lanes_num
        self.lanesLengthList = []
        for i in range(self.lanesNum):
            self.lanesLengthList.append(0)

    def getQueueLength(self):
        if 0 == self.lanesNum:
            return 0
        return sum(self.lanesLengthList) #*1.0/len(self.lanesLengthList)

    def updateQueueLengthList(self):
        sensorTemp = '{edge_name}{idx}'
        for i in range(self.lanesNum):
            sensor = sensorTemp.format(edge_name = self.name, idx = str(i))
            self.lanesLengthList[i] = traci.areal.getLastStepVehicleNumber(sensor)



class Intersection(object):
    def __init__(self, name):
        self.name = name
        self.lightState = None
        self.lightPrivState = None

        # Light
        self.lightMax = 1200
        self.lightMin = 300
        self.defaultInterval = 900

        # WE
        self.weClock = 0
        self.weQueueLength = 0
        self.weGreens = ""
        self.weThreshold = 0

        # NS
        self.nsClock = 0
        self.nsQueueLength = 0
        self.nsGreens = ""
        self.nsThreshold = 0

        # Directions
        self.north = None
        self.south = None
        self.west = None
        self.east = None

    def setLightTime(self, lightMin, lightMax):
        self.lightMin = lightMin
        self.lightMax = lightMax

    def setLightEncode(self, nsGreen, weGreen):
        self.nsGreens = nsGreen
        self.weGreens = weGreen

    def getLightState(self):
        return traci.trafficlights.getRedYellowGreenState(self.name)

    def setLightState(self, ltState):
        traci.trafficlights.setRedYellowGreenState(self.name, ltState)

    def setLines(self, west_lanes_num, east_lanes_num, north_lanes_num, south_lanes_num):
        dString = "{name}S{direction}"
        self.west  = Direction(dString.format(name = self.name, direction = 'W'), west_lanes_num)
        self.east  = Direction(dString.format(name = self.name, direction = 'E'), east_lanes_num)
        self.north = Direction(dString.format(name = self.name, direction = 'N'), north_lanes_num)
        self.south = Direction(dString.format(name = self.name, direction = 'S'), south_lanes_num)

    def setThreshold(self, we, ns):
        self.weThreshold = we
        self.nsThreshold = ns

    def loadFromData(self, dataDict):

        dataList = dataDict[self.name]
        self.setLightEncode(dataList[0], dataList[1])
        self.setLines(dataList[2], dataList[3], dataList[4], dataList[5])

    def updateQueueLength(self):
        sensorString = "{name}S{direction}{lane}"
        self.west.updateQueueLengthList()
        self.east.updateQueueLengthList()
        self.north.updateQueueLengthList()
        self.south.updateQueueLengthList()
        self.nsQueueLength = self.north.getQueueLength() + self.south.getQueueLength()
        self.weQueueLength = self.west.getQueueLength() + self.east.getQueueLength()
#        print self.weQueueLength, self.nsQueueLength


    def updateClock(self):
        if self.lightState == self.nsGreens:
            self.nsClock += 1
            self.weClock = 0
        elif self.lightState == self.weGreens:
            self.weClock += 1
            self.nsClock = 0

    def init(self):
        if self.lightState == None:
            self.lightState = self.getLightState()
        assert self.lightState == self.nsGreens or self.lightState == self.weGreens

    def changeLight(self):
        if self.lightState == self.nsGreens:
            self.setLightState(self.weGreens)
            self.lightState = self.weGreens
        elif self.lightState == self.weGreens:
            self.setLightState(self.nsGreens)
            self.lightState = self.nsGreens

    def keepLight(self):
        self.setLightState(self.lightState)

    def controller(self):
        if ((self.weQueueLength < self.weThreshold and self.nsQueueLength < self.nsThreshold)\
                or (self.weQueueLength >= self.weThreshold and self.nsQueueLength >= self.nsThreshold))\
                and (self.weClock > self.lightMax or self.nsClock > self.lightMax):
            self.changeLight()

        elif (self.weQueueLength >= self.weThreshold and self.nsQueueLength < self.nsThreshold)\
                and (self.nsClock > self.lightMin or self.weClock > self.lightMax):
            self.changeLight()
 
        elif (self.nsQueueLength >= self.nsThreshold and self.weQueueLength < self.weThreshold)\
                and (self.weClock > self.lightMin or self.nsClock > self.lightMax):
            self.changeLight()

        else:
            self.keepLight()

    def defaultController(self):
        if self.weClock > self.defaultInterval or self.nsClock > self.defaultInterval:
            self.changeLight()

    def defaultRun(self):
        self.defaultController()
        self.updateClock()
        assert self.lightState == self.nsGreens or self.lightState == self.weGreens

    def fixRunSetColck(self, clock1, clock2):
        self.clock1 = clock1
        self.clock2 = clock2
        self.fixRun_mark = 1

    def fixRun(self):
        if 1 == self.fixRun_mark and (self.weClock > self.clock1 or self.nsClock > self.clock1):
            self.changeLight()
            self.fixRun_mark = 2
        elif 2 == self.fixRun_mark and (self.weClock > self.clock2 or self.nsClock > self.clock2):
            self.changeLight()
            self.fixRun_mark = 1
        else:
            self.keepLight()
        self.updateClock()

    def run(self):
        if self.nsThreshold == 0 and self.weThreshold == 0:
            self.defaultController()
            self.updateClock()
        else:
            self.updateQueueLength()
            self.controller()
            self.updateClock()

        assert self.lightState == self.nsGreens or self.lightState == self.weGreens


    def debug(self):
        print "ns:", self.nsQueueLength, '(', self.nsThreshold, ')'
        print self.north.lanesLengthList
        print "we:", self.weQueueLength, '(', self.weThreshold, ')'
        print self.south.lanesLengthList
        print "ns.clock:", self.nsClock
        print "we.clock:", self.weClock





