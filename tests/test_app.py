import unittest
from app import app

class FakeAPI:
    def main(self, service, artist_name_or_query):
        if service == 'spotify':
            return FakeSpotifyArtist(
                artist="Test Artist",
                image_url="https://example.com/artist.jpg",
                tracks=[{"title": "Song 1"}, {"title": "Song 2"}, {"title": "Song 3"}],
                genres=lambda: "Pop, Rock" #fake genre
            )
        elif service == 'youtube':
            return "https://youtube.com/test_video"
        elif service == 'events':
            return "Test Event Information"


class FakeSpotifyArtist:
    def __init__(self, artist, image_url, tracks, genres):
        self.artist = artist
        self.image_url = image_url
        self.tracks = tracks
        self.genres = genres


class TestCase(unittest.TestCase):

    # This will set up the Flask test client and fake API client
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.fake_api = FakeAPI()

    # This will set up the homepage route
    def test_homepage(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<!DOCTYPE html>', response.data)


    def test_get_artist_info(self):
        response = self.app.get('/get_artist')
        self.assertEqual(response.status_code, 200)
        artist_info = self.fake_api.main('spotify', 'Test Artist')
        self.assertGreaterEqual(len(artist_info.tracks), 3, "Tracks to test")


if __name__ == '__main__':
    unittest.main()