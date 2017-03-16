import numpy as np
from queue import *
import datetime
from collections import namedtuple

# Input and Output File Names
inState = "InitialConfig.txt"
fiState = "FinalConfig.txt"

# Out of 12 Boxes, these have colors
faces = np.array([1, 4, 5, 6, 7, 9])

# Possible moves, a state can have
rotations = np.array(["F", "B", "L", "R", "U", "D", "-F", "-B", "-L", "-R", "-U", "-D"])

# to read File and create a Cube
def cubeCreation():
    cube = np.zeros((12, 3, 3))
    file = open(inState, "r")
    i = 0; j = 0; k = 0
    for line in file:
        values = line.strip()
        if values:
            cube[faces[i], j, k] = values[0]
            k += 1
            cube[faces[i], j, k] = values[2]
            k += 1
            cube[faces[i], j, k] = values[4]
            k = 0
            j += 1
            if j == 3:
                j = 0
                i += 1
    return cube

# to read File and Create an Unscrambled Cube (Goal)
def unscrambledCubeCreation():
    cube = np.zeros((12, 3, 3))
    file = open(fiState, "r")
    i = 0
    j = 0
    k = 0
    for line in file:
        values = line.strip()
        if values:
            cube[faces[i], j, k] = values[0]
            k += 1
            cube[faces[i], j, k] = values[2]
            k += 1
            cube[faces[i], j, k] = values[4]
            k = 0
            j += 1
            if j == 3:
                j = 0
                i += 1
    return cube

# To compare with the final state of the cube
def goal_test(cube, faces):
    final_state = unscrambledCubeCreation()
    for i in range(6):
        for j in range(3):
            for k in range(3):
               if cube[faces[i], j, k] != final_state[faces[i], j, k]:
                  return False
    return True

# Transition Function for every possible move
def successor_function(cube, faces, move):

    if move == "F":
        # Saving Previous Values of "White" face
        face_1_values = [cube[1, 0, 0], cube[1, 1, 0], cube[1, 2, 0]]

        # Changing White Face values with Orange Face values
        cube[1][0][0] = cube[7][2][2]
        cube[1][1][0] = cube[7][1][2]
        cube[1][2][0] = cube[7][0][2]

        # Changing Orange Face values with Yellow Face values
        cube[7][0][2] = cube[9][0][2]
        cube[7][1][2] = cube[9][1][2]
        cube[7][2][2] = cube[9][2][2]

        # Changing Yellow Face values with Red Face values
        cube[9][0][2] = cube[5][2][0]
        cube[9][1][2] = cube[5][1][0]
        cube[9][2][2] = cube[5][0][0]

        # Changing Red Face values with Previously stored White face values
        cube[5][0][0] = face_1_values[0]
        cube[5][1][0] = face_1_values[1]
        cube[5][2][0] = face_1_values[2]

        # Rotating Green Face Clockwise 90º Degrees
        cube[4, :, :] = np.rot90(cube[4, :, :], 3)
        return cube

    if move == "B":
        # Saving Previous Values of "White" face
        face_1_values = [cube[1, 0, 2], cube[1, 1, 2], cube[1, 2, 2]]

        # Changing White Face values with Red Face values
        cube[1][0][2] = cube[5][0][2]
        cube[1][1][2] = cube[5][1][2]
        cube[1][2][2] = cube[5][2][2]

        # Changing Red Face values with Yellow Face values
        cube[5][0][2] = cube[9][2][0]
        cube[5][1][2] = cube[9][1][0]
        cube[5][2][2] = cube[9][0][0]

        # Changing Yellow Face values with Orange Face values
        cube[9][0][0] = cube[7][0][0]
        cube[9][1][0] = cube[7][1][0]
        cube[9][2][0] = cube[7][2][0]

        # Changing Orange Face values with Previously stored White face values
        cube[7][0][0] = face_1_values[2]
        cube[7][1][0] = face_1_values[1]
        cube[7][2][0] = face_1_values[0]

        # Rotating Blue Face Clockwise 90º Degrees
        cube[6, :, :] = np.rot90(cube[6, :, :], 3)
        return cube

    if move == "L":
        # Saving Previous Values of "White" face
        face_1_values = [cube[1, 0, 0], cube[1, 0, 1], cube[1, 0, 2]]

        # Changing White Face values with Blue Face values
        cube[1][0][0] = cube[6][0][0]
        cube[1][0][1] = cube[6][0][1]
        cube[1][0][2] = cube[6][0][2]

        # Changing Blue Face values with Yellow Face values
        cube[6][0][0] = cube[9][0][0]
        cube[6][0][1] = cube[9][0][1]
        cube[6][0][2] = cube[9][0][2]

        # Changing Yellow Face values with Green Face values
        cube[9][0][0] = cube[4][0][0]
        cube[9][0][1] = cube[4][0][1]
        cube[9][0][2] = cube[4][0][2]

        # Changing Green Face values with Previously stored White face values
        cube[4][0][0] = face_1_values[0]
        cube[4][0][1] = face_1_values[1]
        cube[4][0][2] = face_1_values[2]

        # Rotating Orange Face Clockwise 90º Degrees
        cube[7, :, :] = np.rot90(cube[7, :, :], 3)
        return cube

    if move == "R":
        # Saving Previous Values of "White" face
        face_1_values = [cube[1, 2, 0], cube[1, 2, 1], cube[1, 2, 2]]

        # Changing White Face values with Green Face values
        cube[1][2][0] = cube[4][2][0]
        cube[1][2][1] = cube[4][2][1]
        cube[1][2][2] = cube[4][2][2]

        # Changing Green Face values with Yellow Face values
        cube[4][2][0] = cube[9][2][0]
        cube[4][2][1] = cube[9][2][1]
        cube[4][2][2] = cube[9][2][2]

        # Changing Yellow Face values with Blue Face values
        cube[9][2][0] = cube[6][2][0]
        cube[9][2][1] = cube[6][2][1]
        cube[9][2][2] = cube[6][2][2]

        # Changing Blue Face values with Previously stored White face values
        cube[6][2][0] = face_1_values[0]
        cube[6][2][1] = face_1_values[1]
        cube[6][2][2] = face_1_values[2]

        # Rotating Red Face Clockwise 90º Degrees
        cube[5, :, :] = np.rot90(cube[5, :, :], 3)
        return cube

    if move == "U":
        # Saving Previous Values of "Green" face
        face_4_values = [cube[4, 0, 2], cube[4, 1, 2], cube[4, 2, 2]]

        # Changing Green Face values with Red Face values
        cube[4][0][2] = cube[5][0][0]
        cube[4][1][2] = cube[5][0][1]
        cube[4][2][2] = cube[5][0][2]

        # Changing Red Face values with Blue Face values
        cube[5][0][0] = cube[6][2][0]
        cube[5][0][1] = cube[6][1][0]
        cube[5][0][2] = cube[6][0][0]

        # Changing Blue Face values with Orange Face values
        cube[6][0][0] = cube[7][0][2]
        cube[6][1][0] = cube[7][0][1]
        cube[6][2][0] = cube[7][0][0]

        # Changing Orange Face values with Previously stored Green face values
        cube[7][0][0] = face_4_values[0]
        cube[7][0][1] = face_4_values[1]
        cube[7][0][2] = face_4_values[2]

        # Rotating White Face Clockwise 90º Degrees
        cube[1, :, :] = np.rot90(cube[1, :, :], 3)
        return cube

    if move == "D":
        # Saving Previous Values of "Green" face
        face_4_values = [cube[4, 0, 0], cube[4, 1, 0], cube[4, 2, 0]]

        # Changing Green Face values with Orange Face values
        cube[4][0][0] = cube[7][2][0]
        cube[4][1][0] = cube[7][2][1]
        cube[4][2][0] = cube[7][2][2]

        # Changing Orange Face values with Blue Face values
        cube[7][2][0] = cube[6][2][2]
        cube[7][2][1] = cube[6][1][2]
        cube[7][2][2] = cube[6][0][2]

        # Changing Blue Face values with Red Face values
        cube[6][0][2] = cube[5][2][2]
        cube[6][1][2] = cube[5][2][1]
        cube[6][2][2] = cube[5][2][0]

        # Changing Red Face values with Previously stored Green face values
        cube[5][2][0] = face_4_values[0]
        cube[5][2][1] = face_4_values[1]
        cube[5][2][2] = face_4_values[2]

        # Rotating Yellow Face Clockwise 90º Degrees
        cube[9, :, :] = np.rot90(cube[9, :, :], 3)
        return cube

    if move == "-F":
        # Saving Previous Values of "White" face
        face_1_values = [cube[1, 0, 0], cube[1, 1, 0], cube[1, 2, 0]]

        # Changing White Face values with Red Face values
        cube[1][0][0] = cube[5][0][0]
        cube[1][1][0] = cube[5][1][0]
        cube[1][2][0] = cube[5][2][0]

        # Changing Red Face values with Yellow Face values
        cube[5][0][0] = cube[9][2][2]
        cube[5][1][0] = cube[9][1][2]
        cube[5][2][0] = cube[9][0][2]

        # Changing Yellow Face values with Orange Face values
        cube[9][0][2] = cube[7][0][2]
        cube[9][1][2] = cube[7][1][2]
        cube[9][2][2] = cube[7][2][2]

        # Changing Orange Face values with Previously stored White face values
        cube[7][0][2] = face_1_values[2]
        cube[7][1][2] = face_1_values[1]
        cube[7][2][2] = face_1_values[0]

        # Rotating Green Face Counter-Clockwise 90º Degrees
        cube[4, :, :] = np.rot90(cube[4, :, :], 1)
        return cube

    if move == "-B":
        # Saving Previous Values of "White" face
        face_1_values = [cube[1, 0, 2], cube[1, 1, 2], cube[1, 2, 2]]

        # Changing White Face values with Orange Face values
        cube[1][0][2] = cube[5][2][0]
        cube[1][1][2] = cube[5][1][0]
        cube[1][2][2] = cube[5][0][0]

        # Changing Orange Face values with Yellow Face values
        cube[5][0][0] = cube[9][0][0]
        cube[5][1][0] = cube[9][1][0]
        cube[5][2][0] = cube[9][2][0]

        # Changing Yellow Face values with Red Face values
        cube[9][0][0] = cube[5][2][2]
        cube[9][1][0] = cube[5][1][2]
        cube[9][2][0] = cube[5][0][2]

        # Changing Red Face values with Previously stored White face values
        cube[5][0][2] = face_1_values[0]
        cube[5][1][2] = face_1_values[1]
        cube[5][2][2] = face_1_values[2]

        # Rotating Blue Face Counter-Clockwise 90º Degrees
        cube[6, :, :] = np.rot90(cube[6, :, :], 1)
        return cube

    if move == "-L":
        # Saving Previous Values of "White" face
        face_1_values = [cube[1, 0, 0], cube[1, 0, 1], cube[1, 0, 2]]

        # Changing White Face values with Green Face values
        cube[1][0][0] = cube[4][0][0]
        cube[1][0][1] = cube[4][0][1]
        cube[1][0][2] = cube[4][0][2]

        # Changing Green Face values with Yellow Face values
        cube[4][0][0] = cube[9][0][0]
        cube[4][0][1] = cube[9][0][1]
        cube[4][0][2] = cube[9][0][2]

        # Changing Yellow Face values with Blue Face values
        cube[9][0][0] = cube[6][0][0]
        cube[9][0][1] = cube[6][0][1]
        cube[9][0][2] = cube[6][0][2]

        # Changing Blue Face values with Previously stored White face values
        cube[6][0][0] = face_1_values[0]
        cube[6][0][1] = face_1_values[1]
        cube[6][0][2] = face_1_values[2]

        # Rotating Orange Face Counter-Clockwise 90º Degrees
        cube[7, :, :] = np.rot90(cube[7, :, :], 1)
        return cube

    if move == "-R":
        # Saving Previous Values of "White" face
        face_1_values = [cube[1, 2, 0], cube[1, 2, 1], cube[1, 2, 2]]

        # Changing White Face values with Blue Face values
        cube[1][2][0] = cube[6][2][0]
        cube[1][2][1] = cube[6][2][1]
        cube[1][2][2] = cube[6][2][2]

        # Changing Blue Face values with Yellow Face values
        cube[6][2][0] = cube[9][2][0]
        cube[6][2][1] = cube[9][2][1]
        cube[6][2][2] = cube[9][2][2]

        # Changing Yellow Face values with Green Face values
        cube[9][2][0] = cube[4][2][0]
        cube[9][2][1] = cube[4][2][1]
        cube[9][2][2] = cube[4][2][2]

        # Changing Blue Face values with Previously stored White face values
        cube[4][2][0] = face_1_values[0]
        cube[4][2][1] = face_1_values[1]
        cube[4][2][2] = face_1_values[2]

        # Rotating Red Face Counter-Clockwise 90º Degrees
        cube[5, :, :] = np.rot90(cube[5, :, :], 1)
        return cube

    if move == "-U":
        # Saving Previous Values of "Green" face
        face_4_values = [cube[4, 0, 2], cube[4, 1, 2], cube[4, 2, 2]]

        # Changing Green Face values with Orange Face values
        cube[4][0][2] = cube[7][0][0]
        cube[4][1][2] = cube[7][0][1]
        cube[4][2][2] = cube[7][0][2]

        # Changing Orange Face values with Blue Face values
        cube[7][0][0] = cube[6][2][0]
        cube[7][0][1] = cube[6][1][0]
        cube[7][0][2] = cube[6][0][0]

        # Changing Blue Face values with Red Face values
        cube[6][0][0] = cube[5][0][2]
        cube[6][1][0] = cube[5][0][1]
        cube[6][2][0] = cube[5][0][0]

        # Changing Red Face values with Previously stored Green face values
        cube[5][0][0] = face_4_values[0]
        cube[5][0][1] = face_4_values[1]
        cube[5][0][2] = face_4_values[2]

        # Rotating White Face Counter-Clockwise 90º Degrees
        cube[1, :, :] = np.rot90(cube[1, :, :], 1)
        return cube

    if move == "-D":
        # Saving Previous Values of "Green" face
        face_4_values = [cube[4, 0, 0], cube[4, 1, 0], cube[4, 2, 0]]

        # Changing Green Face values with Red Face values
        cube[4][0][0] = cube[5][2][0]
        cube[4][1][0] = cube[5][2][1]
        cube[4][2][0] = cube[5][2][2]

        # Changing Red Face values with Blue Face values
        cube[5][2][0] = cube[6][2][2]
        cube[5][2][1] = cube[6][1][2]
        cube[5][2][2] = cube[6][0][2]

        # Changing Blue Face values with Orange Face values
        cube[6][0][2] = cube[7][2][2]
        cube[6][1][2] = cube[7][2][1]
        cube[6][2][2] = cube[7][2][0]

        # Changing Orange Face values with Previously stored Green face values
        cube[7][2][0] = face_4_values[0]
        cube[7][2][1] = face_4_values[1]
        cube[7][2][2] = face_4_values[2]

        # Rotating Yellow Face Counter-Clockwise 90º Degrees
        cube[9, :, :] = np.rot90(cube[9, :, :], 1)
        return cube

# Function to iterate through each node of the graph
def iterateNodes (frontier, explored):

    # loop until nothing is left on frontier
    while not frontier.empty():
        current = frontier.get()
        explored.append(str(current))            # putting item on explored Queue
        for i in range(12):
            rotated = successor_function(np.array(current), faces, rotations[i])
            if str(rotated) not in explored:
                frontier.put(rotated)
                if goal_test(rotated, faces):
                    return rotated

# Breadth First Search Algorithm
def bfs(cube, faces):

    # if cube is unscrambled initially
    if goal_test(cube, faces):
        return cube

    frontier = Queue()
    explored = list()
    frontier.put(cube)

    return iterateNodes(frontier, explored)

# Depth First Search Algorithm
def dfs(cube, faces):

    # if cube is unscrambled initially
    if goal_test(cube, faces):
        return cube

    frontier = LifoQueue()
    explored = list()
    frontier.put(cube)

    return iterateNodes(frontier, explored)

# Scrambling the cube
cube = cubeCreation()

# Driver Program Flow
print("\n\t >> Initial Configuration \n")
print(cube)
start = datetime.datetime.now().replace(microsecond=0)
output = bfs(cube,faces)
end = datetime.datetime.now().replace(microsecond=0)
print("\n\t >> Final Configuration \n")
print(output)
print("\nTime Elapsed: " + str(end - start))

