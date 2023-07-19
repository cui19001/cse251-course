"""
Course: CSE 251, week 14
File: functions.py
Author: Mark Cuizon

I may have needed an extra day, but with this extra day, I was able to perfect my work on threading with this concurrent-capable server for maximum speeds.
I am happy to say that this program meets all requirements.

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
request = Request_thread(f'{TOP_API_URL}/family/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 6128784944, 
    'husband_id': 2367673859,        # use with the Person API
    'wife_id': 2373686152,           # use with the Person API
    'children': [2380738417, 2185423094, 2192483455]    # use with the Person API
}

Requesting an individual from the server:
request = Request_thread(f'{TOP_API_URL}/person/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 2373686152, 
    'name': 'Stella', 
    'birth': '9-3-1846', 
    'parent_id': 5428641880,   # use with the Family API
    'family_id': 6128784944    # use with the Family API
}

You will lose 10% if you don't detail your part 1 and part 2 code below

Describe how to speed up part 1

My breakthrough was realizing that the server can handle multiple, multiple concurrent requests.
We essentially create threads for everything and let each thread create their own threads as well.
Every person in a family unit deserves a thread to add them to the tree.
For recursion, the paths of both parents deserve a thread each and so on.


Describe how to speed up part 2

My breakthrough for this part was while loops and relearning about queues.
By using last in first out logic with the queue, we achieve a true breadth-first algorithm.
We can use the while loop to create a thread for each item in the queue, processing the queue as fast as possible while we make use of the server's concurrency abilities.


Extra (Optional) 10% Bonus to speed up part 3

For this part to even function, we have to keep revising the list of threads to only include active threads.
Otherwise, join() would eventually hitch the code as all five threads wait on each other with an empty queue or otherwise.
Combining the while loops into a while loop with two conditions is essential to keep a maximum of five threads working on a queue that isn't empty yet.
Beyond this, I'm not sure how to speed up part 3 with just five threads.

"""
from common import *
import queue

# -----------------------------------------------------------------------------
def depth_fs_pedigree(family_id, tree):
    family = Family(fam_process(family_id, tree, False, True))                          # Processes the family and retains the family information outside of the function.
    parents_ids = [tree.get_person(family.get_husband()).get_parentid(), tree.get_person(family.get_wife()).get_parentid()] # Creates a list of both parent's parent family IDs.
    threads = []                                                                        # Thread list for recursion.

    for parent_id in parents_ids:                                                       # For each parent's parent family ID,
        if parent_id is not None and parent_id != family.get_id():                      # If the parent's parent family ID isn't empty or the same as the parent's family ID,
            thread = threading.Thread(target=depth_fs_pedigree, args=(parent_id, tree)) # We create a recursive thread to take in the parent's parent family ID.
            thread.start()                                                              # Start the thread,
            threads.append(thread)                                                      # then add it to the thread list.

    for thread in threads:                                                              # For each recursive thread,
        thread.join()                                                                   # join them in the end.


def fetch_and_add_person(person_id, tree):                                              # This function is simply for requesting and then adding a person to the tree.
    if tree.get_person(person_id) is not None:                                          # If the person already exists in the tree,
        return                                                                          # we are done.
    
    request = Request_thread(f'{TOP_API_URL}/person/{person_id}')                       # Otherwise, create a thread to request the person's data.
    request.start()                                                                     # Start that thread.
    request.join()                                                                      # Complete that thread.

    if request.get_response() is not None:                                              # If the requested data isn't empty,
        person = Person(request.get_response())                                         # create a Person object with it,
        tree.add_person(person)                                                         # then add to the tree.


# -----------------------------------------------------------------------------
fam_queue = queue.LifoQueue()                                                           # Last in, first out queue.

def breadth_fs_pedigree(family_id, tree):                                               
    fam_queue.put(family_id)                                                            # Toss the starting family into the queue.

    family_men = []                                                                     # This is a list of family men to process the queue.
    while True:                                                                         # While the queue isn't empty,
        if fam_queue.empty():                                                           # if the queue ends up actually being empty,
            break                                                                       # break out of the loop.

        while fam_queue.empty() == False:                                               # While the queue isn't empty,
            man = threading.Thread(target=fam_process, args=(fam_queue.get(), tree, True, True))# Create a man to process a family in the queue.
            man.start()                                                                 # The man begins his work.
            family_men.append(man)                                                      # He is now a family man.

        for man in family_men:                                                          # For every family man,
            man.join()                                                                  # we finish their work.

             
def fam_process(family_id, tree, uses_queue, threaded):                                 # This is the main workhorse.
    request = Request_thread(f'{TOP_API_URL}/family/{family_id}')                       # Creates a thread to request off the server for the family id.
    request.start()                                                                     # Starts the thread.
    request.join()                                                                      # Completes it.

    if request.get_response() is None:                                                  # If there is nothing in that family id,
        return                                                                          # we are done.

    family = Family(request.get_response())                                             # Create a family object with the obtained information.
    tree.add_family(family)                                                             # Add the family object to the tree.

    person_ids = family.get_children() + [family.get_husband(), family.get_wife()]      # Create a list of IDs from every person in the family unit.
    if threaded == True:                                                                # If we are free to use as many threads as we want,
        threads = []                                                                    # we create a list of threads to use.

        for person_id in person_ids:                                                    # For every ID in the list of IDs,
            thread = threading.Thread(target=fetch_and_add_person, args=(person_id, tree))  # We create a thread to add the person attached to the ID to the tree.
            thread.start()                                                              # Start the thread,
            threads.append(thread)                                                      # and add to the list of threads.

        for thread in threads:                                                          # For each thread in the list of threads,
            thread.join()                                                               # We wait for them to complete.
    else:                                                                               # If we aren't free to use as many threads as we want,
        for person_id in person_ids:                                                    # for every ID in the list of IDs,
            fetch_and_add_person(person_id, tree)                                       # add the person attached to the ID to the tree.
    if uses_queue == True:                                                              # If this process is using the queue,
        if tree.get_person(family.get_husband()) is not None:                           # if the family has a father,
            if tree.get_person(family.get_husband()).get_parentid() is not None:        # and the father was raised in his own family,
                fam_queue.put(tree.get_person(family.get_husband()).get_parentid())     # we put the father's original family into the queue.

        if tree.get_person(family.get_wife()) is not None:                              # If the family has a mother,
            if tree.get_person(family.get_wife()).get_parentid() is not None:           # and the mother was raised in her own family,
                fam_queue.put(tree.get_person(family.get_wife()).get_parentid())        # we put the mother's original family into the queue.
    else:                                                                               # Otherwise, if the process isn't using a queue,
        return request.get_response()                                                   # return the family data to be processed some other way.


# def family_man(que, tree):                                                            # Family man process that never ended up getting used.
#     while True:
#         if fam_queue.empty():
#             break

#     while fam_queue.empty() == False:
#         fam_process(que.get(), tree, False)
# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(family_id, tree):
    fam_queue.put(family_id)                                                            # Toss the starting family into the queue.

    family_men = []                                                                     # This is a list of family men to process the queue.
    while True:                                                                         # While the queue isn't empty,
        family_men = [man for man in family_men if man.is_alive()]                      # create a list of family men who are still alive.

        if fam_queue.empty():                                                           # If the family queue is empty,
            if len(family_men) == 0:                                                    # and there are no living family men,
                break                                                                   # we are done.

        while len(family_men) < 5 and fam_queue.empty() == False:                       # If there are less than five family men with work still left to do,
                man = threading.Thread(target=fam_process, args=(fam_queue.get(), tree, True, False))   # we bring in more family men to work on the family queue.
                man.start()                                                             # They begin their work.
                family_men.append(man)                                                  # They are now a family man.

        for man in family_men:                                                          # For each family man,
            man.join()                                                                  # we wait for them to finish their work.