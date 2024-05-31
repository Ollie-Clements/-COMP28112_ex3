#!/usr/bin/python3

import reservationapi
import configparser

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

# Obtain the list of available slots
print("Obtaining the list of available slots...")
available_slots = hotel.get_slots_available()
print("Available Hotel Slots:", available_slots)
print()
bavailable_slots = band.get_slots_available()
print("Available Band Slots:", bavailable_slots)
print()

# Obtain the list of slots held by the client
print("Obtaining the list of slots held by the client...")
held_slots = hotel.get_slots_held()
print("Held Hotel Slots:", held_slots) 
print()
bheld_slots = band.get_slots_held()
print("Held Band Slots:", bheld_slots) 
print()

optimal_slot = available_slots[0]
boptimal_slot = bavailable_slots[0]

# Reserve a slot for the client
print("Attempting to reserve a slot for the client...")
slot_id = optimal_slot["id"] 
hotel.reserve_slot(slot_id)
print("Hotel Slot " + slot_id + " reserved successfully!")
print()
bslot_id = boptimal_slot["id"] 
band.reserve_slot(bslot_id)
print("Band Slot " + bslot_id + " reserved successfully!")
print()

# Obtain the list of slots held by the client
held_slots = hotel.get_slots_held()
print("Held Hotel Slots:", held_slots) 
print()
bheld_slots = band.get_slots_held()
print("Held Band Slots:", bheld_slots) 
print()

# Release a slot held by the client
print("Releasing a slot held by the client...")
slot_id = optimal_slot["id"] 
hotel.release_slot(slot_id)
print("Hotel Slot " + slot_id + " released successfully")
print()
bslot_id = boptimal_slot["id"] 
band.release_slot(bslot_id)
print("Band Slot " + bslot_id + " released successfully")
print()

# Obtain the list of slots held by the client
held_slots = hotel.get_slots_held()
print("Held Hotel Slots:", held_slots) 
print()
bheld_slots = band.get_slots_held()
print("Held Band Slots:", bheld_slots) 
print()