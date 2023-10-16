import asyncio
import json
import time

import httpx
import requests
from tqdm import tqdm

class NewMangaParser():
    def __init__(self, login_payload):
        self.login_url = 'https://api.newmanga.org/v2/login'
        self.search_url = 'https://neo.newmanga.org/catalogue'

        self.file = open('data.json')
        self.search_payload = json.load(self.file)
        self.login_payload = login_payload


    async def migrate(self, manga_catalogue, bookmark): 
        """
        ---Adding multiple mangas to newmanga library
        """
            
        with requests.Session() as session:
            p = session.post(self.login_url, data=json.dumps(self.login_payload))
            for remanga_name in manga_catalogue:
                self.search_payload["query"] = remanga_name
                r = session.post(self.search_url, json=self.search_payload)
                if r.json().get('result').get('hits'):
                    name = r.json().get('result').get('hits')[0].get('document').get('title_ru')
                    slug = r.json().get('result').get('hits')[0].get('document').get('slug')
                    if name == remanga_name:
                        print(name)
                        manga_url = 'https://api.newmanga.org/v2/projects/' + slug
                        r = session.post(manga_url + '/bookmark', json={'type':bookmark})
                    time.sleep(1)


    async def migrate_async(self, manga_catalogue, bookmark): 
        """
        ---Adding multiple mangas to newmanga library
        """

        errors = []
        length = len(manga_catalogue)

        async with httpx.AsyncClient() as client:
            r = await client.request(method='POST', url = self.login_url, data = json.dumps(self.login_payload))
            for remanga_name in tqdm(manga_catalogue):
                self.search_payload["query"] = remanga_name
                r = await client.request(method='POST', url=self.search_url, json = self.search_payload)
                if r.status_code == 429:
                    while r.status_code == 429:
                        print("\nProblem 429. Too many requests. Sleeping for 10 sec.")
                        for i in tqdm(range(10)):
                            time.sleep(1)
                        r = await client.request(method='POST', url=self.search_url, json = self.search_payload)
                if r.status_code != 200:
                    errors.append((remanga_name, "unable to add, status code: " + r.status_code))
                    time.sleep(10)
                    continue
                if r.json().get('result').get('hits'):
                    name = r.json().get('result').get('hits')[0].get('document').get('title_ru')
                    slug = r.json().get('result').get('hits')[0].get('document').get('slug')
                    if name == remanga_name:
                        manga_url = 'https://api.newmanga.org/v2/projects/' + slug
                        r = await client.request(method='POST', url = manga_url + '/bookmark', json = {"type": bookmark})
                        if r.status_code != 200:
                            errors.append((remanga_name, "unable to add, status code: " + r.status_code))
                            continue
                    else:
                        errors.append((remanga_name, "No such manga on catalog i guess?"))
        
        print()
        for error in errors:
            print("Error, not added:", *error)


    def __enter__(self):
        return self
    
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

def main():
    """
    ---Main
    """
    pass

if __name__ == '__main__':
    main()
