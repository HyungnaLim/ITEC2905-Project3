from flask import Flask, render_template, request  # NOT the same as requests
import apis.spotify_api as spotify
import apis.youtube_api as video
import apis.ticketmaster_api as events
import database.search_results_db as db

app = Flask(__name__)

def store_info(artist_info, events_info, music_video):
    db.database_connection(artist_info, events_info, music_video)

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
    events_info = events.main(artist_info.artist)
    music_video = video.main(f'{artist_info.artist} {artist_info.tracks[0]['title']}')

    # uncomment below to store ALL searches to database
    store_info(artist_info, events_info, music_video)

    return render_template('search_result.html',
                           artist_name=artist_info.artist,
                           artist_img=artist_info.image_url,
                           artist_genres=artist_info.genres_str(),
                           artist_tracks=artist_info.tracks_str(),
                           music_video=music_video,
                           events_info=events_info)




if __name__ == '__main__':
    app.run()