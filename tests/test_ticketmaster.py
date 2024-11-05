import sys
import os

# Add the 'apis' directory to sys.path so Python can find it
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'apis')))

# import TicketmasterAPI and TicketmasterEvent as normal
from ticketmaster_api import TicketmasterAPI, TicketmasterEvent # type: ignore


import unittest
from unittest.mock import patch, Mock

class TestTicketmasterAPI(unittest.TestCase):

    # Example test for search_events (success case)
    @patch('requests.get')
    def test_search_events_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "_embedded": {
                "events": [
                    {
                        "name": "Test Event",
                        "dates": {
                            "start": {
                                "localDate": "2024-12-25"
                            }
                        },
                        "_embedded": {
                            "venues": [{"name": "Test Venue"}]
                        }
                    }
                ]
            }
        }
        mock_get.return_value = mock_response

        api = TicketmasterAPI("dummy_api_key")
        events, error_message = api.search_events("Test Artist")
        
        self.assertIsNone(error_message)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].name, "Test Event")

    
    
if __name__ == '__main__':
    unittest.main()