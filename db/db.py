from peewee import *
from datetime import date, datetime

db = SqliteDatabase('music.sqlite', pragmas={'foreign_keys': 1})

class BaseModel(Model):
    class Meta:
        database = db

class Artist(BaseModel):
    name = CharField(unique=True)
    last_updated = DateTimeField()

    def __str__(self):
        return f'{self.name}, {self.last_updated}'


class Album(BaseModel):
    artist = ForeignKeyField(Artist, backref='albums')
    name = CharField(unique=True)
    release_date = CharField()
    last_updated = DateTimeField()

    def __str__(self):
        return f'{self.artist}, {self.name}, {self.release_date}, {self.last_updated}'


class Track(BaseModel):
    artist = ForeignKeyField(Artist, backref='tracks')
    title = CharField(unique=True)
    album = ForeignKeyField(Album, backref='tracks')
    spotify_url = CharField()
    last_updated = DateTimeField()

    def __str__(self):
        return f'{self.artist}, {self.title}, {self.album}, {self.spotify_url}, {self.last_updated}'


db.connect()
db.create_tables([Artist, Album, Track])


def sample_data():
    search_result = {
        'artist': 'Oasis', 'tracks': [
            {
                'title': 'Wonderwall',
                'album': '(Whats The Story) Morning Glory?',
                'release date': '1995',
                'spotify url': 'url'
            }, {
                'title': 'Dont Look Back in Anger',
                'album': '(Whats The Story) Morning Glory?',
                'release date': '1995',
                'spotify url': 'url'
            }, {
                'title': 'Stop Crying Your Heart Out',
                'album': 'Heathen Chemistry',
                'release date': '2002-07-01',
                'spotify url': 'url'
            }
        ]
    }

    return search_result

def main():
    radiohead = Artist(name='Radiohead', last_updated=date.today())
    radiohead.save()

    album = Album(artist=radiohead.name, name='Pablo Honey', release_date='02/22/93', last_updated=date.today())
    album.save()

    track = Track(artist=radiohead.name, title='Creep', album=album.name, spotify_url='url', last_updated=date.today())
    track.save()

    menu_text = """
        1. Display all tables
        2. Search by name
        3. Add new record
        4. Edit existing record
        5. Delete record 
        6. Quit
        """

    while True:
        print(menu_text)
        choice = input('Enter your choice: ')
        if choice == '1':
            display_all_tables()
        elif choice == '2':
            search_by_name()
        elif choice == '3':
            add_new_search_result()
        elif choice == '4':
            edit_existing_table()
        elif choice == '5':
            delete_record()
        elif choice == '6':
            display_all_artists()
        elif choice == '7':
            display_all_albums()
        elif choice == '8':
            display_all_tracks()
        elif choice == '9':
            break
        else:
            print('Not a valid selection, please try again')

def search_by_name():
    name = input('Enter name: ')
    try:
        table = Artist.select().where(Artist.name == name).get()
        print(table)

    except DoesNotExist:
        print(f'{name} does not exist')

def add_new_search_result():
    new_artist = sample_data()

    try:
        get_or_create_artist(new_artist.get('artist'))
        for album in new_artist:
            get_or_create_album(new_artist.get('tracks'))

    except Exception as e:
        print(e)

def get_or_create_artist(artist_name):
    artist, created = Artist.get_or_create(
        name=artist_name,
        defaults={'last_updated': datetime.today()}
    )
    if created:
        print(f'{artist} created!')
    else:
        print(f'{artist} already exists.')

def get_or_create_album(album_name):
    album, created = Artist.get_or_create(
        name=album_name,
        defaults={'last_updated': datetime.today()}
    )
    if created:
        print(f'{album} created!')
    else:
        print(f'{album} already exists.')

def get_or_create_track():

def edit_existing_table():

def delete_record():


def display_all_tables():
    artists = Artist.select()
    for artist in artists:
        print(artist)
    albums = Album.select()
    for album in albums:
        print(album)
    tracks = Track.select()
    for track in tracks:
        print(track)

def display_all_artists():
    artists = Artist.select()
    for artist in artists:
        print(artist)

def display_all_albums():
    albums = Album.select()
    for album in albums:
        print(album)

def display_all_tracks():
    tracks = Track.select()
    for track in tracks:
        print(track)


