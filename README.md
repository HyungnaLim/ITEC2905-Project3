# Discover Artists!
- Uses <a ref="https://developer.spotify.com/documentation/web-api">Spotify</a>, <a ref="https://developers.google.com/youtube/v3/quickstart/python">YouTube</a>, and <a ref="https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/">Ticketmaster</a> APIs.
- This app allows users to search for music artists and view detailed information about them.
- Search result displays artist name, profile picture, genre, top tracks, music video for top track, related events
- If an exact match isn’t found, the app will display the closest matching artist to the search term.
- Some information may not be displayed if it is not found from API.

---

## Environment Variables

### Spotify:
- Create Spotify account and login to <a ref="https://developer.spotify.com/dashboard">developer site</a>.
- Follow instruction from <a ref="https://developer.spotify.com/documentation/web-api/tutorials/getting-started#create-an-app"> API documentation</a> to see your Client ID and Client secret.
- Add the following environment variables to your operating system:
- **SPOTIFY_ID** : Your client ID
- **SPOTIFY_SECRET** : Your client secret (click 'View client secret')

### Youtube:

### Ticketmaster:


---

## To install and run

### Windows:
1. Create a virtual environment:
`python -m venv venv`
2. Activate the virtual environment:
`venv\Scripts\Activate`
3. Install required packages:
`pip install -r requirements.txt`
4. Set flask app
`set FLASK_APP=app.py`
`set FLASK_DEBUG=1`
5. Run the application:
`flask run`
6. App will be running on http://127.0.0.1:5000


### Mac/Linux:
1. Create a virtual environment:
`python -m venv venv`
2. Activate the virtual environment:
`source venv/bin/activate`
3. Install required packages:
`pip install -r requirements.txt``
4. Set flask app
`export FLASK_APP=app.py`
`export FLASK_DEBUG=1`
5. Run the application:
`flask run`
(if not working try: `python app.py`)
6. App will be running on http://127.0.0.1:5000

---

## Tests
To run tests, use this command from the root directory of the project.

`python -m unittest discover tests`