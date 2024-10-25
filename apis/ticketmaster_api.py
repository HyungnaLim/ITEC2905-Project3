import requests
import os
import urllib.parse

class TicketmasterEvent:
    def __init__(self, name, date, venue, artist):
        self.name = name
        self.date = date
        self.venue = venue
        self.artist = artist

    def __str__(self):
        return f"Event: {self.name} by {self.artist}, Date: {self.date}, Venue: {self.venue}"

class TicketmasterAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def search_events(self, search_term, size=20):
        encoded_search_term = urllib.parse.quote(search_term)
        page = 0
        all_events = []

        while True:
            events_url = (f'https://app.ticketmaster.com/discovery/v2/events.json?apikey={self.api_key}&keyword={encoded_search_term}'
                           f'&size={size}&page={page}')

            try:
                response = requests.get(events_url)
                response.raise_for_status()
                events_data = response.json()

                if '_embedded' in events_data and 'events' in events_data['_embedded']:
                    for event in events_data['_embedded']['events']:
                        name = event['name']
                        date = event['dates']['start'].get('localDate', 'N/A')
                        venue = event['_embedded']['venues'][0]['name']

                        # Attempt to extract artist name if available
                        artist = ''
                        if '_embedded' in event and 'attractions' in event['_embedded']:
                            artist = ', '.join(attraction['name'] for attraction in event['_embedded']['attractions'])

                        all_events.append(TicketmasterEvent(name, date, venue, artist))

                    # Check for pagination
                    if 'page' in events_data and events_data['page'].get('hasNext', False):
                        page += 1
                    else:
                        break
                else:
                    print("No events found.")
                    break

            except requests.exceptions.HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
                return {'error': str(http_err)}
            except Exception as err:
                print(f'An error occurred: {err}')
                return {'error': str(err)}

        return all_events

def main(search_term):
    TICKETMASTER_API_KEY = os.getenv('TICKETMASTER_API_KEY', 'GSODZqdDGBo7UGEzXzglQDxeo3fhhdW5')
    ticketmaster = TicketmasterAPI(TICKETMASTER_API_KEY)

    events = ticketmaster.search_events(search_term, size=50)

    if isinstance(events, list) and events:
        for event in events:
            print(event)
    else:
        print(events)

if __name__ == "__main__":
    artist_name = input("Enter artist name to search for events: ")
    main(artist_name)