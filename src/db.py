import datetime
from dataclasses import asdict

from pymongo import MongoClient

from src import env
from src.domain.objave import Objava

client = MongoClient(env.DB_CLUSTER)
this = client[env.DB_NAME]

objave = [
    asdict(Objava(naslov='Python', podnaslov='Zakaj Python', kategorije=['programiranje', 'python'],
                  slika='/static/blog/python.png',
                  opis='Python je danes eden izmed najbolj razširjenimi programskimi jeziki',
                  vsebina='Že vrsto let je python znan kot programski jezik, ki se najbolj uporablja pri programiranju',
                  ustvarjeno=datetime.datetime.now())),
    asdict(Objava(naslov='JavaScript', podnaslov='Zakaj JavaScript', kategorije=['programiranje', 'javascript'],
                  slika='/static/blog/python.png',
                  opis='Python je danes eden izmed najbolj razširjenimi programskimi jeziki',
                  vsebina='Že vrsto let je JavaScript znan kot programski jezik, ki se najbolj uporablja pri programiranju',
                  ustvarjeno=datetime.datetime.now())),
    asdict(Objava(naslov='Kotlin', podnaslov='Zakaj Kotlin', kategorije=['programiranje', 'kotlin'],
                  slika='/static/blog/python.png',
                  opis='Python je danes eden izmed najbolj razširjenimi programskimi jeziki',
                  vsebina='Že vrsto let je Kotlin znan kot programski jezik, ki se najbolj uporablja pri programiranju',
                  ustvarjeno=datetime.datetime.now())),
    asdict(Objava(naslov='Kotlin 2', podnaslov='Zakaj Kotlin', kategorije=['programiranje', 'kotlin'],
                  slika='/static/blog/python.png',
                  opis='Python je danes eden izmed najbolj razširjenimi programskimi jeziki',
                  vsebina='Že vrsto let je Kotlin znan kot programski jezik, ki se najbolj uporablja pri programiranju',
                  ustvarjeno=datetime.datetime.now())),
    asdict(Objava(naslov='Kotlin 3', podnaslov='Zakaj Kotlin', kategorije=['programiranje', 'kotlin'],
                  slika='/static/blog/python.png',
                  opis='Python je danes eden izmed najbolj razširjenimi programskimi jeziki',
                  vsebina='Že vrsto let je Kotlin znan kot programski jezik, ki se najbolj uporablja pri programiranju',
                  ustvarjeno=datetime.datetime.now())),
    asdict(Objava(naslov='Kotlin 4', podnaslov='Zakaj Kotlin', kategorije=['programiranje', 'kotlin'],
                  slika='/static/blog/python.png',
                  opis='Python je danes eden izmed najbolj razširjenimi programskimi jeziki',
                  vsebina='Že vrsto let je Kotlin znan kot programski jezik, ki se najbolj uporablja pri programiranju',
                  ustvarjeno=datetime.datetime.now())),
    asdict(Objava(naslov='Kotlin 5', podnaslov='Zakaj Kotlin', kategorije=['programiranje', 'kotlin'],
                  slika='/static/blog/python.png',
                  opis='Python je danes eden izmed najbolj razširjenimi programskimi jeziki',
                  vsebina='Že vrsto let je Kotlin znan kot programski jezik, ki se najbolj uporablja pri programiranju',
                  ustvarjeno=datetime.datetime.now()))
]


def drop():
    this.objave.drop()


def seed():
    this.objave.insert_many(objave)
