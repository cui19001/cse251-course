"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: Mark Cuizon

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions.
- Do not use any other Python modules other than the ones included.
- Each thread requires a different color by calling get_color().


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What would be your strategy?  

    My strategy would be to have the thread that found the exit to backtrack, 
    coloring its backtracked path, back to its parent and then backtrack 
    through the parent's path until it reaches the parent's parent and so forth.

Why would it work?

    This works logically because the thread that found the end is the one that 
    can claim the found path to the exit position.

"""
import math
import threading 
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 files
from cse251 import *

SCREEN_SIZE = 700
COLOR = (0, 0, 255)
COLORS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)
SLOW_SPEED = 100
FAST_SPEED = 0

# Globals
current_color_index = 0
thread_count = 0
stop = False
speed = SLOW_SPEED

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color

def thread_solve(maze, pos, color):
    """ Create new thread at each fork, continues the path if dead-end not reached """
    global stop, thread_count

    if stop:   # if any thread finds the exit, all others should stop
        return
    
    if maze.at_end(pos[0], pos[1]):  # if current position is the exit, stop all threads
        stop = True
        maze.move(pos[0], pos[1], color)
        return True
    
    maze.move(pos[0], pos[1], color)  # color the bmp

    threads = []
    poss = maze.get_possible_moves(pos[0], pos[1])    # tuples
    if len(poss) > 1:
        # Create a new thread for all paths except the last one
        for new_pos in poss[:-1]:
            new_thread = threading.Thread(target=thread_solve, args=(maze, new_pos, get_color()))
            threads.append(new_thread)
            thread_count += 1
            new_thread.start()

        # For the last path, continue on the same thread
        if thread_solve(maze, poss[-1], color):
            return True

        # wait for all threads to complete
        for t in threads:
            t.join()

    else:
        if poss:
            if thread_solve(maze, poss[0], color):
                return True

    #maze.restore(pos[0], pos[1])   # restores the maze part that doesn't lead to the end
    return False  # otherwise, return false


def solve_find_end(maze):
    """ finds the end position using threads.  Nothing is returned """
    # When one of the threads finds the end position, stop all of them
    global stop
    stop = False

    thread_count + 1

    thread_solve(maze, maze.get_start_pos(), get_color())

    #pass


def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count
    global speed

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

    done = False
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('1'):
                speed = SLOW_SPEED
            elif key == ord('2'):
                speed = FAST_SPEED
            elif key == ord('q'):
                exit()
            elif key != ord('p'):
                done = True
        else:
            done = True



def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)



if __name__ == "__main__":
    main()