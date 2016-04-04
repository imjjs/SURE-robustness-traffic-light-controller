import os
from threading import Lock
import socket
import intersection

PORT_LOCK = Lock()



def get_open_port(howMany=1):
    """Return a list of n free port numbers on localhost"""
    results = []
    sockets = []
    i=0
    while i < howMany:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        # work out what the actual port number it's bound to is
        addr, port = s.getsockname()
        if port < 40000:
            s.close()
            continue
        results.append(port)
        sockets.append(s)
        i += 1
    for s in sockets:
        s.close()

    return results

def generator_ports():
    PORT_LOCK.acquire()
    ports = get_open_port(1)
    PORT_LOCK.release()
    return ports[0]


def generator_intersectionList(intersection_names, paraList):
    ret = []
    for name in intersection_names:
        ins = intersection.Intersection(name)
        ins.loadFromData(IN_DATA)
        ret.append(ins)
    assert len(ret) == len(paraList)

    for idx in range(len(ret)):
        ret[idx].setThreshold(paraList[idx][0], paraList[idx][1])
    return ret

sumoMaps = [
    os.path.join('VanderbiltCampus','Vanderbilt.sumo (1).cfg'),
    os.path.join('VanderbiltCampus','Vanderbilt.sumo (2).cfg'),
    os.path.join('VanderbiltCampus','Vanderbilt.sumo (3).cfg'),
    os.path.join('VanderbiltCampus','Vanderbilt.sumo (4).cfg'),
    os.path.join('VanderbiltCampus','Vanderbilt.sumo (5).cfg'),
    os.path.join('VanderbiltCampus','Vanderbilt.sumo (6).cfg'),
    os.path.join('VanderbiltCampus','Vanderbilt.sumo (7).cfg'),
    os.path.join('VanderbiltCampus','Vanderbilt.sumo (8).cfg'),
 #   os.path.join('VanderbiltCampus','Vanderbilt.sumo (9).cfg'),
 #   os.path.join('VanderbiltCampus','Vanderbilt.sumo (10).cfg'),
]


# NS_GREEN, WE_GREEN, w, e, n, s
# WE_RED, NS_Red
IN_DATA = {
    "1443088101": ["GGGggrrrrGGGggrrrr", "rrrrrGGggrrrrrGGgg", 3, 2, 2, 2],#
    "202270699": ["GGGGgrrrGGGggrrr", "rrrrrGGgrrrrrGgg", 1, 2, 3, 3],
    "202514063": ["GGGGggrrrrGGGGggrrrr", "rrrrrrGGggrrrrrrGGgg", 2, 1, 3, 3],#
    "202305800": ["GGGGggrrrrGGGGggrrrr", "rrrrrrGGggrrrrrrGGgg", 1, 1, 3, 3],#
    "202514074": ["GGGrrrrGgGrrrr", "rrGGGGgrrGGGGg", 3, 3, 2, 2],#
    "202514078": ["GGGGggrrrrGGGGggrrrr", "rrrrrrGGggrrrrrrGGgg", 1, 2, 3, 3],#
    "3010263944": ["GGggrrrrrGGggrrrrr", "rrrrGGGggrrrrGGGgg", 2, 2, 2, 2],#
    "1443088096": ["GGGGggrrGGGGggrrrr", "GrrrrrGGrrrrrrGGgg", 1, 2, 3, 3],#
    "202407913": ["GGGggGGGGgrrrr", "rrrrrrrrrrGGGG", 0, 2, 3, 3],#
    "IK" :["Grr", "rGG", 2, 0, 1, 0],
    "LJ" :["Grr", "rGG", 2, 0, 1, 0],
    "GD" :["Grr", "rGG", 2, 0, 1, 0],
    "FH" :["Grr", "rGG", 2, 0, 1, 0],
    "AC" :["GGrr", "rrGG", 2, 0, 2, 0],
}

smallMap = ['IK', 'LJ', 'GD', 'FH', 'AC']
CompareList = ['1443088096','1443088101','202514078','3010263944','202407913']
IntersectionList2 = ["202514063", "202305800", "202514074", "202514078", "3010263944", "1443088101", "202270699"]
IntersectionList = ['1443088096', '1443088101', '202514078', '3010263944', '202407913', '202514074', '202305800', '202514063', '202270699']
DEVNULL = open(os.devnull, "w")
