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


    # Check get_artist_info() for no matching artist
    @patch('requests.get')
    def test_no_matching_artist(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'artists': {'items': [] } }
        mock_get.return_value = mock_response
        mock_token = {'Authorization': f'Bearer mock_access_token'}
        with self.assertRaises(Exception) as ex_context:
            get_artist_info(mock_token, '[=')
        self.assertEqual('No matching artist found.', str(ex_context.exception))


    # Test a happy case for get_top_tracks_by_artist_id() - valid token, valid artist id
    @patch('requests.get')
    def test_invalid_artist_id(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'tracks' : [
                { 'name':'track1', 'album':{'name':'album1', 'release_date':'2024-11-01'},
                  'external_urls':{'spotify':'url1'} },
                {'name': 'track2', 'album': {'name': 'album2', 'release_date': '2024-11-02'},
                 'external_urls': {'spotify': 'url2'}},
                {'name': 'track3', 'album': {'name': 'album3', 'release_date': '2024-11-03'},
                 'external_urls': {'spotify': 'url3'}}
            ]
        }
        mock_get.return_value = mock_response
        mock_token = {'Authorization': f'Bearer mock_access_token'}
        expected_response = [{'title':'track1', 'album':'album1', 'release date':'2024-11-01', 'spotify url': 'url1'},
                             {'title': 'track2', 'album': 'album2', 'release date': '2024-11-02',
                              'spotify url': 'url2'},
                             {'title': 'track3', 'album': 'album3', 'release date': '2024-11-03',
                              'spotify url': 'url3'}
                             ]
        self.assertEqual(get_top_tracks_by_artist_id(mock_token, 'mock_id'), expected_response)


    # Check get_top_tracks_by_artist_id() for a response with one tracks
    @patch('requests.get')
    def test_only_one_track(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'tracks' : [
                { 'name':'track1', 'album':{'name':'album1', 'release_date':'2024-11-01'},
                  'external_urls':{'spotify':'url1'} }
            ]
        }
        mock_get.return_value = mock_response
        mock_token = {'Authorization': f'Bearer mock_access_token'}
        expected_response = [{'title':'track1', 'album':'album1', 'release date':'2024-11-01', 'spotify url': 'url1'}]
        self.assertEqual(get_top_tracks_by_artist_id(mock_token, 'mock_id'), expected_response)


    # Check get_top_tracks_by_artist_id() for a response with no tracks
    @patch('requests.get')
    def test_no_tracks(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = { 'tracks': [] }
        mock_get.return_value = mock_response
        mock_token = {'Authorization': f'Bearer mock_access_token'}
        self.assertEqual(get_top_tracks_by_artist_id(mock_token, 'mock_id'), [])


    # Test exception handling for main()
    @patch('requests.post')
    def test_main_exception_handling(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response
        artist_info, error = main('artist name')
        expected_error_message = 'Spotify API error: could not get valid token, check your client credentials.'
        self.assertIsNone(artist_info)
        self.assertEqual(error, expected_error_message)