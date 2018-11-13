text = """
╔══╗╔══╗╔══╗╔════╗──╔═══╗╔══╗
║╔═╝║╔╗║║╔═╝╚═╗╔═╝──║╔═╗║║╔╗║
║╚═╗║╚╝║║╚═╗──║║────║║─║║║╚╝║
║╔═╝║╔╗║╚═╗║──║║────║║╔╝║║╔╗║
║║──║║║║╔═╝║──║║────║╚╝─║║║║║
╚╝──╚╝╚╝╚══╝──╚╝────╚═══╝╚╝╚╝
"""

import ini_files.create_ini_file as ini

path = "connect_to_base.ini"


# объявление 2х функций для switch-case
class switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))


print(text)     # приветсвтие
print('1. Изменить настройки\n2. Изменить статус заявки\n3. Создать предзаявку\n4. Поиск отсутствующих файлов')
choice = int(input('Выберите один из вариантов\n'))

while switch(choice):
    if case(1):
        print("используем текущие настройки")
        parameters = ini.get_config_parameters(path, "DEFAULT")     # получаем параметры соединения
        my_connection = get_connection(parameters)  # подключаемся к базе
        break
    if case(2):
        print("Выберите нужное соединение")
        connection_name = ini.get_connections_list(path)
        try:
            answer = int(input("Укажите номер соединения\n"))
        except ValueError:
            answer = 0
        parameters = ini.get_config_parameters(path, connection_name[answer - 1])
        ini.update_default_section(path, parameters)
        my_connection = get_connection(parameters)  # подключаемся к базе
        break
    if case(3):
        print("Укажите новые параметры")
        new_section = ini.create_new_section(path)
        ini.update_default_section(path, new_section)
        my_connection = get_connection(new_section)  # подключаемся к базе
        break
    print("Указали некорректный вариант")
    break

    print("Указали некорректный вариант")
    break



