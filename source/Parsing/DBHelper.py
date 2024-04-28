import psycopg2


class DBHelper:
    def __init__(self, database, user, password, host):
        self.con = psycopg2.connect(database=database, user=user, password=password, host=host)
        self.cur = self.con.cursor()

    def exec(self, command):
        self.cur.execute(command)
        self.con.commit()

    def fetch(self):
        return self.cur.fetchone()

    def check_if_exist(self, id_, table):
        self.exec(f'select * from {table} where id = {id_}')
        return self.fetch()

    def __del__(self):
        self.cur.close()
        self.con.close()


if __name__ == '__main__':
    pass
