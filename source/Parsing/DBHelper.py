import asyncio
import psycopg2


class DBHelper:
    def __init__(self, database, user, password, host):
        self.__con = psycopg2.connect(database=database, user=user, password=password, host=host)
        self.__cur = self.__con.cursor()

    async def exec_await(self, command):
        self.__cur.execute(command)
        self.__con.commit()

    def exec(self, command):
        self.__cur.execute(command)
        self.__con.commit()

    async def fetch(self):
        return self.__cur.fetchone()

    def check_if_exist(self, id_, table):
        self.exec(f'select * from {table} where id = {id_}')
        return self.fetch_all()

    async def check_if_exist_async(self, id_, table):
        await self.exec_await(f'select * from {table} where id = {id_}')
        return await self.fetch()

    def fetch_many(self, n):
        return self.__cur.fetchmany(n)

    def fetch_all(self):
        return self.__cur.fetchall()

    def __del__(self):
        self.__cur.close()
        self.__con.close()


async def main():
    db = DBHelper(database="music", user="postgres", password="1111", host='localhost')
    await db.exec_await('select * from track')
    result = await db.fetch()
    print(result)

if __name__ == '__main__':
    asyncio.run(main())

    # db = DBHelper(database="music", user="postgres", password="1111", host='localhost')
    # db.exec('insert into track values (5, \'Новый мерин\', 2, 666)')
    # db.exec('insert into artist values (666, \'Morgenshtern\')')
    # db.exec('insert into autorship values (4, 666)')

    # db.exec('truncate table track')
    # asyncio.run(db.exec("""
    # create table album_autorship (
    #     album integer,
    #     artist integer,
    #
    #     constraint fk_autorship_album foreign key (album) references album(id),
    #     constraint fk_autorship_artist foreign key (artist) references artist(id)
    # )
    # """))
