import unittest
from unittest.mock import patch, Mock
from apis.spotify_api import *


class TestSpotify(unittest.TestCase):

    # Check get_token() with invalid credential
    @patch.dict('os.environ', {'SPOTIFY_ID': 'teststring', 'SPOTIFY_SECRET': 'teststring'})
    @patch('apis.spotify_api.requests.post')
    def test_invalid_credentials(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        with self.assertRaises(Exception) as ex_context:
            get_token()
        self.assertEqual('could not get valid token, check your client credentials.', str(ex_context.exception))

    # Check get_token() with no environment variables
    @patch.dict('os.environ', {'SPOTIFY_ID': '', 'SPOTIFY_SECRET': ''})
    def test_no_env(self):
        with self.assertRaises(Exception) as ex_context:
            get_token()
        self.assertEqual('could not find environment variables, check your OS environment variables', str(ex_context.exception))

    # TODO test cases:
    #  get_artist_info() for no matching artist
    #  get_top_tracks_by_artist_id() with invalid artist_id
    #  get_top_tracks_by_artist_id() with no tracks
    #  main() happy case