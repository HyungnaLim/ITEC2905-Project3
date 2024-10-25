from flask import Flask, render_template, request  # NOT the same as requests
import apis.spotify_api as spotify
import apis.youtube_api as video
import apis.ticketmaster_api as events
from db.search_results_db import logger

app = Flask(__name__)

@app.route('/') # home page
def homepage():
    return render_template('index.html')

@app.route('/get_artist')
def get_artist_info():
    # get user info from an API (figure out which one)
    print('form data is', request.args)

    # this will read the artist that is being searched for
    artist_name = request.args.get('user_search_query')

    try:
        artist_info = spotify.main(artist_name)
        events_info = events.main(artist_info.artist)

        # artist_info, error_message = spotify.main(artist_name)
        # events_info, error_message = events.main(artist_info.artist)

        # api return format: (api_data, None)
        music_video, error_message = video.main(f'{artist_info.artist} {artist_info.tracks[0]['title']}')

        # first if-clause will trigger if api returns (None, error_message)
        if error_message:
            return render_template('error.html', message=error_message)

        return render_template('search_result.html',
                               artist_name=artist_info.artist,
                               artist_img=artist_info.image_url,
                               artist_genres=artist_info.genres_str(),
                               artist_track_one=artist_info.tracks[0],
                               artist_track_two=artist_info.tracks[1],
                               artist_track_three=artist_info.tracks[2],
                               music_video=music_video,
                               events_info=events_info)

    except Exception as e:
        logger.exception(e)
        return render_template('error.html', message=f'An unexpected error occurred: {e}')


if __name__ == '__main__':
    app.run()