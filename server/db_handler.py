from configparser import ConfigParser
from dataclasses import dataclass
from datetime import datetime
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

    def get_all_processes(self):
        res = self.connection.execute("SELECT datetime, process, title, isActive, recordFrequencySeconds FROM snapshot_processes")
        rows = []
        for row in res:
            # Keys match what the code was using in CSV
            rows.append({"Datetime": row[0], "Process": row[1], "Title": row[2], "IsActive": row[3], "RecordFreqSeconds": row[4]})
        return rows

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
        res = self.connection.execute("SELECT tag, color, icon FROM tags")
        tagList = [
            {"tag": row[0], "color": row[1], "icon": row[2]} for row in res.fetchall()
        ]
        return {"tags": tagList}

    def create_tag(self, tag):
        res = self.connection.execute(
            "INSERT INTO tags (tag, color, icon) VALUES (?, ?, ?)", (tag, None, None)
        )

    def get_all_splits(self):
        res = self.connection.execute(
            "SELECT originalKey, customStartDatetime FROM splits"
        )
        return [(int(row[0]), datetime.fromisoformat(row[1])) for row in res.fetchall()]

    def add_splits(self, sessionKey: int, customStart: datetime):
        res = self.connection.execute(
            """INSERT INTO splits (originalKey, customStartDatetime)
            VALUES (?, ?)""",
            (sessionKey, customStart.isoformat()),
        )
        print(f"Updated {res.rowcount} in add_splits")
