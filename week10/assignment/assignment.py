"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: Mark Cuizon

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  

- Do not use try...except statements

- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can use sleep() statements for any process.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List(), Barrier() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

- When each reader reads a value from the sharedList, use the following code to display
  the value:
  
                    print(<variable>, end=', ', flush=True)

Add any comments for me:
The program does exactly as the instructions say at the speed expected of a shared list.
"""

import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2

def writer(shared_list, lock, empty, full, i):                              # Due to pickling issues, I placed both functions outside of main().
  for _ in range(i):                                                        # For the range in items_to_send,
    empty.acquire()                                                         # one less empty spot in the buffer,
    lock.acquire()                                                          # grab the lock,
    shared_list[BUFFER_SIZE + 2] += 1                                       # increment the value to send to the reader,
    shared_list[shared_list[BUFFER_SIZE]] = shared_list[BUFFER_SIZE + 2]    # set the item in the spot of the current index to the value to send,
    shared_list[BUFFER_SIZE] = (shared_list[BUFFER_SIZE] + 1) % BUFFER_SIZE # move along the index while cycling back if the end is reached,
    lock.release()                                                          # then release the lock,
    full.release()                                                          # and indicate that a spot in the buffer is full.
  shared_list[BUFFER_SIZE + 4] += 1                                         # If the writer is finished with the loop, tag out.

def reader(shared_list, lock, empty, full):                                         # The reader takes in the shared list, the lock, and both semaphores.
  while True:                                                                       # While the loop is going,
    full.acquire()                                                                  # that's one less full spot in the buffer,
    lock.acquire()                                                                  # grab the lock,
    print(shared_list[shared_list[BUFFER_SIZE + 1]], end=', ', flush=True)          # read the item in the tail index,
    shared_list[BUFFER_SIZE + 1] = (shared_list[BUFFER_SIZE + 1] + 1) % BUFFER_SIZE # move along the tail index while cycling back if the end is reached,
    shared_list[BUFFER_SIZE + 3] += 1                                               # increment the number representing the number of items read,
    lock.release()                                                                  # release the lock,
    empty.release()                                                                 # then show there's another empty spot in the buffer.
    if shared_list[BUFFER_SIZE + 4] == WRITERS:                                     # If all writers have tagged out,
      break                                                                         # the readers are done.

def main():

    # This is the number of values that the writer will send to the reader
    items_to_send = random.randint(1000, 10000)

    smm = SharedMemoryManager()
    smm.start()

    shared_list = smm.ShareableList([0] * (BUFFER_SIZE + 5))  # I gave the shared list five extra spots. The first two are for the head and tail index, the third is for the value for the writer to send, the fourth is the number of values the readers have received, and the last spot is for the number of writers who tagged out.

    lock = mp.Lock()                                          # We just need one lock.
    empty = mp.Semaphore(BUFFER_SIZE)                         # Semaphore representing empty spots in the buffer.
    full = mp.Semaphore(0)                                    # Semaphore representing all full spots in the buffer.

    writers = [mp.Process(target=writer, args=(shared_list, lock, empty, full, items_to_send)) for _ in range(WRITERS)] # Create all writer processes.
    readers = [mp.Process(target=reader, args=(shared_list, lock, empty, full)) for _ in range(READERS)]                # Create all reader processes.

    for p in writers + readers:                               # For each process,
      p.start()                                               # start them all.

    for p in writers + readers:                               # For each process,
      p.join()                                                # join them all.

    print(f'{items_to_send} values sent')

    print(f'{shared_list[BUFFER_SIZE + 3]} values received')  # Show the number of values the readers received.
    smm.shutdown()


if __name__ == '__main__':
    main()
