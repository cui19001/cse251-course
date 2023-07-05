"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py

I think this assignment meets requirements because it fulfills all the rules of using the room.
On top of that, the output of this assignment matches the sample output with similar numbers in parties had and times cleaned.
"""

import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner: {id}')
    time.sleep(random.uniform(0, 2))

def guest_waiting():
    time.sleep(random.uniform(0, 2))

def guest_partying(id, count):
    print(f'Guest: {id}, count = {count}')
    time.sleep(random.uniform(0, 1))

def cleaner(id, key, cleaned):          # Cleaners get an ID, the key to the cleaner closet, and the tally counter for how many times cleaned.
    while True:                         # During the 60 seconds the room is functional,
        cleaner_waiting()               # wait for their turn.
        key.acquire()                   # Grab the cleaner closet key to get the supplies,
        print(STARTING_CLEANING_MESSAGE)# notify the residents that the room is starting to be cleaned,
        cleaner_cleaning(id)            # clean the room,
        print(STOPPING_CLEANING_MESSAGE)# notify the residents that the room is finished cleaning,
        cleaned.value += 1              # add a tally to the counter,
        key.release()                   # then return the cleaner closet key to the key rack.

def guest(id, key, clean_key, guest_counter, parties):  # Guests will have an I.D, the room key, the cleaner closet key, a counter for how many are partying, and a tally counter for how many parties were had.
    while True:                                         # During the 60 seconds the room is functional,
        guest_waiting()                                 # Wait to enter the room.
        key.acquire()                                   # Grab the room key.
        if guest_counter.value <= 0:                    # If you're the first one in,
            clean_key.acquire()                         # steal the key to the cleaner closet,
            print(STARTING_PARTY_MESSAGE)               # turn on the lights for the party,
            parties.value += 1                          # add a tally to the tally counter because a party just started.
        guest_counter.value += 1                        # There is, now, one additional guest in the party room.
        key.release()                                   # Slide the key back under the door so more guests can come in.
        guest_partying(id, guest_counter.value)         # Party.
        key.acquire()                                   # Grab the key back so you can
        guest_counter.value -= 1                        # leave the room.
        if guest_counter.value <= 0:                    # If you're the last one out,
            print(STOPPING_PARTY_MESSAGE)               # turn off the lights,
            clean_key.release()                         # and let the cleaners have their closet key back.
        key.release()                                   # Hang the room key back on the key rack.

def main():
    # Start time of the running of the program. 
    start_time = time.time()

    cleaner_key = mp.Lock()         # The key to the cleaner closet.
    room_key = mp.Lock()            # The key to the party room.
    people= []                      # Every human being involved with this room's operations.

    cleaned_count = mp.Value('i', 0)# The number of times the room was cleaned as a mp.Value() to be shared between processes.
    party_count = mp.Value('i', 0)  # The number of times a party was had as a mp.Value() to be shared between processes.
    guests = mp.Value('i', 0)       # The number of guests currently in the party room as a mp.Value() to be shared between processes.

    for i in range(CLEANING_STAFF): # For every assigned cleaning staff,
        p = mp.Process(target=cleaner, args=(i + 1, cleaner_key, cleaned_count))    # become a cleaner.
        people.append(p)            # Each cleaner counts as a human being involved with this room's operations.
        p.start()                   # Begin cleaning.

    for i in range(HOTEL_GUESTS):   # For each hotel guest,
        p = mp.Process(target=guest, args=(i + 1, room_key, cleaner_key, guests, party_count))  # become a guest.
        people.append(p)            # Each guest counts as a human being involved with this room's operations.
        p.start()                   # Begin partying.

    while True:                                 # While the room is operational,
        current_time = time.time()              # time is being kept.
        elapsed_time = current_time - start_time# Elapsed time is simply the current time minus the time the room became operational.

        if elapsed_time >= TIME:                # If a minute has passed,
            for p in people:                    # every person
                p.terminate()                   # must be kicked out, whether or not the room has been cleaned.
            break                               # The room is no longer operational.

        time.sleep(1)                           # Check the timer every 1 second


    for p in people:                            # That's it,
        p.join()                                # the party is over.

    # Results
    print(f'Room was cleaned {cleaned_count.value} times, there were {party_count.value} parties')


if __name__ == '__main__':
    main()

