import requests
from dotenv import load_dotenv
import os
import urllib.parse
import logging
load_dotenv()

class TicketmasterEvent:
    def __init__(self, name, date, venue):
        self.name = name
        self.date = date
        self.venue = venue

    def __str__(self):
        return f"Event: {self.name}, Date: {self.date}, Venue: {self.venue}"

class TicketmasterAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def search_events(self, search_term):
        encoded_search_term = urllib.parse.quote(search_term)
        events_url = (
            f'https://app.ticketmaster.com/discovery/v2/events.json'
            f'?apikey={self.api_key}'
            f'&keyword={encoded_search_term}'
            f'&size=5')

        try:
            response = requests.get(events_url)
            response.raise_for_status()
            return self.extract_events(response.json())

        except requests.exceptions.HTTPError as http_err:
            logging.exception(http_err)
            return None, f'HTTP error occurred: {http_err}'
        except Exception as err:
            logging.exception(err)
            return None, f'An error occurred: {err}'

    def extract_events(self, events_data):
        try:
            if '_embedded' in events_data and 'events' in events_data['_embedded']:
                events = []
                for event in events_data['_embedded']['events']:
                    name = event['name']
                    date = event['dates']['start']['localDate']
                    venue = event['_embedded']['venues'][0]['name']
                    events.append(TicketmasterEvent(name, date, venue))
                return events, None  # No error
            else:
                return None, "No events found."  # Return empty list and message
        except Exception as e:
            logging.exception(e)
            return None, f'Error processing events: {e}'

def main(search_term):
    TICKETMASTER_API_KEY = os.getenv('TICKETMASTER_API_KEY')
    if not TICKETMASTER_API_KEY:
        return None, "Error: API key is not set."

    ticketmaster = TicketmasterAPI(TICKETMASTER_API_KEY)
    events, error_message = ticketmaster.search_events(search_term)

    if error_message:
        return None, error_message
    return events, None

if __name__ == "__main__":
    search_term = input("Enter artist name to search for events: ")
    events, error = main(search_term)

    if error:
        print(error)
    else:
        for event in events:
            print(event)