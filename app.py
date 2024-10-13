from flask import Flask, render_template, request  # NOT the same as requests
import api.spotify_api as spotify

app = Flask(__name__)

@app.route('/') # home page
def homepage():
    return render_template('index.html')

@app.route('/get_artist')
def get_artist_info():
    # get artist info from spotify api and display on new page
    # print('form data is', request.args)
    artist_search = request.args.get('artist_search')
    artist_info = spotify.main(artist_search)   # artist_info will be dictionary
    return render_template('artist_info_page.html', spotify_search=artist_info)


if __name__ == '__main__':
    app.run()
