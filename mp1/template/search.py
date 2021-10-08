# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,extra)

import queue

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "astar": astar,
        "astar_multi": astar_multi,
        "extra": extra,
    }.get(searchMethod)(maze)


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
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here

    dimensions = maze.getDimensions()
    x_max = dimensions[1]
    y_max = dimensions[0]

    start = maze.getStart()
    goal = maze.getObjectives()[0]
    # frontier of bfs
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

    while current_position != goal:
        # pop off queue
        current_position = paths.get()

        # if neighbors have not been traversed, add them to the queue
        neighbors = maze.getNeighbors(current_position[0], current_position[1])
        for coordinate in neighbors:
            x = coordinate[0]
            y = coordinate[1]
            if visited[x][y] == False:
                paths.put(coordinate)
                visited[x][y] = True
                parents[x][y] = current_position

    return backtrace(start, goal, parents)


def dfs(maze):
    """
    Runs DFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here

    dimensions = maze.getDimensions()
    x_max = dimensions[1]
    y_max = dimensions[0]

    start = maze.getStart()
    goal = maze.getObjectives()[0]
    # frontier of bfs
    paths = []
    # boolean value at each coordinate stores whether or not it has been traversed
    visited = [[False for x in range(x_max)] for y in range(y_max)] 
    # value at each coordinate stores the coordinates of the parent (the original neighbor)
    parents = [[(None, None) for x in range(x_max)] for y in range(y_max)]
    parents[0][0] = (-1, -1)

    # push start position onto queue
    paths.append(start)
    visited[start[0]][start[1]] = True
    current_position = start

    while current_position != goal:
        # pop off queue
        current_position = paths.pop()

        # if neighbors have not been traversed, add them to the queue
        neighbors = maze.getNeighbors(current_position[0], current_position[1])
        for coordinate in neighbors:
            x = coordinate[0]
            y = coordinate[1]
            if visited[x][y] == False:
                paths.append(coordinate)
                visited[x][y] = True
                parents[x][y] = current_position

    return backtrace(start, goal, parents)



# pops lowest cost element off given list or in order of which it was enqueued if tied.
def priorityPop(q):
    current_lowest = q[0][0]
    index = 0
    for i in range (len(q)):
        if q[i][0] < current_lowest:
            current_lowest = q[i][0]
            index = i
    popped = q.pop(index)
    q[:] = q
    return popped

def distanceFromStart(start, coordinate, parents):
    distance = 0
    while coordinate != start:
        distance += 1
        coordinate = parents[coordinate[0]][coordinate[1]]
    return distance

def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    dimensions = maze.getDimensions()
    start = maze.getStart()
    goals = maze.getObjectives()
    goal = goals[0]
    # if there are multiple objectives, find the closest one
    if len(goals) > 1:
        goal = goals[findClosestObjective(start, goals)]

    return astarHelper(start, goal, dimensions, maze)


def astarHelper(start, goal, dimensions, maze):
    # this list represents priority queue frontier
    x_max = dimensions[1]
    y_max = dimensions[0]
    paths = []
    paths.append((0, start))
    parents = [[(None, None) for x in range(x_max)] for y in range(y_max)]
    visited = []
  
    while True:
        popped = priorityPop(paths)
        visited.append(popped)
        # current is just the current coordinate
        current = popped[1]
        if current == goal:
            break
        neighbors = maze.getNeighbors(current[0], current[1])
        for i in range (len(neighbors)):
            temp_x = neighbors[i][0]
            temp_y = neighbors[i][1]
            # distance from the start to current 
            g = distanceFromStart(start, current, parents)
            # distance from the goal to current neighbor using Manhattan distance
            h = calculateManhattan(goal, neighbors[i])
            # priority
            f = g + h
            # check if this coordinate is already in array of neighbors called 'paths'
            flag = True
            for a, element in enumerate (paths):
                if (neighbors[i] == element[1]):
                    flag = False
                    if (f < element[0]):
                        paths.append((f, neighbors[i]))
                        paths.pop(a)
                        parents[temp_x][temp_y] = current
                        break
                    
            # print("visited elements:\n")
            # for a, element in enumerate (visited):
            #     # print(element, "\n")
            #     if (neighbors[i] == element[1]):
            #         flag = False
            #         if (f < element[0]):
            #             paths.append((f, neighbors[i]))
            #             visited.pop(a)
            #             parents[temp_x][temp_y] = current
            #             break

            # if flag:
            #     paths.append((f, neighbors[i]))
            #     parents[temp_x][temp_y] = current

            for element in paths:
                if neighbors[i] in element:
                    flag = False
            if flag:
                for element in visited:
                    if neighbors[i] in element:
                        flag = False
            if flag:
                paths.append((f, neighbors[i]))
                parents[temp_x][temp_y] = current


    return backtrace(start, goal, parents)



def calculateManhattan(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def findClosestObjective(start, goals):
    shortest_distance = calculateManhattan(start, goals[0])
    shortest_index = 0
    # find the closest objective using manhattan distances
    for i, objective in enumerate (goals):
        temp = calculateManhattan(start, objective)
        if temp < shortest_distance:
            shortest_distance = temp
            shortest_index = i
    return shortest_index


def astar_multi(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    dimensions = maze.getDimensions()
    x_max = dimensions[1]
    y_max = dimensions[0]
    start = maze.getStart()
    goals = maze.getObjectives()
    path_weights = {}
    solution = []

    current_coordinate = start
    remaining_goals = goals
    
    for i in range (len(goals)):
        index_of_shortest = findClosestObjective(current_coordinate, remaining_goals)

    # index of goal in 'remaining_goals' that is closest to start
    closest_to_start = 0
    closest_distance = None
    # calculate the path_weights and find the closest goal to the start
    for i in range (len(remaining_goals)):
        temp = len(astarHelper(current_coordinate, remaining_goals[i], dimensions, maze))
        if (closest_distance == None) or (temp < closest_distance):
            closest_distance = temp
            closest_to_start = i
        for j in range (i + 1, len(remaining_goals)):
            # input1 = str(remaining_goals[i]) + str(remaining_goals[j])
            input2 = str(remaining_goals[j]) + str(remaining_goals[i])
            # path_weights[input1] = 
            path_weights[input2] = len(astarHelper(remaining_goals[i], remaining_goals[j], dimensions, maze))

    # solve closest objective first
    solution = astarHelper(current_coordinate, remaining_goals[index_of_shortest], dimensions, maze)

    # add path weight to array
    path_weights[str(current_coordinate) + str(remaining_goals[index_of_shortest])] = len(solution)

    # remove goal that was connected from remaining_goals
    remaining_goals.pop(index_of_shortest)


    while remaining_goals:
        # for every state on this new path, calculate heuristic to find which goal to solve next
        shortest_start = None
        curr_shortest = None
        index_of_shortest = None
        # traceback = []
        for traced, element in enumerate (solution):
            for i in range (len(remaining_goals)):
                obj = remaining_goals[i]
                # calculate a* distance from every state in solution to every remaining goal + distance that must be backtraced
                calc_dist = len(astarHelper(element, obj, dimensions, maze)) 
                # + (len(solution) - traced)
                if (curr_shortest == None) or (calc_dist < curr_shortest):
                    shortest_start = element
                    curr_shortest = calc_dist
                    index_of_shortest = i
            # traceback.insert(0, element)
        
        solution_fragment = astarHelper(shortest_start, remaining_goals[index_of_shortest], dimensions, maze)
        # add solution_fragment to full solution, then repeat

        # traceback.extend(solution_fragment)
        # solution.extend(traceback)
        solution.extend(solution_fragment)

        remaining_goals.pop(index_of_shortest)

    # solution = list( dict.fromkeys(solution))

    # path_weights_cp = path_weights
    # # loop until no more remaining goals
    # mst = {}
    # while(remaining_goals):
    #     # create mst
    #     # add smallest weight adjacent edge (Prim's) 
    #     smallest_key = findSmallestWeight(path_weights_cp, mst)
    #     mst[path_weights_cp[smallest_key]]
        
    #     # check if mst is fully connected
        

    
    return solution


            

def extra(maze):
    """
    Runs extra credit suggestion.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []
