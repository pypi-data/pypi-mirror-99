#!/usr/bin/python3

#
#   Developer : Alexey Zakharov (alexey.zakharov@vectioneer.com)
#   All rights reserved. Copyright (c) 2021 VECTIONEER.
#

class Pose(object):
    def __str__(self):
        return f'X: {self.x()} Y: {self.y()}, RZ: {self.rz()}'
    def __init__(self, c1, c2, c3=None):
        self.__x = c1
        if c3:
            self.__y = c2
            self.__rz = c3
        else:
            self.__y = 0
            self.__rz = c2

    def x(self):
        return self.__x

    def y(self):
        return self.__y

    def rz(self):
        return self.__rz

    def almostEqual(self, pose, tolerance=[0.1, 0.1, 0.1]):
        return False
