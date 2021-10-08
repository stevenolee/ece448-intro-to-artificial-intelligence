
# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *

def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.
    
        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """ 
    arm_copy = arm
    # find number of columns and rows
    arm_limit = arm_copy.getArmLimit()
    num_rows = int((arm_limit[0][1] - arm_limit[0][0])/granularity + 1)
    num_cols = int((arm_limit[1][1] - arm_limit[1][0])/granularity + 1)

    input_map = [[SPACE_CHAR] * num_cols for y in range(num_rows)] 

    # get angle ranges
    arm_limits = arm_copy.getArmLimit()
    alpha_limits = arm_limits[0]
    beta_limits = arm_limits[1]

    # mark starting point
    initial_angles = arm_copy.getArmAngle()
    min_angles = (alpha_limits[0], beta_limits[0])
    start_pos = angleToIdx(initial_angles, min_angles, granularity)
 
    input_map[start_pos[0]][start_pos[1]] = START_CHAR
    objectives = []

    temp_obstacles = obstacles
    temp_obstacles.extend(goals)

    
    # map = []
    # curr_row = 0

    # # mark objectives
    # for alpha in range (alpha_limits[0], alpha_limits[1] + 1, granularity):
    #     inner_array = []
    #     for beta in range (beta_limits[0], beta_limits[1] + 1, granularity):
    #         arm_copy.setArmAngle((alpha, beta))
    #         arm_pos = arm_copy.getArmPos()
    #         curr_coordinate = angleToIdx((alpha, beta), min_angles, granularity)
            
    #         if ((doesArmTouchObstacles(arm_pos, obstacles) and not doesArmTouchGoals(arm_copy.getEnd(), goals)) or not isArmWithinWindow(arm_pos, window)):
    #             # input_map[curr_coordinate[0]][curr_coordinate[1]] = WALL_CHAR
    #             inner_array.append(WALL_CHAR)

    #         elif (doesArmTouchGoals(arm_copy.getEnd(), goals)):
    #             # input_map[curr_coordinate[0]][curr_coordinate[1]] = OBJECTIVE_CHAR
    #             inner_array.append(OBJECTIVE_CHAR)
    #             objectives.append((curr_coordinate[0], curr_coordinate[1]))

    #         else:
    #             inner_array.append(SPACE_CHAR)
                
    #     map.append(inner_array)
            

    for x in range (num_rows):
        for y in range (num_cols):
            angles = idxToAngle((x, y), min_angles, granularity)
            alpha = angles[0]
            beta = angles[1]
            arm_copy.setArmAngle((alpha, beta))
            arm_pos = arm_copy.getArmPos()
            # curr_coordinate = angleToIdx((alpha, beta), min_angles, granularity)
            
            if ((doesArmTouchObstacles(arm_pos, obstacles) and not doesArmTouchGoals(arm_copy.getEnd(), goals)) or not isArmWithinWindow(arm_pos, window)):
                input_map[x][y] = WALL_CHAR

            elif (doesArmTouchGoals(arm_copy.getEnd(), goals)):
                input_map[x][y] = OBJECTIVE_CHAR
                objectives.append((x, y))

    # map[start_pos[0]][start_pos[1]] = START_CHAR
    # maze = Maze(map, min_angles, granularity)

    maze = Maze(input_map, min_angles, granularity)
    # maze.setStart(start_pos)
    # maze.setObjectives(objectives)
    maze.saveToFile("maze_output.txt")

    return maze