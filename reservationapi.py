""" Reservation API wrapper

This class implements a simple wrapper around the reservation API. It
provides automatic retries for server-side errors, delays to prevent
server overloading, and produces sensible exceptions for the different
types of client-side error that can be encountered.
"""

# This file contains areas that need to be filled in with your own
# implementation code. They are marked with "Your code goes here".
# Comments are included to provide hints about what you should do.

import requests
import simplejson
import warnings
import time

from requests.exceptions import HTTPError
from exceptions import (
    BadRequestError, InvalidTokenError, BadSlotError, NotProcessedError,
    SlotUnavailableError,ReservationLimitError)

class ReservationApi:
    def __init__(self, base_url: str, token: str, retries: int, delay: float):
        """ Create a new ReservationApi to communicate with a reservation
        server.

        Args:
            base_url: The URL of the reservation API to communicate with.
            token: The user's API token obtained from the control panel.
            retries: The maximum number of attempts to make for each request.
            delay: A delay to apply to each request to prevent server overload.
        """
        self.base_url = base_url
        self.token    = token
        self.retries  = retries
        self.delay    = delay

    def _reason(self, req: requests.Response) -> str:
        """Obtain the reason associated with a response"""
        reason = ''

        # Try to get the JSON content, if possible, as that may contain a
        # more useful message than the status line reason
        try:
            json = req.json()
            reason = json['message']

        # A problem occurred while parsing the body - possibly no message
        # in the body (which can happen if the API really does 500,
        # rather than generating a "fake" 500), so fall back on the HTTP
        # status line reason
        except simplejson.errors.JSONDecodeError:
            if isinstance(req.reason, bytes):
                try:
                    reason = req.reason.decode('utf-8')
                except UnicodeDecodeError:
                    reason = req.reason.decode('iso-8859-1')
            else:
                reason = req.reason

        return reason


    def _headers(self) -> dict:
        """Create the authorization token header needed for API requests"""
        # Your code goes here
        headers = {"Authorization": "Bearer " + self.token}
        return headers

        # Allow for multiple retries if needed
            # Perform the request.
        
            # Delay before processing the response to avoid swamping server.

            # 200 response indicates all is well - send back the json data.

            # 5xx responses indicate a server-side error, show a warning
            # (including the try number).

            # 400 errors are client problems that are meaningful, so convert
            # them to separate exceptions that can be caught and handled by
            # the caller.

            # Anything else is unexpected and may need to kill the client.

        # Get here and retries have been exhausted, throw an appropriate
        # exception.

    def _send_request(self, method: str, endpoint: str) -> dict:
        """Send a request to the reservation API and convert errors to
           appropriate exceptions"""
        # Your code goes here
        url = self.base_url + endpoint
        headers = self._headers()

        for x in range(self.retries):
            try:
                response = requests.request(method, url, headers=headers)
                time.sleep(self.delay) 

                if response.status_code == 200:
                    return response.json()

                elif (response.status_code >= 500 and response.status_code <= 599):
                    warnings.warn(f"Server-side error occurred: {response.status_code}, Try Number: {x+1}") 

                elif (response.status_code >= 400 and response.status_code <= 499):
                    if response.status_code == 400:
                        raise BadRequestError("Error " + str(response.status_code) + ": " + self._reason(response)) 
                    elif response.status_code == 401:
                        raise InvalidTokenError("Error " + str(response.status_code) + ": " + self._reason(response))
                    elif response.status_code == 403:
                        raise BadSlotError("Error " + str(response.status_code) + ": " + self._reason(response))
                    elif response.status_code == 404:
                        raise NotProcessedError("Error " + str(response.status_code) + ": " + self._reason(response))
                    elif response.status_code == 409:
                        raise SlotUnavailableError("Error " + str(response.status_code) + ": " + self._reason(response))
                    elif response.status_code == 451:
                        raise ReservationLimitError("Error " + str(response.status_code) + ": " + self._reason(response))
                    else:
                        raise HTTPError(f"Unexpected client-side error: {response.status_code}")

                else:
                    raise HTTPError(f"Unexpected status code: {response.status_code}")

            except requests.exceptions.RequestException as e:
                print(e)
                # warnings.warn(f"Request exception occurred: {str(e)}")

        raise Exception("Maximum number of retries exceeded")

    def get_slots_available(self):
        """Obtain the list of slots currently available in the system"""
        # Your code goes here
        endpoint = "/reservation/available"
        response = self._send_request("GET", endpoint)
        return response

    def get_slots_held(self):
        """Obtain the list of slots currently held by the client"""
        # Your code goes here
        endpoint = "/reservation"
        response = self._send_request("GET", endpoint)
        return response

    def release_slot(self, slot_id):
        """Release a slot currently held by the client"""
        # Your code goes here
        endpoint = f"/reservation/{slot_id}"
        response = self._send_request("DELETE", endpoint)
        return response

    def reserve_slot(self, slot_id):
        """Attempt to reserve a slot for the client"""
        # Your code goes here
        endpoint = f"/reservation/{slot_id}"
        response = self._send_request("POST", endpoint)
        return response