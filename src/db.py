import datetime
from dataclasses import asdict

from pymongo import MongoClient

from src import env
from src.domain.objave import Objava

client = MongoClient(env.DB_CLUSTER)
this = client[env.DB_NAME]

objave = [
    asdict(Objava(naslov='Python', podnaslov='Zakaj Python', kategorije=['programiranje', 'python'],
                  tagi=['javascript', 'pisanje'],
                  opis='Python je danes eden izmed najbolj srazširjenimi programskimi jeziki',
                  vsebina='Že vrsto let je python znan kot programski jezik, ki se najbolj uporablja pri programiranju',
                  ustvarjeno=datetime.datetime.now())),
    asdict(Objava(naslov='JavaScript', podnaslov='Zakaj JavaScript', kategorije=['programiranje', 'javascript'],
                  tagi=['javascript', 'pisanje'],
                  opis='Python je danes eden izmed najbolj razširjenimi programskimi jeziki',
                  vsebina='Že vrsto let je JavaScript znan kot programski jezik, ki se najbolj uporablja pri programiranju',
                  ustvarjeno=datetime.datetime.now())),
    asdict(Objava(naslov='Kotlin', podnaslov='Zakaj Kotlin', kategorije=['programiranje', 'kotlin'],
                  tagi=['python', 'pisanje'],
                  opis='Python je danes eden izmed najbolj razširjenimi programskimi jeziki',
                  vsebina='Že vrsto let je Kotlin znan kot programski jezik, ki se najbolj uporablja pri programiranju',
                  ustvarjeno=datetime.datetime.now())),
    asdict(
        Objava(naslov='Kotlin 2', podnaslov='Zakaj Kotlin', kategorije=['programiranje', 'kotlin'],
               tagi=['javascript', 'pisanje'],
               opis='Python je danes eden izmed najbolj razširjenimi programskimi jeziki',
               vsebina='Že vrsto let je Kotlin znan kot programski jezik, ki se najbolj uporablja pri programiranju',
               ustvarjeno=datetime.datetime.now())),
    asdict(
        Objava(naslov='Kotlin 3', podnaslov='Zakaj Kotlin', kategorije=['programiranje', 'kotlin'],
               tagi=['java', 'pisanje'],
               opis='Python je danes eden izmed najbolj razširjenimi programskimi jeziki',
               vsebina='Že vrsto let je Kotlin znan kot programski jezik, ki se najbolj uporablja pri programiranju',
               ustvarjeno=datetime.datetime.now())),
    asdict(
        Objava(naslov='Kotlin 4', podnaslov='Zakaj Kotlin', kategorije=['programiranje', 'kotlin'],
               tagi=['javascript', 'pisanje'],
               opis='Python je danes eden izmed najbolj razširjenimi programskimi jeziki',
               vsebina='Že vrsto let je Kotlin znan kot programski jezik, ki se najbolj uporablja pri programiranju',
               ustvarjeno=datetime.datetime.now())),
    asdict(
        Objava(naslov='Kotlin 4', podnaslov='Zakaj Kotlin', kategorije=['programiranje', 'kotlin'],
               tagi=['javascript', 'pisanje'],
               opis='Python je danes eden izmed najbolj razširjenimi programskimi jeziki',
               vsebina='Že vrsto let je Kotlin znan kot programski jezik, ki se najbolj uporablja pri programiranju',
               ustvarjeno=datetime.datetime.now())),
    asdict(
        Objava(naslov='Kotlin 4', podnaslov='Zakaj Kotlin', kategorije=['programiranje', 'kotlin'],
               tagi=['javascript', 'pisanje'],
               opis='Python je danes eden izmed najbolj razširjenimi programskimi jeziki',
               vsebina='Že vrsto let je Kotlin znan kot programski jezik, ki se najbolj uporablja pri programiranju',
               ustvarjeno=datetime.datetime.now())),
    asdict(
        Objava(naslov='Kotlin 4', podnaslov='Zakaj Kotlin', kategorije=['programiranje', 'kotlin'],
               tagi=['javascript', 'pisanje'],
               opis='Python je danes eden izmed najbolj razširjenimi programskimi jeziki',
               vsebina='Že vrsto let je Kotlin znan kot programski jezik, ki se najbolj uporablja pri programiranju',
               ustvarjeno=datetime.datetime.now())),
    asdict(
        Objava(naslov='Kotlin 4', podnaslov='Zakaj Kotlin', kategorije=['programiranje', 'javascript'],
               tagi=['javascript', 'pisanje'],
               opis='Python je danes eden izmed najbolj razširjenimi programskimi jeziki',
               vsebina='Že vrsto let je Kotlin znan kot programski jezik, ki se najbolj uporablja pri programiranju',
               ustvarjeno=datetime.datetime.now())),
    asdict(
        Objava(naslov='Kotlin 4', podnaslov='Zakaj Kotlin', kategorije=['javascript'],
               tagi=['javascript', 'pisanje'],
               opis='Python je danes eden izmed najbolj razširjenimi programskimi jeziki',
               vsebina='Že vrsto let je Kotlin znan kot programski jezik, ki se najbolj uporablja pri programiranju',
               ustvarjeno=datetime.datetime.now())),
    asdict(
        Objava(naslov='Kotlin 4', podnaslov='Zakaj Kotlin', kategorije=['programiranje', 'python'],
               tagi=['javascript', 'pisanje'],
               opis='Python je danes eden izmed najbolj razširjenimi programskimi jeziki',
               vsebina='Že vrsto let je Kotlin znan kot programski jezik, ki se najbolj uporablja pri programiranju',
               ustvarjeno=datetime.datetime.now())),
    asdict(
        Objava(naslov='Kotlin 5', podnaslov='Zakaj Kotlin', kategorije=['java', 'kotlin'],
               tagi=['javascript', 'pisanje'],
               opis='Python je danes eden izmed najbolj razširjenimi programskimi jeziki',
               vsebina='Že vrsto let je Kotlin znan kot programski jezik, ki se najbolj uporablja pri programiranju',
               ustvarjeno=datetime.datetime.now()))
]


def count_tagi(objave):
    tagi = {}
    for objava in objave:
        for t in objava['tagi']:
            if t in tagi:
                tagi[t] += 1
            else:
                tagi[t] = 1
    return tagi


def is_admin(ime, geslo):
    return ime == env.UPORABNISKO_IME and geslo == env.GESLO


def count_kategorije(objave):
    kategorije = {}
    for objava in objave:
        if 'kategorije' in objava:
            for k in objava['kategorije']:
                if k in kategorije:
                    kategorije[k] += 1
                else:
                    kategorije[k] = 1
    return kategorije


def drop():
    this.objave.drop()


def seed():
    this.objave.insert_many(objave)
