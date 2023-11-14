import sqlite3
from sqlite3 import Error


def db_connect():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect("./db/bot.db")
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        return conn