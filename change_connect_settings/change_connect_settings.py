import ini_files.ini as ini


# объявление 2х функций для switch-case
class _switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True

def _case(*args):
    return any((arg == _switch.value for arg in args))



def choice_thing():
    path = "connections.ini"
    print("Текущие настройки:")
    print(*ini.get_config_parameters(path, "DEFAULT"))
    print("\nКакие настройки подключения использовать:")
    try:
        answer = int(input("1-использовать текущие\n"
                           "2-установить другие\n"
                           "3-ввести новые\n"))
    except ValueError:
        answer = 0

    while _switch(answer):
        if _case(1):
            print("используем текущие настройки", end='')
            # ini.get_config_parameters(path, "DEFAULT")     # получаем параметры соединения
            break
        if _case(2):
            print("Выберите нужное соединение")
            connection_name = ini.get_connections_list(path)
            try:
                answer = int(input("Укажите номер соединения\n"))
                parameters = ini.get_config_parameters(path, connection_name[answer - 1])
                ini.update_default_section(path, parameters)
            except IndexError:
                print("Нет сохраненных соединений, либо указали неверный номер")
            break
        if _case(3):
            print("Ввод нового соединения")
            new_section = ini.create_new_section(path)
            # ini.update_default_section(path, new_section)
            break
        print("Указали некорректный вариант")
        break

