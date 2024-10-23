from flask import Flask, render_template, flash, redirect, session, request, url_for  # NOT the same as requests
from peewee import *
import apis.spotify_api as spotify
import apis.youtube_api as video
import apis.ticketmaster_api as events

app = Flask(__name__)
db = SqliteDatabase('temp.db')

class TempSearch(Model):
    

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
    events_info = events.main(artist_name)
    music_video = video.main(f'{artist_info.artist} {artist_info.tracks[0]['title']}')

    return render_template('search_result.html',
                           artist_name=artist_info.artist,
                           artist_img=artist_info.image_url,
                           artist_genres=artist_info.genres_str(),
                           artist_tracks=artist_info.tracks_str(),
                           music_video=music_video,
                           events_info=events_info)



@app.route('/save_search', methods=['POST'])
def save_artist():
    artist = session.get('user_search')
    print(artist)
    store_search_data(artist)
    flash('Artist saved!')
    # replace index with bookmarks.html
    return redirect(url_for('index'))

def store_search_data(artist):
    # send to search_results_db
    # some_save_function_to_db(artist)
    print(f'Saved {artist}')

if __name__ == '__main__':
    app.run()