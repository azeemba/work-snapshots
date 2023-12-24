from configparser import ConfigParser
from dataclasses import dataclass
from typing import cast
import sqlite3

@dataclass
class SessionOverride:
    identifier: int 
    custom_title: str | None
    tags: list[str] | None


class Db:
    def __init__(self, config: ConfigParser):
        db_path = config["main"]["db"]
        self.connection = sqlite3.connect(db_path)
    
    def close(self):
        self.connection.close()
    
    def get_all_overrides(self):
        res = self.connection.execute(
            "SELECT identifier, title, tags FROM session_overrides")
        
        overrides: dict[int, SessionOverride] = {}
        for row in res:
           tags: str = row[2] if row[2] else ""
           overrides[row[0]] = SessionOverride(row[0], row[1], tags.split(" "))
        
        return overrides
    
    def add_title(self, identifer, title):
        res = self.connection.execute(
            'INSERT INTO session_overrides (identifier, title, tags) VALUES (?, ?, "")',
            (identifer, title)
        )
        print(f"Updated {res.rowcount} in add_title")
    
    def get_specific_override(self, identifier):
        res = self.connection.execute(
            "SELECT identifier, title, tags FROM session_overrides WHERE identifier = ?",
            (identifier,))
        
        if not res:
            return None

        row = res.fetchone()
        return SessionOverride(row[0], row[1], row[2].split())