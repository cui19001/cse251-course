"""
Course: CSE 251
Lesson Week: 05
File: team.py
Author: Brother Comeau

Purpose: Check for prime values

Instructions:

- You can't use thread pools or process pools
- Follow the graph in I-Learn 
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it

"""
import time
import threading
import multiprocessing as mp
import random
from os.path import exists



#Include cse 251 common Python files
from cse251 import *

PRIME_PROCESS_COUNT = 1

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# TODO create read_thread function
def read_thread(filename, queue, amount_of_numbers_in_queue, unused_spots_in_queue):
    with open(filename, 'r') as file:
        for line in file:
            # queue.put(line.strip())
            unused_spots_in_queue.acquire()         
            queue.put(int(line))
            amount_of_numbers_in_queue.release()    # Adds 1

    for _ in range(PRIME_PROCESS_COUNT):
        queue.put(-1)
        amount_of_numbers_in_queue.release()    # Adds 1

# TODO create prime_process function
def process_prime(queue, primes, amount_of_numbers_in_queue, unused_spots_in_queue):
    while True:
        amount_of_numbers_in_queue.acquire()
        number = queue.get()        # Automatically blocks if queue is empty. A feature of Python's queue.
        
        if number < 0:
            break                   # Breaks if queue is done.

        if is_prime(number):
            print(number)
            primes.append(number)   # append() is thread safe

        unused_spots_in_queue.release()

def create_data_txt(filename):
    # only create if is doesn't exist 
    if not exists(filename):
        with open(filename, 'w') as f:
            for _ in range(1000):
                f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    filename = 'data.txt'
    create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures
    que = mp.Manager().Queue()
    primes = mp.Manager().list()

    amount_of_numbers_in_queue = mp.Semaphore(0)    # Forces something to equal 10 always.
    unused_spots_in_queue = mp.Semaphore(10)


    # TODO create reading thread
    reader = threading.Thread(target=read_thread, args=(filename, queue,))

    # TODO create prime processes
    processes = [mp.Process(target=process_prime, args=()) for _ in range(PRIME_PROCESS_COUNT)]

    # TODO Start them all
    for p in processes:
        p.start()
        reader.start()

    # TODO wait for them to complete
    reader.join()
    for p in processes:
        p.join()

    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()

