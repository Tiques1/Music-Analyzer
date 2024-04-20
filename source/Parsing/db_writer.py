import sqlite3


class DBHelper:
    def __init__(self, name):
        self.con = sqlite3.connect(name)
        self.cur = self.con.cursor()
        self.result = None

    def exec(self, command):
        self.result = self.cur.execute(command)

    def fetch(self):
        res = self.result.fetchone()
        self.con.commit()
        return res

    def __del__(self):
        self.cur.close()
        self.con.close()


if __name__ == '__main__':
    db = DBHelper('tracks.db')
    db.exec('create table track')
