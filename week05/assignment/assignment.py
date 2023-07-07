"""
Course: CSE 251
Lesson Week: 05
File: assignment.py
Author: Mark Cuizon

Purpose: Assignment 05 - Factories and Dealers

Instructions:

- Read the comments in the following code.  
- Implement your code where the TODO comments are found.
- No global variables, all data must be passed to the objects.
- Only the included/imported packages are allowed.  
- Thread/process pools are not allowed
- You MUST use a barrier
- Do not use try...except statements
- You are not allowed to use the normal Python Queue object.  You must use Queue251.
- the shared queue between the threads that are used to hold the Car objects
  can not be greater than MAX_QUEUE_SIZE

  I ended up giving up after multiple tries of getting the Dealer to catch the sentinel value.
  I'm absolutely clueless on why it isn't receiving it.

"""

from datetime import datetime, timedelta
import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has was just created in the terminal
        self.display()
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []
        self.max_size = 0

    def get_max_size(self):
        return self.max_size

    def put(self, item):
        self.items.append(item)
        if len(self.items) > self.max_size:
            self.max_size = len(self.items)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, car_queue, car_space_semaphore, car_available_semaphore, factory_barrier, dealer_count):
        threading.Thread.__init__(self)
        self.cars_to_produce = random.randint(200, 300)     # Don't change
        self.car_queue = car_queue
        self.car_space_semaphore = car_space_semaphore
        self.car_available_semaphore = car_available_semaphore
        self.factory_barrier = factory_barrier
        self.dealer_count = dealer_count
        self.cars_produced = 0                      # Track the number of cars produced


    def run(self):
        for _ in range(self.cars_to_produce):       # For the number of cars this factory will produce,
            new_car = Car()                         # Create a new car
            self.cars_produced += 1                 # Increment the number of cars produced
            self.car_space_semaphore.acquire()  # Wait until there is space available in the dealership queue
            self.car_queue.put(new_car)             # Place the car on the car queue
            self.car_available_semaphore.release()
    
        self.factory_barrier.wait()                 # Wait until all of the factories are finished producing cars

        if self.factory_barrier.n_waiting == 0:     # "Wake up/signal" the dealerships one more time. Select one factory to do this
            #for _ in range(MAX_QUEUE_SIZE):
            print("barrier reached")
            for _ in range(self.dealer_count):
                self.car_queue.put(None)
                print("sentinel value sent")
                self.car_space_semaphore.release()




class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, car_queue, car_space_semaphore, car_available_semaphore, i, dealer_stats):
        threading.Thread.__init__(self)
        self.car_queue = car_queue
        self.car_available_semaphore = car_available_semaphore
        self.car_space_semaphore = car_space_semaphore
        self.i = i
        self.dealer_stats = dealer_stats

    def run(self):
        while True:
            # Wait until there is a car in the car_queue
            self.car_available_semaphore.acquire()
            #if not self.car_queue.items:  # if the queue is empty, release the semaphore and break the loop
                #self.dealer_semaphore.release()
                #break

            car = self.car_queue.get()
            print("Received car:", repr(car))
            print("increment")

            # Check for the sentinel value
            if car is None:
                print("sentinel value receieved")
                self.car_space_semaphore.release()
                break

            # Increment the count of cars sold by this dealer
            self.dealer_stats[self.i] += 1

            # Signal that a slot in the car_queue is available
            self.car_space_semaphore.release()


            # Sleep a little - don't change.  This is the last line of the loop
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR + 0))



def run_production(factory_count, dealer_count):
    """ This function will do a production run with the number of
        factories and dealerships passed in as arguments.
    """

    # TODO Create semaphore(s) if needed
    car_space_semaphore = threading.Semaphore(MAX_QUEUE_SIZE)
    car_available_semaphore = threading.Semaphore(0)
    # TODO Create queue
    car_queue = Queue251()
    # TODO Create lock(s) if needed
    #queue_lock = threading.Lock()
    # TODO Create barrier
    factory_barrier = threading.Barrier(factory_count)
    # This is used to track the number of cars receives by each dealer
    dealer_stats = list([0] * dealer_count)

    # TODO create your factories, each factory will create CARS_TO_CREATE_PER_FACTORY
    factories = [Factory(car_queue, car_space_semaphore, car_available_semaphore, factory_barrier, dealer_count) for _ in range(factory_count)]
    # TODO create your dealerships
    dealers = [Dealer(car_queue, car_space_semaphore, car_available_semaphore, i, dealer_stats) for i in range(dealer_count)]

    log.start_timer()

    # TODO Start all dealerships
    for dealer in dealers:
        dealer.start()
    # TODO Start all factories
    for factory in factories:
        factory.start()

    # TODO Wait for factories and dealerships to complete
    for factory in factories:
        factory.join()
    for dealer in dealers:
        dealer.join()

    # Collect statistics
    factory_stats = [factory.cars_produced for factory in factories]

    run_time = log.stop_timer(f'{sum(dealer_stats)} cars have been created')

    # This function must return the following - Don't change!
    # factory_stats: is a list of the number of cars produced by each factory.
    #                collect this information after the factories are finished. 
    return (run_time, car_queue.get_max_size(), dealer_stats, factory_stats)


def main(log):
    """ Main function - DO NOT CHANGE! """

    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for factories, dealerships in runs:
        run_time, max_queue_size, dealer_stats, factory_stats = run_production(factories, dealerships)

        log.write(f'Factories      : {factories}')
        log.write(f'Dealerships    : {dealerships}')
        log.write(f'Run Time       : {run_time:.4f}')
        log.write(f'Max queue size : {max_queue_size}')
        log.write(f'Factory Stats  : {factory_stats}')
        log.write(f'Dealer Stats   : {dealer_stats}')
        log.write('')

        # The number of cars produces needs to match the cars sold
        assert sum(dealer_stats) == sum(factory_stats)


if __name__ == '__main__':

    log = Log(show_terminal=True)
    main(log)


