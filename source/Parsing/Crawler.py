from source.Parsing.YaMusicParser import YaMusicParser
from source.Parsing.Exceptions import UnknownLink, IncorrectlySpecified
import asyncio
import datetime
from source.Parsing.DBHelper import DBHelper
from FileRenamer import FileRenamer
import threading


class Log:
    def __init__(self):
        self.log_file = 'log.txt'

    async def log(self, *args):
        with open(self.log_file, 'a') as log_file:
            msg = str(datetime.datetime.now()) + ' '
            for arg in args:
                msg += str(arg) + ' '
            msg += '\n'
            log_file.write(msg)


class Crawler(Log):
    def __init__(self, parser: YaMusicParser, file_renamer):
        super().__init__()
        self.parser = parser
        self.database = DBHelper(database="music", user="postgres", password="1111", host='localhost')
        self.file_renamer = file_renamer

        self.parser.start()

    @staticmethod
    def read_link(file_path):
        with open(file_path, 'r') as file:
            for link in file:
                yield link

    @staticmethod
    def _prepare(link):
        try:
            splitted = link.split(' ')
            if len(splitted) > 2:
                raise IncorrectlySpecified(link)
            if ';' in splitted[1]:
                return splitted[0], (splitted[1].split(';'))
            else:
                ranges = splitted[1].split(',')[0].split('-')
                indexes = []
                for i in range(int(ranges[0]), int(ranges[1]), int(splitted[1].split(',')[1])):
                    indexes.append(i)
                return splitted[0], indexes
        except Exception:
            raise IncorrectlySpecified

    # Fill track table and download tracks
    async def fill_track(self, link):
        try:
            link = self._prepare(link)
        except IncorrectlySpecified as e:
            await self.log(link, e)
            return

        try:
            self.parser.browse(link[0])
        except (UnknownLink, TimeoutError) as e:
            await self.log(e)
            return

        buttons = self.parser.get_buttons()
        while not buttons:
            buttons = self.parser.get_buttons()

        for i in link[1]:
            try:
                alb_id, track_id = self.parser.download(buttons[int(i)])
            except IndexError as e:
                await self.log(link, e)
                continue

            await self.log('alb_id', alb_id, 'track_id', track_id, 'downloaded')

            self.file_renamer.rename(track_id)

            if await self.database.check_if_exist(track_id, 'track') is None:
                await self.database.exec(f'insert into track values ({track_id}, null, null, {alb_id})')
                await self.log('track_id', track_id, 'saved to database')

            if await self.database.check_if_exist(alb_id, 'album') is None:
                await self.database.exec(f'insert into album values ({alb_id}, null, null, null, null)')
                await self.log('alb_id', alb_id, 'saved to database')

    def fill_album(self):
        pass

    def fill_artist(self):
        pass

    def fill_label(self):
        pass

    def __del__(self):
        self.parser.close()


async def main():
    parser = YaMusicParser()
    parser.save_dir = 'D:\\Music\\'
    parser.profile = 'Default'
    parser.user_data = r'C:\\Users\\Сергей\\AppData\\Local\\Google\\Chrome\\User Data'

    file_renamer = FileRenamer('D:\\Music\\')
    crawler = Crawler(parser, file_renamer)

    renamer = threading.Thread(target=file_renamer.mainloop)
    renamer.start()

    for link in crawler.read_link('links.txt'):
        await crawler.fill_track(link)


if __name__ == '__main__':
    asyncio.run(main())
