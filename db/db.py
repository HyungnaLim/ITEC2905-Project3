from peewee import *
from datetime import date, datetime

db = SqliteDatabase('db.sqlite')

class BaseModel(Model):
    class Meta:
        database = db

class Artist(BaseModel):
    name = CharField(unique=True)
    last_updated = CharField()

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

Artist.delete().execute()
Album.delete().execute()
Track.delete().execute()

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
        3. Add new search result
        4. Edit existing table
        5. Delete record 
        6. Display all artists
        7. Display all albums
        8. Display all tracks
        9. Quit
        """

    while True:
        print(menu_text)
        choice = input('Enter your choice: ')
        if choice == '1':
            display_all_tables()
        elif choice == '2':
            name = input('Enter name: ')
            search_by_name(name)
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

def search_by_name(name):
    try:
        table = (Artist.select().where(Artist.name == name).get()
                 or Album.select().where(Artist.name == name).get()
                 or Track.select().where(Artist.name == name).get())
        print(table)
        return table

    except DoesNotExist:
        print(f'{name} does not exist')

def add_new_search_result():
    new_artist = sample_data()

    try:
        get_or_create_artist(new_artist.get('artist'))
        for _ in new_artist:
            get_or_create_album(new_artist.get('artist'))
            get_or_create_track(new_artist.get('artist'))

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

def get_or_create_album(albums):
    album, created = Album.get_or_create(
        name=albums['tracks'][0]['album'],
        defaults={
            'artist': albums['artist'],
            'release_date': albums['tracks'][0]['release date'],
            'last_updated': datetime.today()}
    )
    if created:
        print(f'{album} created!')
    else:
        print(f'{album} already exists.')

def get_or_create_track(tracks):
    track, created = Track.get_or_create(
        name=tracks['tracks'][0]['title'],
        defaults={
            'artist': tracks['artist'],
            'album': tracks['tracks'][0]['album'],
            'spotify_url': tracks['tracks'][0]['spotify url'],
            'last_updated': datetime.today()}
    )
    if created:
        print(f'{track} created!')
    else:
        print(f'{track} already exists.')

def edit_existing_table():
    display_all_tables()
    search = input('Enter Artist, Album or Track name you\'d like to edit: ')
    table = search_by_name(search)
    edits = input('Enter edit: ')
    table.update(edits=edits).where(table.table == table).execute()

def delete_record():
    name = input('Enter name to delete: ')

    Artist.delete().where(Artist.name == name).execute()

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

if __name__ == '__main__':
    main()
