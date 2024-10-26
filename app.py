from flask import Flask, render_template, flash, redirect, session, request, url_for  # NOT the same as requests
import apis.spotify_api as spotify
import apis.youtube_api as video
import apis.ticketmaster_api as events
import database.search_results_db as db
from database.sample_artist import placeholder
from database.search_results_db import Artist

app = Flask(__name__)

# https://flask.palletsprojects.com/en/3.0.x/quickstart/#sessions
app.secret_key = b'development_super_secret_key'

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

    results = data_constructor(artist_info, events_info, music_video)
    session['user_search'] = results

    return render_template('search_result.html',
                           artist_name=artist_info.artist,
                           artist_img=artist_info.image_url,
                           artist_genres=artist_info.genres_str(),
                           artist_tracks=artist_info.tracks_str(),
                           music_video=music_video,
                           events_info=events_info)

@app.route('/save_search', methods=['POST'])
def save_artist():
    artist_to_save = session.get('user_search')
    db.store_artist_data(artist_to_save)
    flash(f'{artist_to_save['artist_name']} saved!')
    # TODO replace index with bookmarks.html or artist page
    return redirect(url_for('artist', name=artist_to_save['artist_name']))

@app.route('/bookmark', methods=['GET', 'POST'])
def bookmarks():
    if request.method == 'POST':
        if request.form.get('action') == "Sample Page":
            sample = placeholder()
            # TODO sample.html can (should) be changed to search_results.html - avoid duplication
            return render_template('sample.html',
                                   artist_name=sample['artist_name'],
                                   artist_img=sample['artist_img_url'],
                                   artist_genres=sample['artist_genre'][0],
                                   artist_tracks=sample['tracks'],
                                   music_video=sample['video_title'],
                                   music_video_id=sample['video_id'],
                                   music_video_thumb=sample['video_thumbnail'],
                                   events_info=sample['event'][0])

        elif request.form.get('action') == "Saved Artists":
            stored_artists = db.get_all_artists()
            return render_template('bookmarks.html', artists=stored_artists)

@app.route('/artist/<name>')
def artist(name):
    chosen_artist = Artist.get(Artist.name == name)
    genres = db.get_genres(chosen_artist)
    tracks = db.get_tracks(chosen_artist)
    print(tracks)
    db_video = db.get_video(chosen_artist)
    db_events = db.get_events(chosen_artist)

    return render_template('sample.html',
                           artist_name=name,
                           artist_img=chosen_artist.img_url,
                           artist_genres=genres,
                           artist_tracks=tracks,
                           music_video=db_video['video_title'],
                           music_video_id=db_video['video_id'],
                           music_video_thumb=db_video['video_thumbnail'],
                           events_info=db_events
                           )

def data_constructor(artist_info, event_info, music_video):
    results = {
        'artist_name': artist_info.artist,
        'artist_img_url': artist_info.image_url,
        'artist_genre': artist_info.genres,
        'tracks': artist_info.tracks,
        'event_name': event_info.name,
        'event_date': event_info.date,
        'event_venue': event_info.venue,
        'video_title': music_video['video_title'],
        'video_id': music_video['video_id'],
        'video_thumbnail': music_video['thumbnail']
    }
    return results

if __name__ == '__main__':
    app.run()