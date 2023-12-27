from configparser import ConfigParser
from dataclasses import dataclass
from typing import cast
import sqlite3


@dataclass
class SessionOverride:
    identifier: int
    custom_title: str | None
    tag: str | None


class Db:
    def __init__(self, config: ConfigParser):
        db_path = config["main"]["db"]
        self.connection = sqlite3.connect(db_path, isolation_level=None)

    def close(self):
        self.connection.close()

    def get_all_overrides(self):
        res = self.connection.execute(
            "SELECT identifier, title, tag FROM session_overrides"
        )

        overrides: dict[int, SessionOverride] = {}
        for row in res:
            tag: str = row[2] if row[2] else ""
            overrides[row[0]] = SessionOverride(row[0], row[1], tag)

        print(overrides)
        return overrides

    def add_override(self, identifer, title, tag):
        res = self.connection.execute(
            """INSERT INTO session_overrides (identifier, title, tag)
                VALUES (?, ?, ?)
                ON CONFLICT (identifier)
                DO UPDATE SET
                    title=excluded.title,
                    tag=excluded.tag
            """,
            (identifer, title, tag),
        )
        print(f"Updated {res.rowcount} in add_override")

    def get_specific_override(self, identifier):
        res = self.connection.execute(
            "SELECT identifier, title, tag FROM session_overrides WHERE identifier = ?",
            (identifier,),
        )

        if not res:
            return None

        row = res.fetchone()
        return SessionOverride(row[0], row[1], row[2])
    
    def get_all_tags(self):
        res = self.connection.execute("SELECT tag, color, icon FROM tags");
        tagList = [{"tag": row[0], "color": row[1], "icon": row[2]} for row in res.fetchall()]
        return {
            "tags":  tagList
        }
    
    def create_tag(self, tag):
        res = self.connection.execute(
            "INSERT INTO tags (tag, color, icon) VALUES (?, ?, ?)",
            (tag, None, None))
