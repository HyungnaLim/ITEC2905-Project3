from peewee import *
from datetime import date

db = SqliteDatabase('search_results_db.sqlite')

class BaseModel(Model):
    class Meta:
        database = db

class Artist(BaseModel):
    name = CharField(unique=True)
    last_updated = DateTimeField()

    def __str__(self):
        return f'{self.name}, {self.last_updated}'


class Album(BaseModel):
    artist = ForeignKeyField(Artist, backref='album')
    name = CharField(unique=True)
    release_date = CharField()
    last_updated = DateTimeField()

    def __str__(self):
        return f'{self.artist}, {self.name}, {self.release_date}, {self.last_updated}'


class Track(BaseModel):
    artist = ForeignKeyField(Artist, backref='track')
    title = CharField(unique=True)
    album = ForeignKeyField(Album, backref='track')
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
    radiohead = Artist(name='Radiohead', last_updated=date.today())
    radiohead.save()

    album = Album(artist=radiohead.name, name='Pablo Honey', release_date='02/22/93', last_updated=date.today())
    album.save()

    track = Track(artist='Radiohead', title='Creep', album='Pablo Honey', spotify_url='url', last_updated=date.today())
    track.save()

    print('created!')

def main():
    menu_text = """
        1. Display all artists
        2. Add sample data
        3. Display all albums
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
            display_all_artists()
        elif choice == '2':
             sample_data()
        elif choice == '3':
            display_all_albums()
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
    albums = Album.select()
    for album in albums:
        print(album)


if __name__ == '__main__':
    main()