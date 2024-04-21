import re
import sqlite3


class SQLite:
    def __init__(self, database):
        self.__conn = sqlite3.connect(database)
        self.__cursor = self.__conn.cursor()

    # Takes query or filename.sql
    def query(self, query: str):
        if query == re.match('.*\.sql', query):
            with open(query, 'r+') as file:
                text = '\n'.join(file.readlines())
                self.__cursor.executescript(text)
        else:
            self.__cursor.execute(query)
        self.__conn.commit()

    def fetch(self, how_many, size=0):
        if how_many == 'one':
            return self.__cursor.fetchone()
        if how_many == 'all':
            return self.__cursor.fetchall()
        if how_many == 'many':
            return self.__cursor.fetchmany(size)

    def disconnect(self):
        self.__cursor.close()
        self.__conn.close()
