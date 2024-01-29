
from dataclasses import dataclass
from enum import Enum

@dataclass
class Process:
    name: str
    title: str
    isActive: bool

