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
class switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True


def case(*args):
    return any((arg == switch.value for arg in args))


print(text)
# print('1. Изменить настройки соединеня\n2. Изменить статус заявки\n3. Создать предзаявку\n4. Поиск отсутствующих файлов')

while 1:
    print(
        '1. Изменить настройки соединеня\n2. Изменить статус заявки\n3. Создать предзаявку\n4. Карточки клиента')
    try:
        choice = int(input('Выберите один из вариантов\n'))
    except ValueError:
        choice = 0
    while switch(choice):
        if case(1):
            print("Изменить настройки соединеня")
            choice_thing()
            print('\n\n')
            break
        if case(2):
            print("Изменить статус заявки")
            change_status()
            print('\n\n')
            break
        if case(3):
            print("Создание предзаявки")
            request()
            print('\n\n')
            break
        if case(4):
            print("Карточки клиента")
            send_request_to_SV()
            print('\n\n')
            break
        print("Указали некорректный вариант")
        break
