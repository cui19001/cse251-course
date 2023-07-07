"""
Course: CSE 251
Lesson Week: 04
File: assignment.py
Author: Mark Cuizon

Purpose: Assignment 04 - Factory and Dealership

Instructions:

- See I-Learn

"""

import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts - Do not change
CARS_TO_PRODUCE = 500
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

        # Display the car that has just be created in the terminal
        self.display()
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        assert len(self.items) <= 10
        self.items.append(item)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, queue, car_space_semaphore, car_available_semaphore):    # Initialize the class with necessary parameters
        threading.Thread.__init__(self)                                         # Initialize the parent threading.Thread class
        self.queue = queue                                                      # Queue for storing cars
        self.car_space_semaphore = car_space_semaphore                          # Semaphore to check if there is space to produce a car
        self.car_available_semaphore = car_available_semaphore                  # Semaphore to signal when a car is available


    def run(self):                                  # Method that is run when the thread starts
        for i in range(CARS_TO_PRODUCE):            # Loop to produce the required number of cars
            self.car_space_semaphore.acquire()      # Check if there is space to produce a car, wait if not
            new_car = Car()                         # Create a new car
            self.queue.put(new_car)                 # Add the new car to the queue
            self.car_available_semaphore.release()  # Signal that a new car is available
            time.sleep(int(random.random() * 3) + 1)# Wait for a random time (between 1 and 3 seconds) before producing the next car
        self.car_space_semaphore.acquire()
        self.queue.put(None)                        # Add a special value to the queue to indicate that production has stopped.
        self.car_available_semaphore.release()

        # signal the dealer that there there are not more cars
        pass


class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, queue, car_space_semaphore, car_available_semaphore, queue_stats):   # Initialize the class with necessary parameters
        threading.Thread.__init__(self)                                                     # Initialize the parent threading.Thread class
        self.queue = queue                                                                  # Queue for storing cars
        self.car_space_semaphore = car_space_semaphore                                      # Semaphore to check if there is space to produce a car
        self.car_available_semaphore = car_available_semaphore                              # Semaphore to signal when a car is available
        self.queue_stats = queue_stats                                                      # queue_stats list to keep track of queue size
        self.cars_sold = 0                                                                  # count of sold cars

    def run(self):                                  # Method that is run when the thread starts
        while True:                                 # Continuously try to sell cars
            self.car_available_semaphore.acquire()  # Wait until a car is available
            queue_size = self.queue.size()          # get the current queue size

            # increment the count for this queue size in queue_stats
            if queue_size < MAX_QUEUE_SIZE:
                self.queue_stats[queue_size] += 1

            sold_car = self.queue.get()             # Remove a car from the queue to sell
            if sold_car is None:                    # Stop selling cars when the special value is encountered.
                break
            self.car_space_semaphore.release()      # Signal that there is now space for a new car
            self.cars_sold += 1                     # increment the count of sold cars

            
            if self.cars_sold >= CARS_TO_PRODUCE:   # check if all cars have been sold
                break                               # break the loop if so

            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))



def main():
    log = Log(show_terminal=True)

    car_space_semaphore = threading.Semaphore(MAX_QUEUE_SIZE)   # Semaphore to check if there is space to produce a car
    car_available_semaphore = threading.Semaphore(0)            # Semaphore to signal when a car is available
    queue = Queue251()                                          # Queue for storing cars
    # TODO Create lock(s) ?

    # This tracks the length of the car queue during receiving cars by the dealership
    # i.e., update this list each time the dealer receives a car
    queue_stats = [0] * MAX_QUEUE_SIZE

    factory = Factory(queue, car_space_semaphore, car_available_semaphore)                  # Creating an instance of the Factory class. 

    dealership = Dealer(queue, car_space_semaphore, car_available_semaphore, queue_stats)   # Creating an instance of the Dealer class. 

    log.start_timer()

    factory.start()
    dealership.start()

    factory.join()
    dealership.join()

    log.stop_timer(f'All {sum(queue_stats)} have been created')

    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')



if __name__ == '__main__':
    main()
