import cx_Oracle
import ini_files.create_ini_file as ini


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


def update_status():
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


def change_status():
    parameters = ini.get_config_parameters("connect_to_base.ini", "DEFAULT")     # получаем параметры соединения
    my_connection = get_connection(parameters)  # подключаемся к базе
    update_status()
    close_connection(my_connection)
