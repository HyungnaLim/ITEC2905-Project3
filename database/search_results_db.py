from peewee import *
from datetime import date, datetime
import logging

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
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
    genre = ForeignKeyField(Track, unique=True)

    def __str__(self):
        return f'{self.genre}'

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
        db.create_tables([Artist, Track, Event, Video])

def delete_tables():
    with db:
        Artist.delete().execute()
        Track.delete().execute()
        Event.delete().execute()
        Video.delete().execute()

@db.connection_context()
def database_connection(spotify_data, events_info, music_video):
    try:
        create_tables()
        store_artist_info(spotify_data)
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
        print(f'{artist.name} saved! Storing tracks...')
        store_track_info(spotify_data)
    else:
        print(f'{artist.name} already in database. Storing tracks...')
        store_track_info(spotify_data)

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
            print(f'{track.title} stored!')
        else:
            print(f'{track.title} already in database.')

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
                print(f'{name.event} record created!')
            else:
                print(f'{name.event} already in database.')

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
            print(f'{video_row.video_name} video saved!')
        else:
            print(f'{video_row.video_name} video already in database.')

    except Exception as error:
        print(f'Error saving music video to database: {error}')

def display_all_artists():
    artists = Artist.select()
    for artist in artists:
        print(artist)

def display_all_tracks():
    tracks = Track.select()
    for track in tracks:
        print(f'{track.title} - {track.artist_id}, {track.album}, {track.release_date}, '
              f'{track.spotify_url}, {track.date_created}')

def main():
    db.connect()
    menu_text = """
        1. Add sample data
        2. Display all artists
        3. Display all tracks
        4. Delete and create fresh tables
        2. Search by name
        3. Add new search result
        4. Edit existing table
        5. Delete record 
        9. Quit
        """

    while True:
        print(menu_text)
        choice = input('Enter your choice: ')
        if choice == '1':
            sample_data()
        elif choice == '2':
             display_all_artists()
        elif choice == '3':
            display_all_tracks()
        elif choice == '4':
            delete_create_tables()
        # elif choice == '4':
        #     edit_existing_record()
        # elif choice == '5':
        #     delete_record()
        elif choice == '9':
            delete_create_tables()
            db.close()
            break
        else:
            print('Not a valid selection, please try again')

def sample_data():
    radiohead = Artist(name='Radiohead', img_url='url', date_created=date.today())
    radiohead.save()

    track = Track(artist=radiohead.name, title='Creep', release_date='02/22/93', album='Pablo Honey',
                  spotify_url='url', date_created=date.today())
    track.save()

    oasis = Artist(name='Oasis', img_url='url', date_created=date.today())
    oasis.save()

    oasis_track = Track(artist=oasis.name, title='Wonderwall', release_date='1995',
                        album='(Whats The Story) Morning Glory?', spotify_url='url2',
                        date_created=date.today())
    oasis_track.save()

    print('created!')

def delete_create_tables():
    delete_tables()
    create_tables()

if __name__ == '__main__':
    create_tables()
    main()