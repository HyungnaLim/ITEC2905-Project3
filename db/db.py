from peewee import *
from datetime import date

db = SqliteDatabase('music.sqlite', pragmas={'foreign_keys': 1})

class BaseModel(Model):
    class Meta:
        database = db


class Artist(BaseModel):
    name = CharField()
    last_updated = DateTimeField()

    def __str__(self):
        return f'{self.name}, {self.last_updated}'


class Album(BaseModel):
    artist = ForeignKeyField(Artist, backref='albums')
    name = CharField()
    release_date = CharField()
    last_updated = DateTimeField()

    def __str__(self):
        return f'{self.artist}, {self.name}, {self.release_date}, {self.last_updated}'


class Track(BaseModel):
    artist = ForeignKeyField(Artist, backref='tracks')
    title = CharField()
    album = ForeignKeyField(Album, backref='tracks')
    spotify_url = CharField()
    last_updated = DateTimeField()

    def __str__(self):
        return f'{self.artist}, {self.title}, {self.album}, {self.spotify_url}, {self.last_updated}'


db.connect()
db.create_tables([Artist, Album, Track])


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



# def populate_test_data():
#     db.connect()
#     db.create_tables([Artist, Album, Track])
#
#     data = (
#         ('Radiohead', ('Pablo Honey', ('02/22/93', ()),
#                        'OK Computer', ('05/28/97', ())))
#     )
#     for artist_name, albums in data:
#         artist = Artist.create(name=artist_name, last_updated=date.today())
#         for album, release in albums:
#             Album.create(artist=artist, name=album, release_date=release, last_updated=date.today())
#
#     track_data = (
#         ('')
#     )
