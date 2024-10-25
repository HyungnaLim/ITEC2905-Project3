from peewee import *
from datetime import datetime

db = SqliteDatabase('search_results_db.sqlite')

class BaseModel(Model):
    class Meta:
        database = db

class Artist(BaseModel):
    name = CharField(unique=True)
    img_url = CharField()
    date_created = DateTimeField()

    def __str__(self):
        return f'{self.name}, {self.img_url}, {self.date_created}'

    def get_genres(self):
        return (Artist
                .select()
                .join(Relationship, on=Relationship.to_genre)
                .where(Relationship.from_artist == self)
                .order_by(Artist.name))

class Track(BaseModel):
    title = CharField(unique=True)
    album = CharField()
    release_date = CharField()
    spotify_url = CharField()
    date_created = DateTimeField()
    artist = ForeignKeyField(Artist, backref='tracks')

    def __str__(self):
        return f'{self.title}, {self.album}, {self.release_date}, {self.spotify_url}, {self.date_created}'

class Genre(BaseModel):
    genre_name = CharField(unique=True)
    date_created = DateTimeField()

    def __str__(self):
        return f'{self.genre_name}, {self.date_created}'

class Event(BaseModel):
    name = CharField(unique=True)
    event_date = DateField()
    venue = CharField()
    date_created = DateTimeField()
    artist = ForeignKeyField(Artist, backref='events')

    def __str__(self):
        return f'{self.name}, {self.event_date}, {self.venue}, {self.date_created}'

class Video(BaseModel):
    video_name = CharField(unique=True)
    video_id = CharField(unique=True)
    thumbnail_url = CharField()
    date_created = DateTimeField()
    artist = ForeignKeyField(Artist, backref='videos')

    def __str__(self):
        return f'{self.video_name}, {self.video_id}, {self.thumbnail_url}, {self.date_created}'

class Relationship(BaseModel):
    from_artist = ForeignKeyField(Artist, backref='relationships')
    to_genre = ForeignKeyField(Genre, backref='related_to')

    class Meta:
        indexes = (
            (('from_artist', 'to_genre'), True),
        )

def create_tables():
    with db:
        db.create_tables([Artist, Track, Genre, Event, Video, Relationship])

def delete_all_tables():
    with db:
        Artist.delete().execute()
        Track.delete().execute()
        Genre.delete().execute()
        Event.delete().execute()
        Video.delete().execute()

@db.connection_context()
def database_connection(artist_data):
    print(artist_data)
    try:
        create_tables()
        store_artist_info(artist_data)
        store_track_info(artist_data)
        store_genres(artist_data)
        store_events_info(artist_data)
        store_music_video_info(artist_data)
    except Exception as e:
        print(f'{e}')

def store_artist_info(spotify_data):
    artist, created = Artist.get_or_create(
        name=spotify_data['artist_name'],
        defaults={
            'img_url': spotify_data['artist_img_url'],
            'date_created': datetime.now()
        }
    )

    if created:
        print(f'Artist: {artist.name} saved! Storing tracks...')
    else:
        print(f'Artist: {artist.name} already in database. Storing tracks...')

def store_track_info(spotify_data):
    for title in spotify_data['tracks']:
        track, created = Track.get_or_create(
            title=title['title'],
            defaults={'album': title['album'],
                      'release_date': title['release date'],
                      'spotify_url': title['spotify url'],
                      'date_created': datetime.now(),
                      'artist': spotify_data['artist_name']}
        )

        if created:
            print(f'Track: {track.title} saved!')
        else:
            print(f'Track: {track.title} already in database.')

def store_genres(spotify_data):
    for genre in spotify_data['artist_genre']:
        genre_row, created = Genre.get_or_create(
            genre_name=genre,
            defaults={'date_created': datetime.now()}
        )
        try:
            with db.atomic():
                Relationship.create(
                    from_artist=spotify_data['artist_name'],
                    to_genre=genre)
            print(f'{genre} relationship created.')
        except IntegrityError:
            print(f'{genre} relationship passed.')
            pass

        if created:
            print(f'Genre: {genre} saved!')
        else:
            print(f'Genre: {genre} already in database.')

def store_events_info(events):
    try:
        for event in events:
            name, created = Event.get_or_create(
                name=event['event_name'],
                defaults={'event_date': event['event_date'],
                          'venue': event['event_venue'],
                          'date_created': datetime.now(),
                          'artist': event['artist_name']}
            )

            if created:
                print(f'Event: {name.event} saved!')
            else:
                print(f'Event: {name.event} already in database.')

    except Exception as error:
        print(f'Error saving events to database: {error}')

def store_music_video_info(video):
    try:
        video_row, created = Video.get_or_create(
            video_name=video['video_title'],
            video_id=video['video_id'],
            defaults={
                'thumbnail_url': video['video_thumbnail'],
                'date_created': datetime.now(),
                'artist': video['artist_name']
            }
        )

        if created:
            print(f'Video: {video_row.video_name} saved!')
        else:
            print(f'Video: {video_row.video_name} already in database.')

    except Exception as error:
        print(f'Error saving music video to database: {error}')
