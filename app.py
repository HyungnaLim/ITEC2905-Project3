from flask import Flask, render_template, request  # NOT the same as requests
import api.spotify as spotify

app = Flask(__name__)

@app.route('/') # home page
def homepage():
    return render_template('index.html')

@app.route('/get_artist')
def get_artist_info():
    # get user info from an API (figure out which one)
    print('form data is', request.args)

    # this will read the artist that is being searched for
    artist_name = request.args.get('artist_name')

    artist_info = spotify.main(artist_name)

    return render_template('search_result.html', artist_info=artist_info)


if __name__ == '__main__':
    app.run()