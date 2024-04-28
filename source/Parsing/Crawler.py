from source.Parsing.YaMusicParser import YaMusicParser
from source.Parsing.Exceptions import UnknownLink, IncorrectlySpecified
import queue
import asyncio
import datetime
from source.Parsing.DBHelper import DBHelper


class Log:
    def __init__(self):
        self.log_file = 'log.txt'

    def log(self, *args):
        with open(self.log_file, 'a') as log_file:
            msg = str(datetime.datetime.now()) + ' '
            for arg in args:
                msg += str(arg) + ' '
            msg += '\n'
            log_file.write(msg)


class Crawler(Log):
    def __init__(self, parser: YaMusicParser):
        super().__init__()
        self.parser = parser
        self.database = DBHelper(database="music", user="postgres", password="1111", host='localhost')

        self.__links = queue.Queue()
        self.parser.start()

    def get_link(self):
        return self.__links.get()

    def put_link(self, link):
        self.__links.put(link)

    async def read_links(self, file_path):
        with open(file_path, 'r') as file:
            link = file.readline()
            while link:
                if self.__links.qsize() < 10:
                    self.put_link(link)
                    link = file.readline()

    @staticmethod
    def _prepare(link):
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

    # Fill track table and download tracks
    def fill_track(self, link):
        if link is None:
            return
        link = self._prepare(link)

        try:
            self.parser.browse(link[0])
        except (UnknownLink, TimeoutError) as e:
            self.log(e)
            return

        buttons = self.parser.get_buttons()
        for i in link[1]:
            alb_id, track_id = self.parser.download(buttons[int(i)])
            self.log('alb_id=', alb_id, 'track_id', track_id, 'downloaded')

            if self.database.check_if_exist(track_id, 'track') is None:
                self.database.exec(f'insert into track values ({track_id}, null, null, {alb_id}, null)')
                self.log('track_id', track_id, 'saved to database')

            if self.database.check_if_exist(alb_id, 'album') is None:
                self.database.exec(f'insert into album values ({alb_id}, null, null, null, null, null)')
                self.log('alb_id=', alb_id, 'saved to database')

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

    crawler = Crawler(parser)

    await crawler.read_links('links.txt')

    link = crawler.get_link()
    while link:
        crawler.fill_track(link)
        link = crawler.get_link()


if __name__ == '__main__':
    asyncio.run(main())
