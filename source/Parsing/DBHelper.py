import asyncio
import psycopg2


class DBHelper:
    def __init__(self, database, user, password, host):
        self.con = psycopg2.connect(database=database, user=user, password=password, host=host)
        self.cur = self.con.cursor()

    async def exec(self, command):
        self.cur.execute(command)
        self.con.commit()

    async def fetch(self):
        return self.cur.fetchone()

    async def check_if_exist(self, id_, table):
        await self.exec(f'select * from {table} where id = {id_}')
        return await self.fetch()

    def __del__(self):
        self.cur.close()
        self.con.close()


async def main():
    db = DBHelper(database="music", user="postgres", password="1111", host='localhost')
    await db.exec('select artist from track')
    result = await db.fetch()
    print(result)

if __name__ == '__main__':
    asyncio.run(main())
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
