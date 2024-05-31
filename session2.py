#!/usr/bin/python3

"""
This script performs a task related to Hotel and Band reservations using the ReservationApi class
from the reservationapi module. It reads configuration settings from the 'api.ini' file to establish
communication with the hotel and band APIs. The script attempts to find the earliest common slot
available between the Hotel and Band, and reserves it for the client.

Approach:
1. Import necessary modules and libraries.
2. Load the configuration file to get the URLs and keys for the APIs.
3. Create API objects to communicate with the hotel and band APIs.
4. Define a function 'refresh()' to perform the reservation process.
5. Check if the client is already holding a slot. If not, set the optimal slot ID as a default value which definitely means a slot will be reserved.
6. Get the available slots for the hotel and band APIs.
7. Extract the slot IDs and store them in separate lists.
8. Find the common slots available in both lists.
9. Sort the common slots and print the first 20 slots.
10. Reserve the earliest common slot for the client, releasing the previous slot if applicable.
11. Print the held slots for both the hotel and band.
12. Repeat the process for another four iterations to try and improve upon the slot.
13. End the script.

Author: Oliver Clements
"""

import reservationapi
import configparser
import time

# Load the configuration file containing the URLs and keys
config = configparser.ConfigParser()
config.read("api.ini")

# Create an API object to communicate with the hotel API
hotel  = reservationapi.ReservationApi(config['hotel']['url'],
                                       config['hotel']['key'],
                                       int(config['global']['retries']),
                                       float(config['global']['delay']))

# Create an API object to communicate with the band API
band  = reservationapi.ReservationApi(config['band']['url'],
                                       config['band']['key'],
                                       int(config['global']['retries']),
                                       float(config['global']['delay']))

# Your code goes here

# Function that actually carries out the searching for and reserving of slots
def refresh():
    # Checks to see the best slot held, if no slots held ensures that a slot will still be selected
    initial = band.get_slots_held()
    if initial:
        optimal_slot = initial[0]
        optimal_slot = optimal_slot["id"]
    else:
        optimal_slot = 551

    # Get Slots for Hotel and Band
    print("Obtaining the available slots for hotels and bands...")
    available_hotel_slots = hotel.get_slots_available()
    available_band_slots = band.get_slots_available()

    hotels = []
    bands= []

    # Converts the dictionary of hotel slots to a list of just the slot number, removing the key
    for x in range(len(available_hotel_slots)):
        current = available_hotel_slots[x]
        hotels.append(current["id"])

    # Converts the dictionary of band slots to a list of just the slot number, removing the key
    for y in range(len(available_band_slots)):
        current = available_band_slots[y]
        bands.append(current["id"])

    print("Checking the availability of common slots...")
    print()
    common_slots = set(hotels).intersection(bands) # Finds the slots that are common to both the available bands and the available hotels
    common_slots_list = list(sorted(common_slots)) # Sorts the slots so that the lowest number is treated as the priority
    print("The first 20 common slots are: ", common_slots_list[:20])
    print()
    hotels.clear()
    bands.clear()

    # Reserve a slot for the client
    if (int(common_slots_list[0]) < int(optimal_slot)): # A slot should only be reserved if it is better than the slot currently held
        print("Attempting to reserve the earliest common slot...")
        slot_id = common_slots_list[0]
        try:
            hotel.reserve_slot(slot_id)
            try:
                band.reserve_slot(slot_id)
            except: # If the hotel slot has been reserved and the band slot can't be reserved then the hotel slot needs to be released
                hotel.release_slot(slot_id)
                refresh()
        except:
            print("Error - Retrying")
            refresh()
        if (optimal_slot != 551):
            # Release the old slot which wasn't as good
            hotel.release_slot(optimal_slot)
            band.release_slot(optimal_slot)
        optimal_slot = slot_id
    else: 
        print("There are currently no better slots")
        print()

    # Display the current slot held to the client
    hotel_held_slots = hotel.get_slots_held()
    band_held_slots = band.get_slots_held()
    print("Held Hotel slots: ", hotel_held_slots)
    print("Held Band slots: ", band_held_slots)

# Overall the best slot is searched for 5 times 
for a in range(4):
    refresh()
    print("Rechecking for better bookings...")
refresh()
print("End of Program")

# As you work on your Lab 3 coursework, I wanted to remind you of the importance of commenting your code. 
# Commenting your code is a great way to make it more readable and understandable to others. 
# It can also help you debug your code and understand your own thought process later on. 
# In addition to commenting your code, I also wanted to remind you to include a header in your "mysession2.py" file that describes your approach 
# to completing tasks as defined in the lab exercise. This will help the markers to understand your thought process and provide context for your code.
