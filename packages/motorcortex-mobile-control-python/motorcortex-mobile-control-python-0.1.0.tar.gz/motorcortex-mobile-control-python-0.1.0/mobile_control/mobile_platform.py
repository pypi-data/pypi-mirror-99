#!/usr/bin/python3

#
#   Developer : Alexey Zakharov (alexey.zakharov@vectioneer.com)
#   All rights reserved. Copyright (c) 2021 VECTIONEER.
#

from .system_defs import TIMEOUT_INF, Modes, States, ModeEvents, StateEvents


class MobilePlatform(object):
    LOGIC_STATE_COMMAND = "root/Logic/stateCommand"
    LOGIC_MODE_COMMAND = "root/Logic/modeCommand"
    LOGIC_STATE = "root/Logic/state"
    LOGIC_MODE = "root/Logic/mode"

    def __init__(self, req):
        self.__req = req

    def engage(self, timeout_sec=TIMEOUT_INF):
        self.__req.setParameter(MobilePlatform.LOGIC_STATE_COMMAND, StateEvents.GOTO_ENGAGE.value).get()
        return self.switchToLogicState(self.__req, timeout_sec, States.ENGAGED_S, "Engage state")

    def idle(self, timeout_sec=TIMEOUT_INF):
        self.__req.setParameter(MobilePlatform.LOGIC_STATE_COMMAND, StateEvents.GOTO_IDLE.value).get()
        return self.switchToLogicState(self.__req, timeout_sec, States.IDLE_S, "Idle state")

    def off(self, timeout_sec=TIMEOUT_INF):
        self.__req.setParameter(MobilePlatform.LOGIC_STATE_COMMAND, StateEvents.GOTO_OFF.value).get()
        return self.switchToLogicState(self.__req, timeout_sec, States.OFF_S, "Off state")

    def acknowledge(self, timeout_sec=TIMEOUT_INF):
        return False

    def velocityMode(self, timeout_sec=TIMEOUT_INF):
        self.__req.setParameter(MobilePlatform.LOGIC_MODE_COMMAND, ModeEvents.GOTO_VELOCITY.value).get()
        return self.switchToLogicMode(self.__req, timeout_sec, Modes.VELOCITY, "Direct Velocity mode")

    def positionMode(self, timeout_sec=TIMEOUT_INF):
        self.__req.setParameter(MobilePlatform.LOGIC_MODE_COMMAND, ModeEvents.GOTO_POSITION.value).get()
        return self.switchToLogicMode(self.__req, timeout_sec, Modes.POSITION, "Position mode")

    def getMode(self, timeout_sec=TIMEOUT_INF):
        return self.__req.getParameter(MobilePlatform.LOGIC_STATE).get().value

    def getMode(self, timeout_sec=TIMEOUT_INF):
        return self.__req.getParameter(MobilePlatform.LOGIC_MODE).get().value

    def switchToLogicState(self, req, timeout_sec, desired_state, state_name):
        while True:
            logic_state = self.__req.getParameter(MobilePlatform.LOGIC_STATE).get().value[0]
            if States(logic_state) == States.ESTOP_S:
                return False
            if timeout_sec < 0:
                return False
            if States(logic_state) == desired_state:
                break

        return True

    def switchToLogicMode(self, req, timeout_sec, desired_mode, mode_name):
        while True:
            rep = self.__req.getParameterList([MobilePlatform.LOGIC_MODE,
                                               MobilePlatform.LOGIC_STATE]).get()
            logic_mode = rep.params[0].value[0]
            logic_state = rep.params[1].value[0]
            if States(logic_state) != States.ENGAGED_S:
                return False
            if timeout_sec < 0:
                return False
            if Modes(logic_mode) == desired_mode:
                break

        return True
