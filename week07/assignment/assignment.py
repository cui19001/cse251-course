"""
Course: CSE 251
Lesson Week: 07
File: assingnment.py
Author: Mark Cuizon
Purpose: Process Task Files

Instructions:  See I-Learn


Add your comments here on the pool sizes that you used for your assignment and
why they were the best choices.

    prime_pool = mp.Pool(processes=2)   # 2 processes because this is CPU-bound.
    word_pool = mp.Pool(processes=4)    # 4 processes because this is I/O bound, but by file.
    upper_pool = mp.Pool(processes=2)   # 2 processes because this is CPU-bound.
    sum_pool = mp.Pool(processes=2)     # 2 processes because this is CPU-bound.
    name_pool = mp.Pool(processes=8)    # 8 processes because this is I/O bound, but by network.

Also, I'm running on an AMD Ryzen 7 3700X CPU on Windows 10 with a handful of other programs in the background.
This was the furthest I could do without freezing up other programs.
The process ratio was also determined through trial and error. Adding more to name_pool did the most difference.


"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
from cse251 import *

TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def is_prime(n: int):
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
 
def task_prime(value):
    if is_prime(value) == True:         # If the value is prime according to the function above,
        return f"{value} is prime"      # return the designated message.
    else:                               # Otherwise,
        return f"{value} is not prime"  # return the other designated message.
    
def prime_callback(result):             
    result_primes.append(result)        # Appends the result to result_primes.
    

def task_word(word):
    with open('words.txt', 'r') as file:# While reading the words.txt file,
        for line in file:               # for every line,
            if word in line:            # if the word exists in the line
                return f"{word} Found"  # return the designated message.
    return f"{word} not found *****"    # Otherwise, return the other designated message.
            
def word_callback(result):
    result_words.append(result)         # Appends the result to result_words.

def task_upper(text):
    return text.upper()                 # Simply returns the uppercase version of what is passed in.

def upper_callback(result):
    result_upper.append(result)         # Appends the result to result_upper.

def task_sum(start_value, end_value):
    total = start_value + end_value     # The designated total is the start and end value added together,
    return f"sum of {start_value:,} to {end_value:,} = {total:,}"   # then return the designated message.

def sum_callback(result):
    result_sums.append(result)          # Append the result to result_sums.

def task_name(url):
    #try:                                       # Try except loop. Let's hope this works.
        response = requests.get(url, timeout=5) # Requests on the url for a response.
        if response.status_code == 200:         # If the request goes through,
        #response.raise_for_status()            # Raise an error if it doesn't go through.
            data = response.json()              # JSON is pulled from the response.
            name = data['name']                 # A variable to simplyify things.
            return f"{url} has name {name}"     # Return the designated message.
    #elif response.status_code == 404:          # If it doesn't go through,
    #except requests.exceptions.RequestException as e:   # For this exception,
        return f"{url} had an error receiving the information"  # Return the other designated message.
    
def name_callback(result):
    result_names.append(result)         # Append the result to result_names


def main():
    log = Log(show_terminal=True)
    log.start_timer()


    prime_pool = mp.Pool(processes=2)   # 2 processes because this is CPU-bound.
    word_pool = mp.Pool(processes=4)    # 4 processes because this is I/O bound, but by file.
    upper_pool = mp.Pool(processes=2)   # 2 processes because this is CPU-bound.
    sum_pool = mp.Pool(processes=2)     # 2 processes because this is CPU-bound.
    name_pool = mp.Pool(processes=8)    # 8 processes because this is I/O bound, but by network.

    
    count = 0
    task_files = glob.glob("*.task")
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            #task_prime(task['value'],)
            prime_pool.apply_async(task_prime, args=(task['value'],), callback=prime_callback)          # Adds the task to an asynchronous pool.
        elif task_type == TYPE_WORD:
            #task_word(task['word'])
            word_pool.apply_async(task_word, args=(task['word'],), callback=word_callback)              # Adds the task to an asynchronous pool.
        elif task_type == TYPE_UPPER:
            #task_upper(task['text'])
            upper_pool.apply_async(task_upper, args=(task['text'],), callback=upper_callback)           # Adds the task to an asynchronous pool.
        elif task_type == TYPE_SUM:
            #task_sum(task['start'], task['end'])
            sum_pool.apply_async(task_sum, args=(task['start'], task['end']), callback=sum_callback)    # Adds the task to an asynchronous pool.
        elif task_type == TYPE_NAME:
            #task_name(task['url'])
            name_pool.apply_async(task_name, args=(task['url'],), callback=name_callback)               # Adds the task to an asynchronous pool.
        else:
            log.write(f'Error: unknown task type {task_type}')

    prime_pool.close()
    word_pool.close()
    upper_pool.close()
    sum_pool.close()
    name_pool.close()   # Closes all pools,
    prime_pool.join()
    word_pool.join()
    upper_pool.join()
    sum_pool.join()
    name_pool.join()    # then joins them all.

    # Do not change the following code (to the end of the main function)
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Finished processes {count} tasks')

if __name__ == '__main__':
    main()
