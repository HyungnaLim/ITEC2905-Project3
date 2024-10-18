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
    artist = ForeignKeyField(Artist, backref='albums')
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
    print(radiohead.name)

    album = Album(artist=radiohead.name, name='Pablo Honey', release_date='02/22/93', last_updated=date.today())
    album.save()

    track = Track(artist=radiohead.name, title='Creep', album='Pablo Honey', spotify_url='url', last_updated=date.today())
    track.save()

    oasis = Artist(name='Oasis', last_updated=date.today())
    oasis.save()

    oasis_album = Album(artist=oasis.name, name='(Whats The Story) Morning Glory?', release_date='1995', last_updated=date.today())
    oasis_album.save()

    oasis_track = Track(artist=oasis.name, title='Wonderwall', album=oasis_album.name, spotify_url='url2', last_updated=date.today())
    oasis_track.save()

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
    """
    Tweet.user = Album.artist
    User.tweet = Artist.album
    access FK
    tweet = Tweet.get()
    tweet.user
    backref
    user = User.get()
    user.tweets
    """
    artists = Artist.select()
    for artist in artists:
        print(f'Artist: {artist.name}')
        for album in artist.albums:
            print(f' Album: {album.name} Release Date: {album.release_date}')
    # print(artist.albums)
    # for i in artist.albums:
    #     print(i.album)



    # album = Album.get()
    # print(album.artist)
    # for x in artist.album:
    #     print(x.name)



    # artists = Artist.get()
    # print(artists.album)
    # for artist in artists.album:
    #     print(artist.select())


if __name__ == '__main__':
    main()