from multiprocessing import connection
import sqlite3

class Database:
    def __init__(self, dbfile):
        self.connection = sqlite3.connect(dbfile)
        self.cur = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            self.cur.execute("INSERT INTO ")