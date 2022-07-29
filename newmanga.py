import requests
import json
import time

def main():
    """
    ---Main
    """
    pass

def migrate(login_payload, manga_catalogue, bookmark): 
    """
    ---Adding multiple mangas to newmanga library
    """
    login_url = 'https://api.newmanga.org/v2/login'
    with requests.Session() as session:
        p = session.post(login_url, data=json.dumps(login_payload))
        search_url = 'https://neo.newmanga.org/catalogue'
        file = open('data.json')
        search_payload = json.load(file)
        for rname in manga_catalogue:
            search_payload["query"] = rname
            r = session.post(search_url, json=search_payload)
            if r.json().get('result').get('hits'):
                name = r.json().get('result').get('hits')[0].get('document').get('title_ru')
                slug = r.json().get('result').get('hits')[0].get('document').get('slug')
                if name == rname:
                    print()
                    print(name)
                    manga_url = 'https://api.newmanga.org/v2/projects/' + slug
                    r = session.post(manga_url + '/bookmark', json={'type':bookmark})
                time.sleep(1)

if __name__ == '__main__':
    main()