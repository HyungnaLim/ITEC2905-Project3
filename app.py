from flask import Flask, render_template, flash, redirect, session, request, url_for  # NOT the same as requests
import apis.spotify_api as spotify
import apis.youtube_api as video
import apis.ticketmaster_api as events

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
    artist = session.get('user_search')
    store_search_data(artist)
    flash(f'{artist['artist_name']} saved!')
    # TODO replace index with bookmarks.html or artist page
    return redirect(url_for('homepage'))

def store_search_data(artist):
    # TODO send to search_results_db
    # some_save_function_to_db(artist)
    print(f'Pretend saved {artist['artist_name']} to database!')

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