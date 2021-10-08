# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains geometry functions that relate with Part1 in MP2.
"""

import math
import numpy as np
from const import *


def computeCoordinate(start, length, angle):
    """Compute the end cooridinate based on the given start position, length and angle.

        Args:
            start (tuple): base of the arm link. (x-coordinate, y-coordinate)
            length (int): length of the arm link
            angle (int): degree of the arm link from x-axis to couter-clockwise

        Return:
            End position of the arm link, (x-coordinate, y-coordinate)
    """
    radians = math.radians(angle)
    if angle == 90:
        return (start[0], start[1] - length)

    x = math.cos(radians) * length
    y = math.sin(radians) * length

    return (start[0] + x, start[1] - y)


def doesArmTouchObstacles(armPos, obstacles):
    """Determine whether the given arm links touch obstacles

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            obstacles (list): x-, y- coordinate and radius of obstacles [(x, y, r)]

        Return:
            True if touched. False it not.
    """

    for element in armPos:
        start_point = element[0]
        end_point = element[-1]

        for obst in obstacles:
            center = (obst[0], obst[1])
            radius = obst[2]
            d = (end_point[0] - start_point[0], end_point[1] - start_point[1])
            f = (start_point[0] - center[0], start_point[1] - center[1])
            x = np.dot(d, d)
            y = 2 * np.dot(f, d)
            z = np.dot(f, f) - radius ** 2
            disc = y ** 2 - 4 * x * z

            if (disc < 0):
                continue

            else:
                disc = math.sqrt(disc)
                t1 = (-y - disc)/(2*x)
                t2 = (-y + disc)/(2*x)

                if t1 >= 0 and t1 <= 1:
                    return True

                if t2 >= 0 and t2 <= 1:
                    return True
    return False



def doesArmTouchGoals(armEnd, goals):
    """Determine whether the given arm links touch goals

        Args:
            armEnd (tuple): the arm tick position, (x-coordinate, y-coordinate)
            goals (list): x-, y- coordinate and radius of goals [(x, y, r)]

        Return:
            True if touched. False it not.
    """
    for element in goals:
        dist = math.sqrt((element[0] - armEnd[0]) **2 + (element[1] - armEnd[1])**2)
        if dist <= element[2]:
            return True

    return False


def isArmWithinWindow(armPos, window):
    """Determine whether the given arm stays in the window

        Args:
            armPos (list): start and end position of all arm links [(start, end)]
            window (tuple): (width, height) of the window

        Return:
            True if all parts are in the window. False it not.
    """
    for element in armPos:
        start = element[0] 
        end = element[1]
        width = window[0]
        height = window[1]
        if ((start[0] < 0 or start[0] > width) or (start[1] < 0 or start[1] > height))  \
            or ((end[0] < 0 or end[0] > width) or (end[1] < 0 or end[1] > height)):
            return False
    return True
