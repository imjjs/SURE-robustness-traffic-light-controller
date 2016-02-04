import xml.etree.ElementTree as ET
import os
import re

import config


class XmlBlock(object):
    def __init__(self, name, n, e, s, w):
        self.name = name
        self.n = n
        self.e = e
        self.s = s
        self.w = w
        self.xmlLineList = []

    def addXmlLine(self, line):
        self.xmlLineList.append(line)

    def output(self):
        head = '<!--   w = {w},  e = {e}, n = {n}, s = {s} -->'
        out = ''
        out += head.format(w = str(self.w), e = str(self.e), n = str(self.n), s = str(self.s))
        out += '\n'
        for i in self.xmlLineList:
            out += i.output()
            out += '\n'
        return out

class XmlLine(object):
    def __init__(self, name, lane):
        self.name = name
        self.lane = lane

    def setPos(self, l):
        length = float(l)
        if length >= 80:
            self.pos = length - 50
        else:
            self.pos = length / 2

    def getlane(self):
        return self.lane

    def output(self):
        temp =   '<e2Detector id="{name}" lane="{lane}" length="80" pos="{pos}"  freq="1" file="dsc.out" friendlyPos="true"/>'
        return temp.format(name = self.name, lane = self.lane, pos = self.pos)

def getLength(lane_name, xmlroot):
    reg = re.compile(r'(.+?)_\d')
    road = reg.match(lane_name).group(1)
    for ele in xmlroot:
        if 'edge' != ele.tag:
            continue
        if ele.attrib['id'] != road:
            continue
        for ele2 in ele:
            if 'lane' != ele2.tag:
                continue
            if ele2.attrib['id'] != lane_name:
                continue
            return ele2.attrib['length']

if __name__ == '__main__':
    f = os.path.join('VanderbiltCampus', 'Vanderbilt.net.xml')
    a = ET.ElementTree(file = f)
    root = a.getroot()
    reg = re.compile(r'(.+?)_\d')
    direction = ['N', 'E', 'S', 'W']

    xmlBlockList = []
    for ele in root:
        if 'junction' != ele.tag:
            continue
        if ele.attrib['id'] not in config.IntersectionList:
            continue

        id = ele.attrib['id']
        lanesString = ele.attrib['incLanes']
        lanesList = lanesString.split(' ')
        lanesDict = {}
        idx = 0

        prevName = reg.match(lanesList[0]).group(1)
        count = 0
        for lane in lanesList:
            laneName = reg.match(lane).group(1)
            if laneName == prevName:
                count += 1
            else:
                lanesDict[direction[idx]] = (prevName, count,)
                count = 1
                prevName = laneName
                idx += 1
        assert idx < 4
        lanesDict[direction[idx]] = (prevName, count,)
        for i in range(idx + 1, 4):
            lanesDict[direction[i]] = (None, 0)
        #TODO: when #direction < 4, the direction of each lane maybe wrong
        xmlBlock = XmlBlock(id, lanesDict['N'][1], lanesDict['E'][1], lanesDict['S'][1], lanesDict['W'][1])
        lanenameString = '{junctionId}S{direction}{idx}'
        for k in lanesDict:
            v1, v2 = lanesDict[k]
            num = v2
            for i in range(num):
                xmlLine = XmlLine(lanenameString.format(junctionId = id, direction = k, idx = i), v1 + '_' + str(i))
                xmlLine.setPos(getLength(xmlLine.getlane(), root))
                #TODO: setpos
                xmlBlock.addXmlLine(xmlLine)
        print xmlBlock.output()

