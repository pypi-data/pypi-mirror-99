#!/usr/bin/python3

#
#   Developer : Alexey Zakharov (alexey.zakharov@vectioneer.com)
#   All rights reserved. Copyright (c) 2018 VECTIONEER.
#

from robot_control.motion_program import MotionProgram, \
    Waypoint, PoseTransformer
from robot_control.robot_command import RobotCommand
from robot_control.system_defs import States, \
    InterpreterEvents, InterpreterStates, StateEvents, ModeCommands, Modes
from robot_control import motionSL_pb2
import os
from math import radians

def init(motorcortex_types):
    path = os.path.dirname(motionSL_pb2.__file__)
    return motorcortex_types.load([{'proto': motionSL_pb2, 'hash': path + '/motionSL_hash.json'}])

def to_radians(degrees):
    return [radians(x) for x in degrees]