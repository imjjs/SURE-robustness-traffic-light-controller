import os

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
    "202407913": ["GGGggGGGGgrrrr", "rrrrrrrrrrGGGG", 0, 2, 3, 3]#
}

IntersectionList2 = ["202514063", "202305800", "202514074", "202514078", "3010263944", "1443088101", "202270699"]
IntersectionList = ['1443088096', '1443088101', '202514078', '3010263944', '202407913', '202514074', '202305800', '202514063', '202270699']
DEVNULL = open(os.devnull, "w")
