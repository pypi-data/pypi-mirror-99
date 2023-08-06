"""
Wave generator functionality:
- Various wave functions: square, sine, triangular etc.
- Function time_to_angle: conversion function elapsed time -> angle
- Function wave_custom: for custom waves

2020, September 5

"""

import math


def time_to_angle(time, frequency, phase=0):
    """
    Convert an elapsed time to an angle.
    Designed to be used with the wave functions
    that take an anle as input.

    :param time: elapsed time, in s
    :param frequency: frequency, in Hz
    :param phase: phase offset, in radians
    :return: angle, in radians
    """
    return ((time*frequency + phase/(2*math.pi)) % 1) * 2*math.pi


# Some wave functions
# Input range is [0, 2*pi] and output range is [-1, 1].
# These functions are static and thus can be placed outside of the class definition.
def unity(angle):
    return 1


def sine(angle):
    return math.sin(angle)


def square(angle):
    if angle <= math.pi:
        return 1
    else:
        return -1


def triangle(angle):
    if angle <= math.pi / 2:
        value = angle * 2 / math.pi
    elif angle > math.pi * 3 / 2:
        value = -4 + angle * 2 / math.pi
    else:
        value = 2 - angle * 2 / math.pi
    return value


def sawtooth(angle):
    return 1 - angle / math.pi
