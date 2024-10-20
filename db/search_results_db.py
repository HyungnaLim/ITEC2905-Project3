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

class Album(BaseModel):
    name = CharField(unique=True)
    date_created = DateField()
    artist = ForeignKeyField(Artist, backref='albums')

    def __str__(self):
        return f'{self.name}, {self.date_created}'

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

Artist.delete().execute()
Album.delete().execute()
Track.delete().execute()

def main():
    menu_text = """
        1. Add sample data
        2. Display all artists
        3. Display all albums
        4. Display all tracks
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
            display_all_albums()
        elif choice == '4':
            display_all_tracks()
        # elif choice == '4':
        #     edit_existing_record()
        # elif choice == '5':
        #     delete_record()
        elif choice == '9':
            break
        else:
            print('Not a valid selection, please try again')

def store_artist_info(spotify_data):
    print(spotify_data)
    artist, created = Artist.get_or_create(
        name=spotify_data.artist,
        defaults={'img_url': spotify_data.image_url, 'date_created': datetime.today()}
    )
    if created:
        print(f'{artist} saved!. Storing tracks...')
        store_track_info(spotify_data)
    else:
        print(f'{artist} already in database. Storing tracks...')
        store_track_info(spotify_data)

def store_track_info(spotify_data):
    for title in spotify_data.tracks['title']:
        track, created = Track.get_or_create(
            name=title,
            defaults={'album': spotify_data.tracks['album'],
                      'release_date': spotify_data.tracks['release date'],
                      'spotify_url': spotify_data.tracks['spotify url'],
                      'date_created': datetime.today(),
                      'artist': spotify_data.artist}
        )
        if created:
            print(f'{track} stored!')
        else:
            print(f'{track} already in database.')

def display_all_artists():
    artists = Artist.select()
    for artist in artists:
        print(artist)

def display_all_albums():
    # might be inefficient, but only way I found to work
    albums = Album.select()
    for album in albums:
        print(f'{album.artist_id}: ', album)

def display_all_tracks():
    tracks = Track.select()
    for track in tracks:
        print(f'{track.title} - {track.artist_id}, {track.album}, {track.release_date}, '
              f'{track.spotify_url}, {track.date_created}')

def sample_data():
    radiohead = Artist(name='Radiohead', img_url='url', date_created=date.today())
    radiohead.save()

    album = Album(artist=radiohead.name, name='Pablo Honey', date_created=date.today())
    album.save()

    track = Track(artist=radiohead.name, title='Creep', release_date='02/22/93', album='Pablo Honey',
                  spotify_url='url', date_created=date.today())
    track.save()

    oasis = Artist(name='Oasis', img_url='url', date_created=date.today())
    oasis.save()

    oasis_album = Album(artist=oasis.name, name='(Whats The Story) Morning Glory?', date_created=date.today())
    oasis_album.save()

    oasis_album = Album(artist=oasis.name, name='Heathen Chemistry', date_created=date.today())
    oasis_album.save()

    oasis_track = Track(artist=oasis.name, title='Wonderwall', release_date='1995',
                        album=oasis_album.name, spotify_url='url2', date_created=date.today())
    oasis_track.save()

    print('created!')


if __name__ == '__main__':
    # db.connect()
    db.create_tables([Artist, Album, Track])
    main()