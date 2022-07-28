import requests
import json
import keyboard

def main():
    """
    ---Main
    """
    login = input("Input login: ")
    password = input("Input password: ")

    login_url = 'https://api.newmanga.org/v2/login'

    login_payload = {
        'credentials': login,
        'password': password
        }

    with requests.Session() as session:
        p = session.post(login_url, data=json.dumps(login_payload))
        manga_name = 'kill-the-hero'
        
        search_url = 'https://neo.newmanga.org/catalogue'
        file = open('data.json')
        search_payload = json.load(file)
        search_payload["query"] = manga_name
        r = session.post(search_url, json=search_payload)
        if not r.json().get('result').get('hits'):
            print("1")
        else:
            name = r.json().get('result').get('hits')[0].get('document').get('title_ru')
            slug = r.json().get('result').get('hits')[0].get('document').get('slug')
        if slug:
            manga_url = 'https://api.newmanga.org/v2/projects/' + slug
            r = session.post(manga_url + '/bookmark', json={'type':'Не интересно'})

def get_name(name, session):
    """
    ---Just getting name of the manga
    """
    login_url = 'https://api.newmanga.org/v2/login'

    with requests.Session() as session:
        manga_name = name
        
        search_url = 'https://neo.newmanga.org/catalogue'
        file = open('data.json')
        search_payload = json.load(file)
        search_payload["query"] = manga_name
        r = session.post(search_url, json=search_payload)
        if not r.json().get('result').get('hits'):
            return None
        else:
            name = r.json().get('result').get('hits')[0].get('document').get('title_ru')
            slug = r.json().get('result').get('hits')[0].get('document').get('slug')
            return name

def add_manga(login_payload, name, bookmark):
    """
    ---Adding one manga to newmanga library
    """
    login_url = 'https://api.newmanga.org/v2/login'
    with requests.Session() as session:
        slug = None
        p = session.post(login_url, data=json.dumps(login_payload))
        search_url = 'https://neo.newmanga.org/catalogue'

        file = open('data.json')
        search_payload = json.load(file)
        search_payload["query"] = name
        
        r = session.post(search_url, json=search_payload)
        if not r.json().get('result').get('hits'):
            slug = None
        else:
            slug = r.json().get('result').get('hits')[0].get('document').get('slug')
        if slug:
            manga_url = 'https://api.newmanga.org/v2/projects/' + slug
            r = session.post(manga_url + '/bookmark', json={'type':bookmark})

def add_multiple(login_payload, manga_list, bookmark):
    """
    ---Adding multiple mangas to newmanga library
        standart method
    """
    login_url = 'https://api.newmanga.org/v2/login'
    with requests.Session() as session:
        p = session.post(login_url, data=json.dumps(login_payload))
        search_url = 'https://neo.newmanga.org/catalogue'
        file = open('data.json')
        search_payload = json.load(file)
        for rname in manga_list:
            search_payload["query"] = rname
            r = session.post(search_url, json=search_payload)
            if not r.json().get('result').get('hits'):
                name = None
            else:
                name = r.json().get('result').get('hits')[0].get('document').get('title_ru')
                slug = r.json().get('result').get('hits')[0].get('document').get('slug')
            if name:
                print()
                print()
                print("Remanga name: {}\nNewmanga title: {}".format(rname, name))
                k = keyboard.read_event().scan_code
                if k == 21 or k == 28:
                    manga_url = 'https://api.newmanga.org/v2/projects/' + slug
                    r = session.post(manga_url + '/bookmark', json={'type':bookmark})
                    print('adding')
                elif k == 49:
                    print('pass')
                else:
                    print('pass')

def add_multiple_lazy_method(login_payload, manga_list, bookmark): 
    """
    ---Adding multiple mangas to newmanga library
        lazy method
    """
    login_url = 'https://api.newmanga.org/v2/login'
    with requests.Session() as session:
        p = session.post(login_url, data=json.dumps(login_payload))
        search_url = 'https://neo.newmanga.org/catalogue'
        file = open('data.json')
        search_payload = json.load(file)
        for rname in manga_list:
            search_payload["query"] = rname
            r = session.post(search_url, json=search_payload)
            if not r.json().get('result').get('hits'):
                name = None
            else:
                name = r.json().get('result').get('hits')[0].get('document').get('title_ru')
                slug = r.json().get('result').get('hits')[0].get('document').get('slug')
            if name:
                if name == rname:
                    print()
                    manga_url = 'https://api.newmanga.org/v2/projects/' + slug
                    r = session.post(manga_url + '/bookmark', json={'type':bookmark})
                    print(name)

def add_multiple_crazy_method(login_payload, manga_list, bookmark): 
    """
    ---Adding multiple mangas to newmanga library 
        crazy method
    """
    login_url = 'https://api.newmanga.org/v2/login'
    with requests.Session() as session:
        p = session.post(login_url, data=json.dumps(login_payload))
        search_url = 'https://neo.newmanga.org/catalogue'
        file = open('data.json')
        search_payload = json.load(file)
        for rname in manga_list:
            search_payload["query"] = rname
            r = session.post(search_url, json=search_payload)
            if not r.json().get('result').get('hits'):
                name = None
            else:
                name = r.json().get('result').get('hits')[0].get('document').get('title_ru')
                slug = r.json().get('result').get('hits')[0].get('document').get('slug')
            if name:
                print()
                manga_url = 'https://api.newmanga.org/v2/projects/' + slug
                r = session.post(manga_url + '/bookmark', json={'type':bookmark})
                print(name)

if __name__ == '__main__':
    main()