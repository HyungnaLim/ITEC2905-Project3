from flask import Flask, render_template, flash, redirect, session, request, url_for  # NOT the same as requests
import apis.spotify_api as spotify
import apis.youtube_api as video
import apis.ticketmaster_api as events
import database.search_results_db as db
from database.sample_artist import placeholder
from database.search_results_db import Artist
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

# https://flask.palletsprojects.com/en/3.0.x/quickstart/#sessions
app.secret_key = b'development_super_secret_key'


@app.route('/') # home page
def homepage():
    return render_template('index.html')

    """ This renders the homepage
    
    Returns:
        The rendered HTML template on the homepage
    """


@app.route('/get_artist')
def get_artist_info():
    # get user info from an API (figure out which one)

    """Display information about the artist

    Using the Spotify & Ticketmaster API's, this will retreive artist 
    name from the parameters and on the search result page it will
    render the results

    Returns:
        HTML's rendered template to serach for the artist or error page
    """

    print('form data is', request.args)

    # this will read the artist that is being searched for
    artist_name = request.args.get('user_search_query')

    try:
        artist_info, spotify_error = spotify.main(artist_name)
        if spotify_error:
            return render_template('error.html', message=spotify_error)

        # events_info = events.main(artist_info.artist)
        events_info, error_message = events.main(artist_info.artist)
        if error_message:
            return render_template('error.html', message=error_message)

        # api return format: (api_data, None)
        music_video, youtube_error_message = video.main(f'{artist_info.artist} {artist_info.tracks[0]['title']}')

        # first if-clause will trigger if api returns (None, error_message)
        if youtube_error_message:
            return render_template('error.html', message=error_message)

        results = data_constructor(artist_info, events_info, music_video)
        session['user_search'] = results

        if artist_name.lower() != artist_info.artist.lower():
            flash('Displaying closest match to search term')

        return render_template('search_result.html',
                               artist_name=artist_info.artist,
                               artist_img=artist_info.image_url,
                               artist_genres=artist_info.genres_str(),
                               artist_track_one=artist_info.tracks[0] if len(artist_info.tracks) > 0 else None,
                               artist_track_two=artist_info.tracks[1] if len(artist_info.tracks) > 1 else None,
                               artist_track_three=artist_info.tracks[2] if len(artist_info.tracks) > 2 else None,
                               music_video=music_video,
                               events_info=events_info)


    except Exception as e:
        logger.exception(e)
        return render_template('error.html', message=f'An unexpected error occurred: {e}')


@app.route('/bookmark', methods=['GET', 'POST'])
def bookmarks():

    """This will handle bookmarks for artist actions

    For the POST requests
    it will render a sample artist page only if the sample page is requested
    it will render a list of saved artists only if saved artists is requested

    Returns:
        This will render the HTML template for both sample artist page or 
        the saved artist 
    
    """

    if request.method == 'POST':
        if request.form.get('action') == "Sample Page":
            sample = placeholder()
            print(sample['event'])
            # TODO sample.html can (should) be changed to search_results.html - avoid duplication
            return render_template('sample.html',
                                   artist_name=sample['artist_name'],
                                   artist_img=sample['artist_img_url'],
                                   artist_genres=sample['artist_genre'][0],
                                   artist_tracks=sample['tracks'],
                                   music_video=sample['video_title'],
                                   music_video_id=sample['video_id'],
                                   music_video_thumb=sample['video_thumbnail'],
                                   events=sample['event'])

        elif request.form.get('action') == "Saved Artists":
            stored_artists = db.get_all_artists()
            return render_template('bookmarks.html', artists=stored_artists)


@app.route('/save_search', methods=['POST'])
def save_artist():

    """This will save the current artist search to the database

    Stores the result of what was searched in the database of that session

    Return:
        This will redirect back to thee saved artist's detail page 
    """


    artist_to_save = session.get('user_search')
    db.store_artist_data(artist_to_save)
    flash(f'{artist_to_save['artist_name']} saved!')
    return redirect(url_for('artist', name=artist_to_save['artist_name']))


@app.route('/artist/<name>')
def artist(name):

    """Display the saved artist information

    Will retrieve a saved artist in the database along with their genre, tracks,
    videos and events

    Returns:
        Rendered HTML template with artist information
    
    """

    chosen_artist = Artist.get(Artist.name == name)
    genres = db.get_genres(chosen_artist)
    tracks = db.get_tracks(chosen_artist)
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
                           events=db_events)


def data_constructor(artist_info, event, music_video):

    """Artist data into a dictionary for storage

    Artist data rerieved from Spotify API
    Event data retrieved from Ticketmaster API
    Video data retrieved from YouTube API

    Returns:
        dictionary containing artist data
    
    """

    results = {
        'artist_name': artist_info.artist,
        'artist_img_url': artist_info.image_url,
        'artist_genre': artist_info.genres,
        'tracks': artist_info.tracks,
        'event': f'{event}',
        'video_title': music_video['video_title'],
        'video_id': music_video['video_id'],
        'video_thumbnail': music_video['thumbnail']
    }
    return results


if __name__ == '__main__':
    app.run()