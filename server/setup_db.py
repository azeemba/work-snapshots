import sqlite3
import sys
from contextlib import closing

from configparser import ConfigParser

schema = {
    1: "CREATE TABLE IF NOT EXISTS session_overrides("
    " identifier INTEGER PRIMARY KEY,"
    " title TEXT,"
    " tags TEXT)",
    2: "ALTER TABLE session_overrides RENAME tags TO tag",
    3: "CREATE TABLE IF NOT EXISTS tags("
    "tag TEXT, color TEXT, icon TEXT)"
}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Invoke with 'all' or integer for newly added sql")
    config = ConfigParser()
    config.read("config.conf")
    db_path = config["main"]["db"]

    with closing(sqlite3.connect(db_path)) as db:
        if sys.argv[1] != "all":
            db.execute(schema[int(sys.argv[1])])
        else:
            for sql in schema.values():
                db.execute(sql)
        res = db.execute("SELECT name FROM sqlite_master")
        print(res.fetchall())
