text = """
╔══╗╔══╗╔══╗╔════╗──╔═══╗╔══╗
║╔═╝║╔╗║║╔═╝╚═╗╔═╝──║╔═╗║║╔╗║
║╚═╗║╚╝║║╚═╗──║║────║║─║║║╚╝║
║╔═╝║╔╗║╚═╗║──║║────║║╔╝║║╔╗║
║║──║║║║╔═╝║──║║────║╚╝─║║║║║
╚╝──╚╝╚╝╚══╝──╚╝────╚═══╝╚╝╚╝
"""

from change_connect_settings.change_connect_settings import choice_thing
from change_request_status.change_status_request import change_status
from prerequest.create_prerequest import request

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
print('1. Изменить настройки соединеня\n2. Изменить статус заявки\n3. Создать предзаявку\n4. Поиск отсутствующих файлов')
try:
    choice = int(input('Выберите один из вариантов\n'))
except ValueError:
    choice = 0

while switch(choice):
    if case(1):
        print("Изменить настройки соединеня")
        choice_thing()
        break
    if case(2):
        print("Изменить статус заявки")
        change_status()
        break
    if case(3):
        print("Создание предзаявки")
        request()
        break
    print("Указали некорректный вариант")
    break
    request()
    print("Указали некорректный вариант")
    break
