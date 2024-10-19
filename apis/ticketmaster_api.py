import requests
import os
import urllib.parse

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
        events_url = f'https://app.ticketmaster.com/discovery/v2/events.json?apikey={self.api_key}&keyword={encoded_search_term}&size=1'

        try:
            response = requests.get(events_url)
            response.raise_for_status()
            events_data = response.json()

            if '_embedded' in events_data and 'events' in events_data['_embedded']:
                events = []
                for event in events_data['_embedded']['events']:
                    name = event['name']
                    date = event['dates']['start']['localDate']
                    venue = event['_embedded']['venues'][0]['name']
                    events.append(TicketmasterEvent(name, date, venue))
                return events
            else:
                return {'error': 'No events found'}

        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            return {'error': str(http_err)}
        except Exception as err:
            print(f'An error occurred: {err}')
            return {'error': str(err)}

def main(search_term):
    TICKETMASTER_API_KEY = os.getenv('TICKETMASTER_API_KEY', 'GSODZqdDGBo7UGEzXzglQDxeo3fhhdW5')
    ticketmaster = TicketmasterAPI(TICKETMASTER_API_KEY)

    # search_term = input("Enter artist name to search for events: ")
    events = ticketmaster.search_events(search_term)

    if isinstance(events, list):
        for event in events:
            # print(event)
            return event
    else:
        # print(events)
        return events