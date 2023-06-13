from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Objava:
    naslov: str
    tagi: list[str]
    podnaslov: str
    opis: str
    vsebina: str
    ustvarjeno: datetime
    kategorije: list[str]
