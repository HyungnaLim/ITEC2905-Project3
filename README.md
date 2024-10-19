# ITEC2905-Project3

set up

windows:
1. python -m venv apitestvenv
2. apitestvenv\Scripts\Activate
3. pip install -r requirements.txt
4. set FLASK_APP=app.py
5. set FLASK_DEBUG=1
6. flask run

mac/linux:
1. python -m venv apitestvenv
2. source apitestvenv/bin/activate
3. pip install -r requirements.txt
4. export FLASK_APP=app.py
5. export FLASK_DEBUG=1
6. flask run (if not working try: python app.py)
