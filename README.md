# ITEC2905-Project3

## Environment Variables:
Add the following environment variables for the API to your operating system:

- SPOTIFY_ID : `0c5ba66cb29e46e8a415a35c19033bdd`
- SPOTIFY_SECRET : `280da5fed992434abc6598b3beadb449`
- TICKETMASTER_API_KEY : `GSODZqdDGBo7UGEzXzglQDxeo3fhhdW5`
- DEVELOPER_KEY : `AIzaSyDwqLyFMv40cYjRW8jUEQyBgD-nvxR_PwY`

## Windows:
1. Create a virtual environment:
```bash 
python -m venv venv
```
2. Activate the virtual environment:
```bash
venv\Scripts\Activate
```
3. Install required packages:
```bash
pip install -r requirements.txt
```
4. Set flask app
```bash
set FLASK_APP=app.py
set FLASK_DEBUG=1
```
5. Run the application:
```bash
flask run
````

## Mac/Linux:
1. Create a virtual environment:
```bash 
python -m venv venv
```
2. Activate the virtual environment:
```bash
source venv/bin/activate
```
3. Install required packages:
```bash
pip install -r requirements.txt
```
4. Set flask app
```bash
export FLASK_APP=app.py
export FLASK_DEBUG=1
```
5. Run the application (if not working try: python app.py):
```bash
flask run
````