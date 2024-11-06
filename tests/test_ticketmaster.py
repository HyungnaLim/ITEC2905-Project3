import sys
import os
import requests  # Import requests to fix the NameError

# Add the parent directory of 'tests' (the root directory of the project) to sys.path
project_root = os.path.dirname(os.path.abspath(__file__))  # Get the directory of this test file
project_root = os.path.abspath(os.path.join(project_root, '..'))  # Go one directory up
sys.path.append(project_root)  # Add project root to Python path

# Now we can import TicketmasterAPI from the 'apis' directory
from apis.ticketmaster_api import TicketmasterAPI, TicketmasterEvent
import unittest
from unittest.mock import patch

class TestTicketmasterAPI(unittest.TestCase):

    @patch('apis.ticketmaster_api.requests.get')
    def test_search_events_success(self, mock_get):
        # Prepare mock response data for a successful request
        mock_response = {
            '_embedded': {
                'events': [
                    {
                        'name': 'Event 1',
                        'dates': {'start': {'localDate': '2024-01-01'}},
                        '_embedded': {
                            'venues': [{'name': 'Venue 1'}]
                        }
                    },
                    {
                        'name': 'Event 2',
                        'dates': {'start': {'localDate': '2024-02-01'}},
                        '_embedded': {
                            'venues': [{'name': 'Venue 2'}]
                        }
                    }
                ]
            }
        }
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200
        
        # Instantiate the API and call the method
        api = TicketmasterAPI(api_key='mock_api_key')
        events, error_message = api.search_events('artist_name')
        
        # Check that events are returned and no error message
        self.assertEqual(len(events), 2)
        self.assertIsNone(error_message)
        self.assertEqual(events[0].name, 'Event 1')  # Access the 'name' attribute of the event
        self.assertEqual(events[1].name, 'Event 2')

    @patch('apis.ticketmaster_api.requests.get')
    def test_search_events_http_error(self, mock_get):
        # Simulate an HTTP error
        mock_get.side_effect = requests.exceptions.HTTPError("HTTP error")
        
        api = TicketmasterAPI(api_key='mock_api_key')
        events, error_message = api.search_events('artist_name')
        
        # Assert that the error message corresponds to the HTTP error
        self.assertIsNone(events)
        self.assertEqual(error_message, "HTTP error occurred: HTTP error")

    @patch('apis.ticketmaster_api.requests.get')
    def test_search_events_no_results(self, mock_get):
        # Simulate no results being found
        mock_response = {
            '_embedded': {
                'events': []
            }
        }
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200
        
        api = TicketmasterAPI(api_key='mock_api_key')
        events, error_message = api.search_events('artist_name')
        
        # Assert that events is an empty list and error_message is as expected
        self.assertIsNone(error_message)
        self.assertEqual(events, [])

if __name__ == '__main__':
    unittest.main()