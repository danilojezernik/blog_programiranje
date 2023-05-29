from dataclasses import dataclass
from datetime import datetime


@dataclass
class Objava:
    naslov: str
    podnaslov: str
    opis: str
    vsebina: str
    ustvarjeno: datetime
