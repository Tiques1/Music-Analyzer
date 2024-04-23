from source.Parsing.YaMusicParser import YaMusicParser
from source.Parsing.Exceptions import UnknownLink
import psycopg2
import queue


class MainParser:
    def __init__(self, parser: YaMusicParser):
        self.parser = parser
        self.connection = psycopg2.connect(database="music", user="postgres", password="1111", host='localhost')
        self.cursor = self.connection.cursor()

        self.__links = queue.Queue()

    def get_link(self):
        return self.__links.get()

    def put_link(self):
        self.__links.put(0)

    def read_links(self):
        pass

    def first_step(self):
        try:
            link_type = self.parser.browse('https://music.yandex.ru/artist/8855006/tracks')
        except UnknownLink:
            return

        for button in self.parser.get_buttons():
            alb_id, tarck_id = self.parser.download(button)
            self.cursor.execute(f'insert into table artist values ({tarck_id}, null, null, {alb_id}, null)')

    def second_step(self):
        pass

    def third_step(self):
        pass

    def fourth_step(self):
        pass


def main():
    parser = YaMusicParser()
    parser.save_dir = 'D:\\Music\\'
    parser.profile = 'Default'
    parser.user_data = r'C:\\Users\\Сергей\\AppData\\Local\\Google\\Chrome\\User Data'

    main_parser = MainParser(parser)
    while True:
        main_parser.put_link()
        print(main_parser.get_link())

    parser.start()

    parser.close()


if __name__ == '__main__':
    main()
