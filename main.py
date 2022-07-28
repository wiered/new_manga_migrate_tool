from newmanga import add_multiple, add_multiple_crazy_method, add_multiple_lazy_method, get_name, add_manga
import keyboard
import requests, json

login = input("Input newmanga login: ")
password = input("Input newmanga password: ")
from remanga import get_manga

def main():
    login_url = 'https://api.newmanga.org/v2/login'
    login_payload = {
        'credentials': login,
        'password': password
        }

    session = requests.Session()
    p = session.post(login_url, data=json.dumps(login_payload))
    if p.status_code != 200:
        print("Что-то пошло не так, попробуйте проверить правильность введённых данных")
        return None
    
    reading_now, will_read, read, postponed, throw, not_interedted = get_manga() # Получение списков из решки
    
    print('Выберете пункт:')
    print("1 - Я хочу сам всё проверить (Рекомендую для маленькой библиотеки из 50-200 манг)\n    - Покажет вам всё что есть в виде:\n      Remanga name: {remanga name}\n      Newmanga name: {newmanga name}\n      По нажатию 'y' или 'enter' добавит в библиотеку, по нажатию любой другой клавиши - нет")
    print()
    print("2 - Я ленивый, давай автоматически (Рекомендую для большой библиотеки из 300+ манг)\n    - Ленивый метод не требующий от юзера лишних телодвижений.\n      Возможно, некоторая манга не будет добавлена")
    print()
    print("3 - Я бешенный, давай всё подряд (Не рекомендую)\n    - Бешенный метод не требующий от юзера лишних телодвижений.\n      Возможно, будет добавлена манга не из библиоеки")

    k = keyboard.read_event().scan_code
    if k == 3:
        add_multiple_lazy_method(login_payload, reading_now, "Читаю")
        add_multiple_lazy_method(login_payload, will_read, "Буду читать")
        add_multiple_lazy_method(login_payload, read, "Прочитано")
        add_multiple_lazy_method(login_payload, postponed, "Отложено")
        add_multiple_lazy_method(login_payload, throw, "Брошено")
        add_multiple_lazy_method(login_payload, not_interedted, "Не интересно")
    elif k == 4:
        add_multiple_crazy_method(login_payload, reading_now, "Читаю")
        add_multiple_crazy_method(login_payload, will_read, "Буду читать")
        add_multiple_crazy_method(login_payload, read, "Прочитано")
        add_multiple_crazy_method(login_payload, postponed, "Отложено")
        add_multiple_crazy_method(login_payload, throw, "Брошено")
        add_multiple_crazy_method(login_payload, not_interedted, "Не интересно")
    else:
        add_multiple(login_payload, reading_now, "Читаю")
        add_multiple(login_payload, will_read, "Буду читать")
        add_multiple(login_payload, read, "Прочитано")
        add_multiple(login_payload, postponed, "Отложено")
        add_multiple(login_payload, throw, "Брошено")
        add_multiple(login_payload, not_interedted, "Не интересно")
    
if __name__ == '__main__':
    main()
