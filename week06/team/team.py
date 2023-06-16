"""
Course: CSE 251
Lesson Week: 06
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- Implement the process functions to copy a text file exactly using a pipe

After you can copy a text file word by word exactly
- Change the program to be faster (Still using the processes)

"""

import multiprocessing as mp
from multiprocessing import Value, Process
import filecmp 

# Include cse 251 common Python files
from cse251 import *

BLOCK = 1024 * 4
END_MESSAGE = 'done'

def sender(conn, filename):                     # Pipe sender.
    with open(filename, 'r') as file:           # Reads the file into `file`. Consider implementing Binary.
        #for line in file:                       # For each line in the file,
        while True:
            #words = line.split()                # Split the line into words by whitespace
            word = f.read(BLOCK)
            if not word:
                break
            conn.send(word)
            #for word in words:                  # For each word,
                #conn.send(word.encode('utf-8')) # Send it over the pipe as unicode.
                #count += 1
    #conn.send(None)                             # Sentinel value
    #conn.send(count)
    conn.close()                                # Closes the pipe.


def receiver(conn, filename_out, count):        # Pipe receiver.
    count.value = 0
    with open(filename_out, 'w') as file:       # Open an output file for writing
        while True:                             # While continuous,
            try:
            word = conn.recv()                  # Receive a word from the pipe
            #if word is None:                        # If it isn't a word,
                #break                           # Break continuity.
            ffile.write(word)
        escept E0FError:
        break
            count.value += 1                          # Increment once received
            file.write(word.decode('utf-8') + ' ')  # write the word as unicode plus space
        conn.close()                            # Close the pipe
        #return count                            # Return the number of words passed


def are_files_same(filename1, filename2):
    """ Return True if two files are the same """
    return filecmp.cmp(filename1, filename2, shallow = False) 


def copy_file(log, filename1, filename2):
    parent_conn, child_conn = mp.Pipe() # create a pipe 
    count_pipe = Value('i', 0)                     # create variable to count items sent over the pipe
    # TODO create processes 
    sender_process = mp.Process(target=sender, args=(child_conn, filename1))
    receiver_process = mp.Process(target=receiver, args=(parent_conn, filename2, count_pipe))

    log.start_timer()
    start_time = log.get_time()

    # TODO start processes 
    sender_process.start()
    receiver_process.start()
    #count_pipe = receiver_process.join()
    # TODO wait for processes to finish
    sender_process.join()
    receiver_process.join()

    stop_time = log.get_time()

    log.stop_timer(f'Total time to transfer content = {count_pipe.value}: ')
    log.write(f'items / second = {count_pipe.value / (stop_time - start_time)}')

    if are_files_same(filename1, filename2):
        log.write(f'{filename1} - Files are the same')
    else:
        log.write(f'{filename1} - Files are different')


if __name__ == "__main__": 

    log = Log(show_terminal=True)

    copy_file(log, 'gettysburg.txt', 'gettysburg-copy.txt')
    
    # After you get the gettysburg.txt file working, uncomment this statement
    # copy_file(log, 'bom.txt', 'bom-copy.txt')

