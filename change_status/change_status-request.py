import cx_Oracle
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


def get_connection(parameter):
    dbUrl = parameter[4] + '/' + parameter[5] + '@' + parameter[1] + '/' + parameter[3]
    connect = cx_Oracle.connect(dbUrl)
    cursor = connect.cursor()
    connection = connect, cursor
    return connection


def select_status_request(cursor, id):
    request_list = cursor.execute("select id, status from requests where ID = " + id)
    # for result in connect:
    print(*request_list)

def select_status():
    status = ('START', 'DECISION', 'REJECT_CLIENT', 'EXTERNAL_END', 'END')
    i = 1
    print("Список статусов:")
    for x in status:
        print(f"{i}-{x}")
        i += 1
    try:
        status_number = int(input("Укажите номер нового статуса\n"))
    except ValueError:
        print("Указали неверный номер статуса.\nНа заявку будет"
              " установлен статус 'EXTERNAL_END'")
        status_number = 3
    return status[status_number-1]


def change_status():
    while True:
        try:
            idRequest = int(input("Укажите номер заявки\n"))
            select_status_request(my_connection[1], str(idRequest))
            new_status = select_status()
            my_connection[1].execute(
                "update requests set status = '" + new_status + "' where ID = " + str(
                    idRequest))
            my_connection[0].commit()
            select_status_request(my_connection[1], str(idRequest))
        except ValueError:
            print("Указали неверное значение\n")
        else:
            break


def close_connection(connect):
    connect[1].close()
    connect[0].close()

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

change_status()
close_connection(my_connection)
