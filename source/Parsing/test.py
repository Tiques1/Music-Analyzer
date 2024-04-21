from source.Parsing.YaMusicParser import YaMusicParser
import psycopg2


def first_step():
    parser = YaMusicParser('https://music.yandex.ru/artist/8855006/tracks', 'predefined')
    db = psycopg2.connect(database="music", user="postgres", password="1111", host='localhost')
    cursor = db.cursor()

    try:
        parser.browse()
    except TimeoutError:
        return

    for elem in parser.get_buttons():
        alb_id, track_id, track_name = parser.download(elem)

        cursor.execute(f'insert into track values ({track_id}, \'{track_name}\', null, null, {alb_id}, null)')
        db.commit()


if __name__ == '__main__':
    first_step()
