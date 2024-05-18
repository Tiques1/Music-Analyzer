from YaMusicParser import YaMusicParser
from DBHelper import DBHelper
from FileRenamer import FileRenamer
from threading import Thread
import json


class BaseCrawler:
    def __init__(self):
        self.parser = None
        self.db = None

    @staticmethod
    def read_link(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    # any list of tracks on https://music.yandex.ru
    # add record about track to track table
    # download track
    # only one which use read_link method
    def download(self, link):
        pass

    # only https://music.yandex.ru/album/alb_id/
    # check if artist is not exist, add record to artist table
    # fill up album data
    # add record to album_autorship table
    def parse_album(self, link):
        pass

    # only https://music.yandex.ru/album/album_id/track/track_id
    # check if artist is not exist, add record to artist table
    # fill up track data
    # add record to autorship table
    def parse_track(self, link):
        pass

    # only https://music.yandex.ru/artist/artist_id
    # fill up artist table
    def parse_artist(self, link):
        pass


class Crawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.parser = YaMusicParser()
        self.parser.save_dir = 'D:\\Music\\Test'
        self.parser.profile = 'Default'
        self.parser.user_data = r'C:\\Users\\Сергей\\AppData\\Local\\Google\\Chrome\\User Data'

        self.db = DBHelper('music', 'postgres', '1111', 'localhost')

        self.file_renamer = FileRenamer('D:\\Music\\')
        self.renamer = Thread(target=self.file_renamer.mainloop)

        self.parser.start()
        self.renamer.start()

    def download(self, link):
        if self.parser.browse(link['link']) is None:
            return

        buttons = self.parser.get_buttons()
        while not buttons:
            buttons = self.parser.get_buttons()

        for i in range(link['start'], link['stop'], link['step']):
            try:
                alb_id, track_id = self.parser.download(buttons[i])
            except IndexError:
                continue

            self.file_renamer.rename(track_id)

            if self.db.check_if_exist(track_id, 'track') is None:
                self.db.exec(f'insert into track values ({track_id}, null, null, {alb_id})')

            if self.db.check_if_exist(alb_id, 'album') is None:
                self.db.exec(f'insert into album values ({alb_id}, null, null, null, null)')

    def parse_artist(self, link):
        if self.parser.browse(link) is None:
            return

        artist_id = link.split('/')[4]
        artist_name, cover = self.parser.get_artist()

        if self.db.check_if_exist(artist_id, 'artist') is None:
            self.db.exec(f'insert into artist values ({artist_id}, {artist_name})')

    def parse_album(self, link):
        if self.parser.browse(link) is None:
            return

        album_id = link.split('/')[4]
        cover, name, year, genres, artists_id, label_id = self.parser.get_album()

        for artist_id in artists_id:
            if self.db.check_if_exist(artist_id, 'artist') is None:
                self.db.exec(f'insert into artist values ({artist_id}, none)')

            self.db.exec(f'select * from album_autorship where album = {album_id} and artist = {artist_id})')
            if self.db.fetch_all() is None:
                self.db.exec(f'insert into album_autorship values ({album_id}, {artist_id})')

        if self.db.check_if_exist(album_id, 'album') is None:
            self.db.exec(f'insert into album values ({album_id}, {name}, none, none, {genres})')

    def parse_track(self, link):
        if self.parser.browse(link) is None:
            return

        track_id = link.split('/')[6]
        artists_id, name, number_in_album = self.parser.get_track()

        if self.db.check_if_exist(track_id, 'track') is None:
            self.db.exec(f'insert into track values ({track_id}, {name}, {number_in_album}, none)')
        else:
            self.db.exec(f"""UPDATE track
                        SET name = {name}, album_bum = {number_in_album}
                        WHERE id = {track_id}""")

        for artist_id in artists_id:
            if self.db.check_if_exist(artist_id, 'artist') is None:
                self.db.exec(f'insert into artist values ({artist_id}, none)')

            self.db.exec(f'select * from autorship where track = {track_id} and artist = {artist_id})')
            if self.db.fetch_all() is None:
                self.db.exec(f'insert into album_autorship values ({track_id}, {artist_id})')

    def __del__(self):
        self.parser.close()


if __name__ == '__main__':
    crawler = BaseCrawler()
    db = DBHelper('music', 'postgres', '1111', 'localhost')

    # First of all download tracks from json file

    # links = crawler.read_link('links.json')
    # for link1 in links.values():
    #     crawler.download(link1)

    # Then generate links from database and fill up info

    db.exec('select distinct album from track')
    for album in db.fetch_all():
        link = f'https://music.yandex.ru/album/{album[0]}'
        crawler.parse_album(link)

    db.exec('select distinct artist from album_autorship')
    for artist in db.fetch_all():
        link = f'https://music.yandex.ru/artist/{artist[0]}'
        crawler.parse_artist(link)

    db.exec('select album, id from track')
    for info in db.fetch_all():
        link = f'https://music.yandex.ru/album/{info[0]}/track/{info[1]}'
        crawler.parse_artist(link)
