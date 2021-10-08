import queue
from util import *
# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
# 
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod, [])(maze)


def backtrace(start, goal, parents):
    if start == goal:
        return [start]
    # print("start: ", start, " goal: ", goal, "\n")
    traceback = goal
    final_path = []
    while True:
        # print(traceback)
        final_path.insert(0, traceback)
        traceback = parents[traceback[0]][traceback[1]]
        if traceback == start:
            final_path.insert(0, start)
            return final_path


def bfs(maze):
    # TODO: Write your code here 
    dimensions = maze.getDimensions()
    x_max = dimensions[1]
    y_max = dimensions[0]

    start = angleToIdx(maze.getStart(), maze.offsets, maze.granularity)
    goal = maze.getObjectives()
    # frontier of bfsx
    paths = queue.Queue()
    # boolean value at each coordinate stores whether or not it has been traversed
    visited = [[False for x in range(x_max)] for y in range(y_max)] 
    # value at each coordinate stores the coordinates of the parent (the original neighbor)
    parents = [[(None, None) for x in range(x_max)] for y in range(y_max)]
    parents[0][0] = (-1, -1)

    # push start position onto queue
    paths.put(start)
    visited[start[0]][start[1]] = True
    current_position = start
    found = False

    while not paths.empty():
        # pop off queue
        current_position = paths.get()

        angles = idxToAngle(current_position, maze.offsets, maze.granularity)
        if maze.isObjective(angles[0], angles[1]):
            found = True
            break

        # if neighbors have not been traversed, add them to the queue
        neighbors = maze.getNeighbors(angles[0], angles[1])
        for coordinate in neighbors:
            idx_coordinate = angleToIdx(coordinate, maze.offsets, maze.granularity)
            x = idx_coordinate[0]
            y = idx_coordinate[1]
            if not maze.isWall(coordinate[0], coordinate[1]) and not visited[x][y]:
                paths.put(idx_coordinate)
                visited[x][y] = True
                parents[x][y] = current_position
        visited[current_position[0]][current_position[1]] = True
        
    converted_retval = []
    if found:
        retval = backtrace(start, current_position, parents)
        for element in retval:
            converted_retval.append(idxToAngle(element, maze.offsets, maze.granularity))        
    return converted_retval, 0

def dfs(maze):
    # TODO: Write your code here    
    return [], 0

def greedy(maze):
    # TODO: Write your code here    
    return [], 0

def astar(maze):
    # TODO: Write your code here    
    return [], 0