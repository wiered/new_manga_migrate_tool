from newmanga import migrate
import requests, json
import remanga

bookmarks = {
    1: "Читаю",
    2: "Буду читать",
    3: "Прочитано",
    4: "Отложено",
    5: "Брошено",
    6: "Не интересно"
}

def main():
    login_url = 'https://api.newmanga.org/v2/login'

    login = input("Input newmanga login: ")
    password = input("Input newmanga password: ")
    login_payload = {
        'credentials': login,
        'password': password
        }

    session = requests.Session()
    p = session.post(login_url, data=json.dumps(login_payload))
    if p.status_code != 200:
        print("Что-то пошло не так, попробуйте проверить правильность введённых данных")
        return None

    remanga.load_webdriver()

    parsed_manga = remanga.get_manga() # Получение списков из решки
    bookmark = 1
    for catalogue in parsed_manga:
        migrate(login_payload, catalogue, bookmarks[bookmark])
        bookmark += 1
    
if __name__ == '__main__':
    main()
