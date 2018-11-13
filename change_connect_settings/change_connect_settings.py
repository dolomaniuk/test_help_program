import ini_files.create_ini_file as ini


# объявление 2х функций для switch-case
class switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))



def choice_thing()
    path = "connect_to_base.ini"
    print("Текущие настройки:")
    print(*ini.get_config_parameters(path, "DEFAULT"))
    print("\nКакие настройки подключения использовать:")
    try:
        answer = int(input("1-использовать текущие\n"
                           "2-установить другие\n"
                           "3-ввести новые\n"))
    except ValueError:
        answer = 0

    while switch(answer):
        if case(1):
            print("используем текущие настройки")
            parameters = ini.get_config_parameters(path, "DEFAULT")     # получаем параметры соединения
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
            break
        if case(3):
            print("Укажите новые параметры")
            new_section = ini.create_new_section(path)
            ini.update_default_section(path, new_section)
            break
        print("Указали некорректный вариант")
        break

