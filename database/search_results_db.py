from peewee import *
from datetime import datetime

db = SqliteDatabase('search_results_db.sqlite')

class BaseModel(Model):
    class Meta:
        database = db

class Artist(BaseModel):
    name = CharField(unique=True)
    img_url = CharField()
    date_created = DateField()

    def __str__(self):
        return f'{self.name}, {self.img_url}, {self.date_created}'

class Track(BaseModel):
    title = CharField(unique=True)
    album = CharField()
    release_date = CharField()
    spotify_url = CharField()
    date_created = DateField()
    artist = ForeignKeyField(Artist, backref='tracks')

    def __str__(self):
        return f'{self.title}, {self.album}, {self.release_date}, {self.spotify_url}, {self.date_created}'

class Genre(BaseModel):
    genre_name = CharField(unique=True)
    date_created = DateField()
    artist = ForeignKeyField(Artist, backref='genres')

    def __str__(self):
        return f'{self.genre_name}, {self.date_created}'

class Event(BaseModel):
    name = CharField(unique=True)
    event_date = DateField()
    venue = CharField()
    date_created = DateField()
    artist = ForeignKeyField(Artist, backref='events')

    def __str__(self):
        return f'{self.name}, {self.event_date}, {self.venue}, {self.date_created}'

class Video(BaseModel):
    video_name = CharField(unique=True)
    video_id = CharField(unique=True)
    thumbnail_url = CharField()
    date_created = DateField()
    artist = ForeignKeyField(Artist, backref='videos')

    def __str__(self):
        return f'{self.video_name}, {self.video_id}, {self.thumbnail_url}, {self.date_created}'

def create_tables():
    with db:
        db.create_tables([Artist, Track, Genre, Event, Video])

def delete_all_tables():
    with db:
        Artist.delete().execute()
        Track.delete().execute()
        Genre.delete().execute()
        Event.delete().execute()
        Video.delete().execute()

@db.connection_context()
def database_connection(spotify_data, events_info, music_video):
    try:
        create_tables()
        store_artist_info(spotify_data)
        store_track_info(spotify_data)
        store_genres(spotify_data)
        store_events_info(spotify_data, events_info)
        store_music_video_info(spotify_data, music_video)
    except Exception as e:
        print(f'{e}')

def store_artist_info(spotify_data):
    artist, created = Artist.get_or_create(
        name=spotify_data.artist,
        defaults={
            'img_url': spotify_data.image_url,
            'date_created': datetime.today()
        }
    )

    if created:
        print(f'Artist: {artist.name} saved! Storing tracks...')
    else:
        print(f'Artist: {artist.name} already in database. Storing tracks...')

def store_track_info(spotify_data):
    for title in spotify_data.tracks:
        track, created = Track.get_or_create(
            title=title['title'],
            defaults={'album': title['album'],
                      'release_date': title['release date'],
                      'spotify_url': title['spotify url'],
                      'date_created': datetime.today(),
                      'artist': spotify_data.artist}
        )

        if created:
            print(f'Track: {track.title} saved!')
        else:
            print(f'Track: {track.title} already in database.')

def store_genres(spotify_data):
    for genre in spotify_data.genres:
        genre_row, created = Genre.get_or_create(
            genre_name=genre,
            defaults={'date_created': datetime.today(),
                      'artist': spotify_data.artist}
        )

        if created:
            print(f'Genre: {genre} saved!')
        else:
            print(f'Genre: {genre} already in database.')

def store_events_info(artist, events):
    try:
        for event in events:
            name, created = Event.get_or_create(
                name=event['Event'],
                defaults={'event_date': event['Date'],
                          'venue': event['Venue'],
                          'date_created': datetime.today(),
                          'artist': artist.artist}
            )

            if created:
                print(f'Event: {name.event} saved!')
            else:
                print(f'Event: {name.event} already in database.')

    except Exception as error:
        print(f'Error saving events to database: {error}')

def store_music_video_info(artist, video):
    try:
        video_row, created = Video.get_or_create(
            video_name=video['video_title'],
            video_id=video['video_id'],
            defaults={
                'thumbnail_url': video['thumbnail'],
                'date_created': datetime.today(),
                'artist': artist.artist
            }
        )

        if created:
            print(f'Video: {video_row.video_name} saved!')
        else:
            print(f'Video: {video_row.video_name} already in database.')

    except Exception as error:
        print(f'Error saving music video to database: {error}')
