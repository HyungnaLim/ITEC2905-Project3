from peewee import *
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)
db_path = os.path.join('database', 'search_results_db.sqlite')
db = SqliteDatabase(db_path)


class BaseModel(Model):
    class Meta:
        database = db


class Artist(BaseModel):
    name = CharField(unique=True)
    img_url = CharField()
    date_created = DateTimeField()

    def __str__(self):
        return f'{self.name}, {self.img_url}, {self.date_created}'

    def genre_relationship(self):
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
    genre_name = CharField(unique=True, null=True)
    date_created = DateTimeField()
    artist = ForeignKeyField(Artist, backref='genres')

    def __str__(self):
        return f'{self.genre_name}, {self.date_created}'


class Event(BaseModel):
    name = CharField(null=True)
    date = CharField(null=True)
    venue = CharField(null=True)
    date_created = DateTimeField()
    artist = ForeignKeyField(Artist, backref='events')

    def __str__(self):
        return f'{self.name}, {self.date}, {self.venue}, {self.date_created}'


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
def store_artist_data(artist_data):
    try:
        create_tables()
        # artist must be stored as db object for backref to work
        artist = store_artist_info(artist_data)
        store_track_info(artist, artist_data)
        store_genres(artist, artist_data)
        store_events_info(artist, artist_data)
        store_music_video_info(artist, artist_data)
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
        print(f'Artist: {artist.name} saved!')
        return artist
    else:
        print(f'Artist: {artist.name} already in database.')
        return artist


def store_track_info(artist, spotify_data):
    for title in spotify_data['tracks']:
        track, created = Track.get_or_create(
            title=title['title'],
            defaults={'album': title['album'],
                      'release_date': title['release date'],
                      'spotify_url': title['spotify url'],
                      'date_created': datetime.now(),
                      'artist': artist}
        )
        if created:
            print(f'Track: {track.title} saved!')
        else:
            print(f'Track: {track.title} already in database.')


def store_genres(artist, spotify_data):
    for genre in spotify_data['artist_genre']:
        genre_row, created = Genre.get_or_create(
            genre_name=genre,
            defaults={'date_created': datetime.now(),
                      'artist': artist}
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


def store_events_info(artist, artist_data):
    for e in artist_data['events']:
        try:
            name, created = Event.get_or_create(
                name=e['event'],
                date=e['date'],
                venue=e['venue'],
                defaults={
                    # 'date': e['date'],
                    # 'venue': e['venue'],
                    'date_created': datetime.now(),
                    'artist': artist
                }
            )
            if created:
                print(f'Event: {name} saved!')
            else:
                print(f'Event: {name} already in database.')

        except Exception as error:
            print(f'Error saving events to database: {error}')


def store_music_video_info(artist, video):
    try:
        video_row, created = Video.get_or_create(
            video_name=video['video_title'],
            video_id=video['video_id'],
            defaults={
                'thumbnail_url': video['video_thumbnail'],
                'date_created': datetime.now(),
                'artist': artist
            }
        )
        if created:
            print(f'Video: {video_row.video_name} saved!')
        else:
            print(f'Video: {video_row.video_name} already in database.')

    except Exception as error:
        print(f'Error saving music video to database: {error}')


def get_all_artists():
    create_tables()
    return (Artist
            .select()
            .order_by(Artist.date_created))


def get_artist(artist):
    return {
        'artist_name': artist.name,
        'artist_img_url': artist.img_url,
    }


def get_tracks(artist):
    track_li = []
    for track in artist.tracks:
        a_track = {
            'title': track.title,
            'album': track.album,
            'release_date': track.release_date,
            'spotify_url': track.spotify_url,
            'date_created': track.date_created
        }
        track_li.append(a_track)
    return track_li


def get_genres(artist):
    genre_li = []
    for g in artist.genres:
        genre_li.append(g.genre_name)
    genres = ', '.join(genre_li)
    return genres


def get_events(artist):
    events = []
    for event in artist.events:
        x = {
            'name': event.name,
            'date': event.date,
            'venue': event.venue,
        }
        events.append(x)
    return events


def get_video(artist):
    video = {}
    for v in artist.videos:
        video['video_title'] = v.video_name
        video['video_id'] = v.video_id
        video['video_thumbnail'] = v.thumbnail_url
    return video
