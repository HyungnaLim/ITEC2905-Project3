from flask import Flask, render_template, request  # NOT the same as requests
import apis.spotify_api as spotify
import apis.youtube_api as video
import apis.ticketmaster_api as events

app = Flask(__name__)

@app.route('/') # home page
def homepage():
    return render_template('index.html')

@app.route('/get_artist')
def get_artist_info():

    try:
        # get user info from an API (figure out which one)
        print('form data is', request.args)

        # this will read the artist that is being searched for
        artist_name = request.args.get('artist_name')

        artist_info = spotify.main(artist_name)

        if artist_info is None:
            print(f"Error: No artist found from spotify api")
            return render_template('error.html', error='Spotify API error: cannot get artist info')
        else:
            events_info = events.main(artist_name)
            music_video = video.main(f'{artist_info.artist} {artist_info.tracks[0]['title']}')

            return render_template('search_result.html',
                                   artist_name=artist_info.artist,
                                   artist_img=artist_info.image_url,
                                   artist_genres=artist_info.genres_str(),
                                   artist_track_one=artist_info.tracks[0],
                                   artist_track_two=artist_info.tracks[1],
                                   artist_track_three=artist_info.tracks[2],
                                   events_info=events_info,
                                   music_video=music_video)
    except Exception as e:
        # Handle unexpected errors
        print(f"An error occurred: {e} Please return to the main page")
        return render_template('error.html', error="An unexpected error occurred.")


if __name__ == '__main__':
    app.run()