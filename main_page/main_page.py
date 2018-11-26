text = """
╔══╗╔══╗╔══╗╔════╗──╔═══╗╔══╗
║╔═╝║╔╗║║╔═╝╚═╗╔═╝──║╔═╗║║╔╗║
║╚═╗║╚╝║║╚═╗──║║────║║─║║║╚╝║
║╔═╝║╔╗║╚═╗║──║║────║║╔╝║║╔╗║
║║──║║║║╔═╝║──║║────║╚╝─║║║║║
╚╝──╚╝╚╝╚══╝──╚╝────╚═══╝╚╝╚╝
"""

from change_connect_settings.change_connect_settings import choice_thing
from db_operations.db_requests import change_status
from prerequest.create_prerequest import request
from check_status_card_in_sv.check_status_card_in_sv import send_request_to_SV

path = "connect_to_base.ini"


# объявление 2х функций для switch-case
class _switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True


def _case(*args):
    return any((arg == _switch.value for arg in args))


print(text)

while 1:
    print(
        """
        1. Изменить настройки соединеня
        2. Изменить статус заявки
        3. Создать предзаявку
        4. Карточки клиента
        """)
    try:
        choice = int(input('Выберите один из вариантов\n'))
    except ValueError:
        choice = 0
    while _switch(choice):
        if _case(1):
            print("Изменить настройки соединеня")
            choice_thing()
            print('\n\n')
            break
        if _case(2):
            print("Изменить статус заявки")
            change_status()
            print('\n\n')
            break
        if _case(3):
            print("Создание предзаявки")
            request()
            print('\n\n')
            break
        if _case(4):
            print("Карточки клиента")
            send_request_to_SV()
            print('\n\n')
            break
        print("Указали некорректный вариант")
        break
