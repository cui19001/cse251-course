"""
Course: CSE 251
Lesson Week: 09
File: team1.py

Purpose: team activity - Dining philosophers problem

Problem statement

Five silent philosophers sit at a round table with bowls of spaghetti. Forks
are placed between each pair of adjacent philosophers.

Each philosopher must alternately think and eat. However, a philosopher can
only eat spaghetti when they have both left and right forks. Each fork can be
held by only one philosopher and so a philosopher can use the fork only if it
is not being used by another philosopher. After an individual philosopher
finishes eating, they need to put down both forks so that the forks become
available to others. A philosopher can only take the fork on their right or
the one on their left as they become available and they cannot start eating
before getting both forks.  When a philosopher is finished eating, they think 
for a little while.

Eating is not limited by the remaining amounts of spaghetti or stomach space;
an infinite supply and an infinite demand are assumed.

The problem is how to design a discipline of behavior (a concurrent algorithm)
such that no philosopher will starve

Instructions:

        **************************************************
        ** DO NOT search for a solution on the Internet **
        ** your goal is not to copy a solution, but to  **
        ** work out this problem.                       **
        **************************************************

- You have Locks and Semaphores that you can use.
- Remember that lock.acquire() has an argument called timeout.
- philosophers need to eat for 1 to 3 seconds when they get both forks.  
  When the number of philosophers has eaten MAX_MEALS times, stop the philosophers
  from trying to eat and any philosophers eating will put down their forks when finished.
- philosophers need to think for 1 to 3 seconds when they are finished eating.  
- You want as many philosophers to eat and think concurrently.
- Design your program to handle N philosophers and N forks after you get it working for 5.
- Use threads for this problem.
- When you get your program working, how to you prove that no philosopher will starve?
  (Just looking at output from print() statements is not enough)
- Are the philosophers each eating and thinking the same amount?
- Using lists for philosophers and forks will help you in this program.
  for example: philosophers[i] needs forks[i] and forks[i+1] to eat (the % operator helps)
"""

import time
import threading

PHILOSOPHERS = 5
MAX_MEALS_EATEN = PHILOSOPHERS * 5

def main():
    # TODO - create the forks
    #5 forks
    forks = [1, 2, 3, 4, 5]
    lock = threading.Lock()
    eaten = 0
    def eat(eating, whois, eaten, forks):
        #global forks
        if lock.acquire(timeout = eating):
          try:
            print(f"philosopher {whois} eating...")
            print(forks[whois])
            #print(forks[whois + 1])
            eaten += 1
          finally:
              lock.release()
        print(f"philosopher {whois} thinking...")
        time.sleep(3)
    # TODO - create PHILOSOPHERS philosophers
    #5 philosophers
    def philosopher(name):
        print("philosopher eating...")
        time.sleep(3)
        print("philosopher thinking...")
        time.sleep(3)
    #philosophers[5]
    # TODO - Start them eating and thinking
    #designate philosophers by number. have 1 and 3 eat, then think, then 2 and 4 eat and the think, then 3 and 5, then 4 and 1.
    philosopher1 = threading.Thread(target=eat, args=(3, 1, eaten, forks))
    philosopher2 = threading.Thread(target=eat, args=(3, 2, eaten, forks))
    philosopher3 = threading.Thread(target=eat, args=(3, 3, eaten, forks))
    philosopher4 = threading.Thread(target=eat, args=(3, 4, eaten, forks))
    philosopher5 = threading.Thread(target=eat, args=(3, 5, eaten, forks))

    philosopher1.start()
    philosopher2.start()
    philosopher3.start()
    philosopher4.start()
    philosopher5.start()

    if (eaten == MAX_MEALS_EATEN):
       philosopher1.join()
       philosopher2.join()
       philosopher3.join()
       philosopher4.join()
       philosopher5.join()
    
    # TODO - Display how many times each philosopher ate

    pass

if __name__ == '__main__':
    main()
