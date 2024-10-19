from peewee import *
from datetime import date
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
    last_updated = DateField()

    def __str__(self):
        return f'{self.name}, {self.last_updated}'

class Album(BaseModel):
    name = CharField(unique=True)
    release_date = CharField()
    last_updated = DateField()
    artist = ForeignKeyField(Artist, backref='albums')

    def __str__(self):
        return f'{self.name}, {self.release_date}, {self.last_updated}'

class Track(BaseModel):
    title = CharField(unique=True)
    spotify_url = CharField()
    last_updated = DateField()
    artist = ForeignKeyField(Artist, backref='tracks')
    album = ForeignKeyField(Album, backref='tracks')

    def __str__(self):
        return f'{self.title}, {self.spotify_url}, {self.last_updated}'

db.connect()
db.create_tables([Artist, Album, Track])

Artist.delete().execute()
Album.delete().execute()
Track.delete().execute()

def sample_data():
    radiohead = Artist(name='Radiohead', last_updated=date.today())
    radiohead.save()
    print(radiohead.name)

    album = Album(artist=radiohead.name, name='Pablo Honey', release_date='02/22/93', last_updated=date.today())
    album.save()

    track = Track(artist=radiohead.name, title='Creep', album='Pablo Honey', spotify_url='url', last_updated=date.today())
    track.save()

    oasis = Artist(name='Oasis', last_updated=date.today())
    oasis.save()

    oasis_album = Album(artist=oasis.name, name='(Whats The Story) Morning Glory?', release_date='1995',
                        last_updated=date.today())
    oasis_album.save()

    oasis_album = Album(artist=oasis.name, name='Heathen Chemistry', release_date='2002-07-01',
                        last_updated=date.today())
    oasis_album.save()

    oasis_track = Track(artist=oasis.name, title='Wonderwall', album=oasis_album.name, spotify_url='url2', last_updated=date.today())
    oasis_track.save()

    print('created!')

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
        elif choice == '6':
            break
        else:
            print('Not a valid selection, please try again')

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
        # print(f'{track.artist_id}: {track.album_id}', track)
        print(f'{track.title} - {track.artist_id}, {track.album_id}, {track.spotify_url}, {track.last_updated}')


if __name__ == '__main__':
    main()