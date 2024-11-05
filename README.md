# ITEC2905-Project3

## Environment Variables

### Spotify:
- Create Spotify account and login to <a ref="https://developer.spotify.com/dashboard">developer site</a>.
- Follow instruction from <a ref="https://developer.spotify.com/documentation/web-api/tutorials/getting-started#create-an-app"> API documentation</a> to see your Client ID and Client secret.
- Add the following environment variables to your operating system:
- **SPOTIFY_ID** : Your client ID
- **SPOTIFY_SECRET** : Your client secret (click 'View client secret')

### Youtube

### Ticketmaster


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

---

## Tests