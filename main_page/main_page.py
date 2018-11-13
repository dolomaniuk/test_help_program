text = """
╔══╗╔══╗╔══╗╔════╗──╔═══╗╔══╗
║╔═╝║╔╗║║╔═╝╚═╗╔═╝──║╔═╗║║╔╗║
║╚═╗║╚╝║║╚═╗──║║────║║─║║║╚╝║
║╔═╝║╔╗║╚═╗║──║║────║║╔╝║║╔╗║
║║──║║║║╔═╝║──║║────║╚╝─║║║║║
╚╝──╚╝╚╝╚══╝──╚╝────╚═══╝╚╝╚╝
"""

from change_connect_settings.change_connect_settings import choice_thing

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
choice = int(input('Выберите один из вариантов\n'))

while switch(choice):
    if case(1):
        print("Изменить настройки")
        choice_thing()
        break

    print("Указали некорректный вариант")
    break

    print("Указали некорректный вариант")
    break
