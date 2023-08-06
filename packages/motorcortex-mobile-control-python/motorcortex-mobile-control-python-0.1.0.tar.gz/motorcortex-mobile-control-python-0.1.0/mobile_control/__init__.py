#!/usr/bin/python3
#
#   Developer : Alexey Zakharov (alexey.zakharov@vectioneer.com)
#   All rights reserved. Copyright (c) 2021 VECTIONEER.
#

from mobile_control.mobile_platform import MobilePlatform
from mobile_control.position_mode import PositionMode
from mobile_control.velocity_mode import VelocityMode
from mobile_control.pose import Pose
from mobile_control.pose import Pose as Velocity
from mobile_control.system_defs import States, StateEvents, \
    Modes, ModeEvents, MotionGeneratorStates, TIMEOUT_INF
from math import radians

def toRadians(degrees):
    return [radians(x) for x in degrees]
