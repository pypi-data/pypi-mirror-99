#!/usr/bin/python3

#
#   Developer : Alexey Zakharov (alexey.zakharov@vectioneer.com)
#   All rights reserved. Copyright (c) 2021 VECTIONEER.
#

import time


class VelocityMode(object):
    TARGET_VELOCITY = "root/Control/hostInTargetVelocity"
    ACTUAL_VELOCITY_POLAR = "root/Control/VelocityIntegrator/velocityOutPolar"
    ACTUAL_VELOCITY_CARTESIAN = "root/Control/VelocityIntegrator/velocityOut"
    SHORT_SLEEP_SEC = 0.01

    def __init__(self, req):
        self.__req = req

    def setVelocity(self, vel, timeout_sec=0):
        if timeout_sec == 0:
            return self.__req.setParameter(VelocityMode.TARGET_VELOCITY, [vel.x(), vel.y(), vel.rz()])

        status = None
        while timeout_sec > 0:
            t0 = time.time()
            status = self.__req.setParameter(VelocityMode.TARGET_VELOCITY, [vel.x(), vel.y(), vel.rz()])
            t1 = time.time()
            timeout_sec -= (t1 - t0)
            if timeout_sec >= 0:
                time.sleep(VelocityMode.SHORT_SLEEP_SEC)
                timeout_sec -= VelocityMode.SHORT_SLEEP_SEC

        return status

    def getTargetVelocity(self):
        return self.__req.getParameter(VelocityMode.TARGET_VELOCITY).get().value

    def getActualVelocity(self):
        return self.__req.getParameter(VelocityMode.ACTUAL_VELOCITY_POLAR).get().value
