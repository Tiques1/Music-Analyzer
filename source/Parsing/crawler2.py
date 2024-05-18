from YaMusicParser import YaMusicParser
from DBHelper import DBHelper
from FileRenamer import FileRenamer
from threading import Thread
import json
from selenium.common.exceptions import NoSuchElementException


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
    def download(self, link_):
        pass

    # only https://music.yandex.ru/album/alb_id/
    # check if artist is not exist, add record to artist table
    # fill up album data
    # add record to album_autorship table
    def parse_album(self, link_):
        pass

    # only https://music.yandex.ru/album/album_id/track/track_id
    # check if artist is not exist, add record to artist table
    # fill up track data
    # add record to autorship table
    def parse_track(self, link_):
        pass

    # only https://music.yandex.ru/artist/artist_id
    # fill up artist table
    def parse_artist(self, link_):
        pass


class Crawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.parser = YaMusicParser()
        self.parser.save_dir = 'D:\\Music\\Test'
        self.parser.profile = 'Default'
        self.parser.user_data = 'C:/Users/Сергей/AppData/Local/Google/Chrome/User Data'

        self.db = DBHelper('music', 'postgres', '1111', 'localhost')

        self.file_renamer = FileRenamer('D:\\Music\\Test\\')
        self.renamer = Thread(target=self.file_renamer.mainloop)

        self.parser.start()
        self.renamer.start()

    def download(self, link_):
        if self.parser.browse(link_['link']) is None:
            return

        buttons = self.parser.get_buttons()
        while not buttons:
            buttons = self.parser.get_buttons()

        for i in range(int(link_['start']), int(link_['stop']), int(link_['step'])):
            try:
                alb_id, track_id = self.parser.download(buttons[i])
            except IndexError:
                continue

            self.file_renamer.rename(track_id)

            if self.db.check_if_exist(track_id, 'track') is None:
                self.db.exec(f'insert into track values ({track_id}, null, null, {alb_id})')

            if self.db.check_if_exist(alb_id, 'album') is None:
                self.db.exec(f'insert into album values ({alb_id}, null, null)')

    def parse_artist(self, link_):
        if self.parser.browse(link_) is None:
            return

        artist_id = link_.split('/')[4]
        artist_name = None
        while True:
            try:
                artist_name = self.parser.get_artist()
            except NoSuchElementException:
                continue
            break

        print(artist_id, artist_name)
        self.db.exec(f"""UPDATE artist
                        SET name = '{artist_name.replace("'", "''")}'
                        WHERE id = {artist_id}""")

    def parse_album(self, link_):
        if self.parser.browse(link_) is None:
            return

        album_id = link_.split('/')[4]
        cover, name, year, genres, artists_id, label_id = None, None, None, None, None, None
        while True:
            try:
                cover, name, year, genres, artists_id, label_id = self.parser.get_album()
            except NoSuchElementException:
                continue
            break

        print(cover, name, year, genres, artists_id, label_id)
        for artist_id in artists_id:
            if not self.db.check_if_exist(artist_id, 'artist'):
                self.db.exec(f'insert into artist values ({artist_id}, null)')

            self.db.exec(f'select * from album_autorship where album = {album_id} and artist = {artist_id}')
            if not self.db.fetch_all():
                self.db.exec(f'insert into album_autorship values ({album_id}, {artist_id})')

        self.db.exec(f"""UPDATE album
                                SET name = '{name.replace("'", "''")}', genre = '{genres}'
                                WHERE id = {album_id}""")

    def parse_track(self, link_):
        if self.parser.browse(link_) is None:
            return

        track_id = link_.split('/')[6]
        album_id = link_.split('/')[4]

        artists_ids, name, number_in_album = None, None, None
        while True:
            try:
                artists_ids, name, number_in_album = self.parser.get_track(track_id)
            except NoSuchElementException:
                continue
            break

        print(artists_ids, name, number_in_album)
        if not self.db.check_if_exist(track_id, 'track'):
            self.db.exec(f'insert into track values ({track_id}, \'{name}\', {number_in_album}, {album_id})')
        else:
            self.db.exec(f"""UPDATE track
                        SET name = '{name.replace("'", "''")}', album_num = {number_in_album}
                        WHERE id = {track_id}""")

        for artist_id in artists_ids:
            if not self.db.check_if_exist(artist_id, 'artist'):
                self.db.exec(f'insert into artist values ({artist_id}, null)')

            self.db.exec(f'select * from autorship where track = {track_id} and artist = {artist_id}')
            if not self.db.fetch_all():
                self.db.exec(f'insert into autorship values ({track_id}, {artist_id})')

    def __del__(self):
        self.parser.close()


if __name__ == '__main__':
    crawler = Crawler()
    db = DBHelper('music', 'postgres', '1111', 'localhost')

    # First of all download tracks from json file

    # links = crawler.read_link('test.json')
    # for link1 in links.values():
    #     crawler.download(link1)

    # Then generate links from database and fill up info

    # db.exec('select distinct album from track')
    # for album in db.fetch_all():
    #     link = f'https://music.yandex.ru/album/{album[0]}'
    #     print(link)
    #     crawler.parse_album(link)

    db.exec('select id from artist')
    for artist in db.fetch_all():
        link = f'https://music.yandex.ru/artist/{artist[0]}'
        print(link)
        crawler.parse_artist(link)

    # db.exec('select album, id from track')
    # for info in db.fetch_all():
    #     link = f'https://music.yandex.ru/album/{info[0]}/track/{info[1]}'
    #     print(link)
    #     crawler.parse_track(link)

    crawler.parser.close()
