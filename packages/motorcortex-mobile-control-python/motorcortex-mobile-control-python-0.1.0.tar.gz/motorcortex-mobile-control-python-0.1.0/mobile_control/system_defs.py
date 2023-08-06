#!/usr/bin/python3

#
#   Developer : Alexey Zakharov (alexey.zakharov@vectioneer.com)
#   All rights reserved. Copyright (c) 2017 VECTIONEER.
#
from enum import Enum


class States(Enum):
    """List of states of the mobile platform"""
    INIT_S = 0
    OFF_S = 1
    ENGAGED_S = 4
    FREEZE_S = 6
    ESTOP_S = 7
    SHUTDOWN_S = 8

    IDLE_S = 10

    TO_OFF_T = 111
    TO_SHUTDOWN_T = 888
    OFF_TO_IDLE_T = 1010

    IDLE_TO_ENGAGED_T = 1004
    ENGAGED_TO_IDLE_T = 4010

    RESET_ESTOP_T = 701

    MOBILITY_TRANSITION_S = 255


class StateEvents(Enum):
    """List of events of the mobile platform state machine"""
    EMPTY = 0
    GOTO_OFF = 1
    GOTO_IDLE = 2
    GOTO_ENGAGE = 6
    CALIBRATE = 8
    ACKNOWLEDGE = 255


class Modes(Enum):
    """List of modes of the mobile platform"""
    INIT = 0
    VELOCITY = 1
    POSITION = 2


class ModeEvents(Enum):
    """List of mode events of the mobile platform"""
    EMPTY = 0
    GOTO_VELOCITY = 1
    GOTO_POSITION = 2


class MotionGeneratorStates(Enum):
    """List of states of the motion generator"""
    IDLE = 0
    VELOCITY_MOVE = 1
    POSITION_MOVE = 2


TIMEOUT_INF = float("inf")
