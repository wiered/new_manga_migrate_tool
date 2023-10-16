import asyncio
from getpass import getpass
from time import sleep
from sys import exit

import requests, json
from tqdm import tqdm

from remanga import ReMangaParser
from newmanga import NewMangaParser

bookmarks = {
    1: "Читаю",
    2: "Буду читать",
    3: "Прочитано",
    4: "Отложено",
    5: "Брошено",
    6: "Не интересно"
}

__version__ = "v1.4.1"

def get_login_payload():
    login = input("Input newmanga login: ")
    password = getpass("Input newmanga password (will be invisible): ")
    login_payload = {
        'credentials': login,
        'password': password
        }

    return login_payload

def check_credentials(login_payload):
    login_url = 'https://api.newmanga.org/v2/login'
    session = requests.Session()

    p = session.post(login_url, data=json.dumps(login_payload))
    if p.status_code != 200:
        print("Неправильно введён логин или пароль")
        sleep(5)
        raise Exception("Неправильно введён логин или пароль")
    
def main():
    login_payload = get_login_payload()
    check_credentials(login_payload)

    parser = ReMangaParser()
    parsed_manga = parser.get_manga() # Получение списков из решки
    bookmark = 1
    print("\nAdding manga to your newmanga library! \nBe patient, please. It can take from 20 seconds to several minutes.\n")
    errors = []
    with NewMangaParser(login_payload) as parser:
        for catalogue in tqdm(parsed_manga):
            errors.append(asyncio.run(parser.migrate_async(catalogue, bookmarks[bookmark])))
            bookmark += 1

    print()
    for _errors in errors:
        for error in _errors:
            print("Error, not added: {}".format(*error))

if __name__ == '__main__':
    main()
    exit()
