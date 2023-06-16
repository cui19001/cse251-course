"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: Mark Cuizon
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.

I think I'm slightly deficient because I only got the bare minimum of the program working done.
I have a feeling that there are ways to make this code faster.
"""

import random
import multiprocessing as mp
import os.path
import time
import datetime

# Include cse 251 common Python files - Don't change
from cse251 import *

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME   = 'boxes.txt'

# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
NUMBER_OF_MARBLES_IN_A_BAG = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'


DONE = "Done!"
# No Global variables

class Bag():
    """ bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, o_conn, MARBLE_COUNT, CREATOR_DELAY):
        mp.Process.__init__(self)
        self.o_conn = o_conn                # Free variable
        self.MARBLE_COUNT = MARBLE_COUNT    # Passing in settings
        self.CREATOR_DELAY = CREATOR_DELAY  # And once again


    def run(self):
        for _ in range(self.MARBLE_COUNT):              # For the number of marbles we have to make,
            self.o_conn.send(random.choice(self.colors))# Send a random marble.
            time.sleep(self.CREATOR_DELAY)              # Then sleep for a little bit.
        self.o_conn.send(DONE)                          # Tell bagger there are no more marbles
        self.o_conn.close()                             # When all marbles have been created, close the pipe.


class Bagger(mp.Process):
    def __init__(self, i_conn, o_conn, NUMBER_OF_MARBLES_IN_A_BAG, BAGGER_DELAY):
        mp.Process.__init__(self)
        self.i_conn = i_conn                # Free variable.
        self.o_conn = o_conn                # Another free variable.
        self.bag = Bag()                    # Local bag
        self.NUMBER_OF_MARBLES_IN_A_BAG = NUMBER_OF_MARBLES_IN_A_BAG    # Passing in settings
        self.BAGGER_DELAY = BAGGER_DELAY    # And once again

    def run(self):
        while True:                             # While this is going on,
            marble = self.i_conn.recv()         # Recieve the marble
            if marble == DONE:                  # If the marble is some piece of paper saying "Done!"
                if self.bag.get_size() > 0:     # And there's still some marbles in the bag,
                    self.o_conn.send(self.bag)  # Send the half-empty bag.
                self.o_conn.send(DONE)          # Tell the Assember that we're done.
                self.o_conn.close()             # Close pipe
                break                           # Finish loop
            self.bag.add(marble)                # Adds marble into the bag
            if self.bag.get_size() == self.NUMBER_OF_MARBLES_IN_A_BAG:  # If the bag is full,
                self.o_conn.send(self.bag)      # Send the bag to the assembler
                self.bag = Bag()                # Resets the bag
                time.sleep(self.BAGGER_DELAY)   # Designated sleep time




class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'Big Joe', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, i_conn, o_conn, ASSEMBLER_DELAY):
        mp.Process.__init__(self)
        self.i_conn = i_conn    # Free variable.
        self.o_conn = o_conn    # Another free variable.
        self.ASSEMBLER_DELAY = ASSEMBLER_DELAY  # Passing in settings

    def run(self):
        while True:                         # While this is going on,
            bag = self.i_conn.recv()        # Receive the bag
            if bag == DONE:                 # If the bag just has a paper that says "Done!",
                self.o_conn.send(DONE)      # Tell the Wrapper that we're done.
                self.o_conn.close()         # Close pipe
                break                       # Break out of loop
            large_marble = random.choice(self.marble_names) # Get a random large marble
            gift = Gift(large_marble, bag)  # Create a gift to send
            self.o_conn.send(gift)          # Send the gift to the Wrapper
            time.sleep(self.ASSEMBLER_DELAY)# Designated sleep time


class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self, i_conn, WRAPPER_DELAY):
        mp.Process.__init__(self)
        self.i_conn = i_conn                    # Free variable.
        self.WRAPPER_DELAY = WRAPPER_DELAY      # Passing in settings

    def run(self):
        with open("boxes.txt", "w") as file:    # Open up boxes.txt to write to
            while True:                         # While this is going on,
                gift = self.i_conn.recv()       # Receive the gift.
                if gift == DONE:                # If the gift is just... "Done!"
                    break                       # Break out of the loop
                file.write(f'Created - {datetime.now().time()}: {gift}\n')  # Write these lines into boxes.txt
                time.sleep(self.WRAPPER_DELAY)  # Designated sleep time.


def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count     = {settings[MARBLE_COUNT]}')
    log.write(f'Marble delay     = {settings[CREATOR_DELAY]}')
    log.write(f'Marbles in a bag = {settings[NUMBER_OF_MARBLES_IN_A_BAG]}') 
    log.write(f'Bagger delay     = {settings[BAGGER_DELAY]}')
    log.write(f'Assembler delay  = {settings[ASSEMBLER_DELAY]}')
    log.write(f'Wrapper delay    = {settings[WRAPPER_DELAY]}')

    m_conn, mb_conn = mp.Pipe()         # Marble pipe
    b_conn, ba_conn = mp.Pipe()         # Bagger pipe
    a_conn, aw_conn = mp.Pipe()         # Assember pipe

    log.write('Create the processes')   # The Processes are being created

    creator = Marble_Creator(m_conn, settings[MARBLE_COUNT], settings[CREATOR_DELAY])               # The Creator
    bagger = Bagger(mb_conn, b_conn, settings[NUMBER_OF_MARBLES_IN_A_BAG], settings[BAGGER_DELAY])  # The Bagger
    assembler = Assembler(ba_conn, a_conn, settings[ASSEMBLER_DELAY])                               # The Assembler
    wrapper = Wrapper(aw_conn, settings[WRAPPER_DELAY])                                             # The Wrapper

    processes = [creator, bagger, assembler, wrapper]                                               # All processes

    log.write('Starting the processes')                                                             # The processes are starting

    for process in processes:                                                                       # For each process,
        process.start()                                                                             # Start them

    log.write('Waiting for processes to finish')                                                    # Now, we wait

    for process in processes:                                                                       # For each process,
        process.join()                                                                              # Wait and join.

    display_final_boxes(BOXES_FILENAME, log)                                                        # Time to display the work
    
    with open(BOXES_FILENAME, 'r') as f:                                                            # Read boxes.txt
        lines = f.readlines()                                                                       # Go through each line,
        log.write(f'Number of gifts created: {len(lines)}')                                         # The number of lines is the amount of gifts created.

if __name__ == '__main__':                                                                          # Main
    main()                                                                                          # Main
