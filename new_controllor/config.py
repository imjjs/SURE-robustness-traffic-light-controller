class Param(object):
    def __init__(self, _controller, _phase):
        self.controller = _controller
        self.phase = _phase

    def __str__(self):
        return 'controller:' + self.controller + ', phase:' + str(self.phase)

ignore_sensors = []
blue = ["Controller1443088096", "Controller202305800", "Controller202407913", "Controller202514063", "Controller202514074"]
red = ["Controller1443088101", "Controller202270699", "Controller202514078", "Controller3010263944"]

morning_opt = [5, 0, 17, 1, 0, 0, 0, 13, 0, 26, 8, 3, 7, 19, 0, 26, 1, 20, 0]
afternoon_opt =[3, 9, 18, 4, 4, 0, 22, 16, 10, 29, 30, 13, 6, 15, 6, 26, 6, 26, 8]
night_opt = [1, 1, 2, 0, 0, 0, 2, 4, 2, 2, 8, 11, 0, 1, 1, 0, 1, 3, 0]

morning_opt1 = [0, 0, 20, 0, 0, 0, 0, 5, 0, 0, 0, 30, 4, 6, 3, 30, 14, 24, 14]
morning_opt2 = [0, 0, 27, 1, 0, 0, 9, 7, 3, 19, 18, 28, 4, 0, 3, 22, 1, 23, 11]
morning_opt5 = [0, 0, 27, 2, 2, 0, 10, 1, 0, 21, 24, 15, 0, 9, 0, 27, 30, 11, 7]
