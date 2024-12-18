from flask import Flask, render_template, flash, redirect, session, request, url_for  # NOT the same as requests
import apis.spotify_api as spotify
import apis.youtube_api as video
import apis.ticketmaster_api as events
import database.search_results_db as db
from database.sample_artist import placeholder
from database.search_results_db import Artist
import logging
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
logger = logging.getLogger(__name__)

# https://flask.palletsprojects.com/en/3.0.x/quickstart/#sessions
app.secret_key = b'SESSION_KEY'


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/get_artist')
def get_artist_info():
    try:
        artist_name = request.args.get('user_search_query')
        artist_info, spotify_error = spotify.main(artist_name)
        if spotify_error:
            raise Exception(spotify_error)

        events_info, event_error_message = events.main(artist_info.artist)
        music_video, youtube_error_message = video.main(f'{artist_info.artist} {artist_info.tracks[0]['title']}')
        error_logging([event_error_message, youtube_error_message])

        create_session(artist_info, events_info, music_video)

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
        return render_template('error.html', message=f'An app error occurred: {e}')


@app.route('/bookmark', methods=['GET', 'POST'])
def bookmarks():
    if request.method == 'POST':
        if request.form.get('action') == "Sample Page":
            sample = placeholder()
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
    artist_to_save = session.get('user_search')
    db.store_artist_data(artist_to_save)
    flash(f'{artist_to_save['artist_name']} saved!')
    return redirect(url_for('artist', name=artist_to_save['artist_name']))


@app.route('/artist/<name>')
def artist(name):
    chosen_artist = Artist.get(Artist.name == name)
    genres = db.get_genres(chosen_artist)
    tracks = db.get_tracks(chosen_artist)
    db_video = db.get_video(chosen_artist)
    db_events = db.get_events(chosen_artist)

    return render_template('saved_artist.html',
                           artist_name=name,
                           artist_img=chosen_artist.img_url,
                           artist_genres=genres,
                           artist_tracks=tracks,
                           music_video=db_video['video_title'],
                           music_video_id=db_video['video_id'],
                           music_video_thumb=db_video['video_thumbnail'],
                           events=db_events)


def create_session(artist_session, event_session, video_session):
    results = data_constructor(artist_session, event_session, video_session)
    session['user_search'] = results


def data_constructor(artist_info, event, music_video):
    if event:
        events_li = []
        for e in event:
            x = {
                'event': e.name,
                'date': e.date,
                'venue': e.venue,
            }
            events_li.append(x)

        if music_video:
            results = {
                'artist_name': artist_info.artist,
                'artist_img_url': artist_info.image_url,
                'artist_genre': artist_info.genres,
                'tracks': artist_info.tracks,
                'events': events_li,
                'video_title': music_video['video_title'],
                'video_id': music_video['video_id'],
                'video_thumbnail': music_video['thumbnail']
            }
            return results

        else:
            results = {
                'artist_name': artist_info.artist,
                'artist_img_url': artist_info.image_url,
                'artist_genre': artist_info.genres,
                'tracks': artist_info.tracks,
                'events': events_li
            }
            return results

    elif music_video:
        results = {
            'artist_name': artist_info.artist,
            'artist_img_url': artist_info.image_url,
            'artist_genre': artist_info.genres,
            'tracks': artist_info.tracks,
            'video_title': music_video['video_title'],
            'video_id': music_video['video_id'],
            'video_thumbnail': music_video['thumbnail']
        }
        return results

    else:
        results = {
            'artist_name': artist_info.artist,
            'artist_img_url': artist_info.image_url,
            'artist_genre': artist_info.genres,
            'tracks': artist_info.tracks
        }
        return results


def error_logging(messages):
    for m in messages:
        if m:
            logger.error(m)


if __name__ == '__main__':
    app.run()