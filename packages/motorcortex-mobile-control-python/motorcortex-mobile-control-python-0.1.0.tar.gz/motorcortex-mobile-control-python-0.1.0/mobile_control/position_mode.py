#!/usr/bin/python3

#
#   Developer : Alexey Zakharov (alexey.zakharov@vectioneer.com)
#   All rights reserved. Copyright (c) 2021 VECTIONEER.
#

from .pose import Pose

class PositionMode(object):
    GLOBAL_POSE = "root/Control/globalPositionOut"

    def __init__(self, req):
        self.__req = req

    def getGlobalPose(self):
        return Pose(self.__req.getParameter(PositionMode.GLOBAL_POSE).get().value[0],
                    self.__req.getParameter(PositionMode.GLOBAL_POSE).get().value[1],
                    self.__req.getParameter(PositionMode.GLOBAL_POSE).get().value[2])
