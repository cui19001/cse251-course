"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here


# TODO Add any functions you need here


def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    # TODO Retrieve Top API urls

    # TODO Retireve Details on film 6

    # TODO Display results

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()
    response = requests.get(TOP_API_URL)
    
    # Check the status code to see if the request succeeded.
    if response.status_code == 200:
        data = response.json()
        print(data)

		# Example to get person 1 url
        print('\nHere is the URL for person id = 1:', f'{data["people"]}1')
    else:
        print('Error in requesting ID')
    # Make a GET request to the URL for person id = 1
    response = requests.get('http://127.0.0.1:8790/films/6/')

# Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
    # Access the response data (content)
      film_info = response.json()  # Assuming the response contains JSON data
    # Process the data as needed
      print(film_info['title'])
    else:
      print('Error:', response.status_code)
    # Display results
    log = Log(show_terminal=False)
    log.write('-----------------------------------------')
    log.write(f'Title   : {film_info["title"]}')
    log.write(f'Director: {film_info["director"]}')
    log.write(f'Producer: {film_info["producer"]}')
    log.write(f'Released: {film_info["release_date"]}\n')

    #for category in ["characters", "planets", "starships", "vehicles", "species"]:
        #data = retrieve_data(film_info[category])
        #names = sorted([item["name"] for item in data])
        #log.write(f'{category.capitalize()}: {len(names)}')
        #log.write(", ".join(names) + '\n')
