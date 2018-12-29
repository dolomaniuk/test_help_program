""""
Database module.
"""

import cx_Oracle
import ini_files.ini as ini


class My_db_Default(object):

    def __init__(self):
        parameter = ini.get_config_parameters('connect_to_base.ini', "DEFAULT")
        _dbUrl = parameter[4] + '/' + parameter[5] + '@' + parameter[1] + '/' + \
                 parameter[3]
        try:
            self._connect = cx_Oracle.connect(_dbUrl)
            self._cursor = self._connect.cursor()
        except Exception as error:
            print(f'Error: connection not established {error}')

    def query(self, query):
        return self._cursor.execute(query)

    def __del__(self):
        self._connect.close()


class My_db_Forpost(My_db_Default):
    def __init__(self):
        parameter = ini.get_config_parameters('connect_to_base.ini', "FORPOST")
        _dbUrl = parameter[4] + '/' + parameter[5] + '@' + parameter[1] + '/' + \
                 parameter[3]
        try:
            self._connect = cx_Oracle.connect(_dbUrl)
            self._cursor = self._connect.cursor()
        except Exception as error:
            print(f'Error: connection not established {error}')


def __select_status_request(db_obj, id):
    request_list = db_obj.query(
        f"select id, status from requests where ID = {id}").fetchone()
    print(request_list)


def __select_status():
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
    return status[status_number - 1]


# меняем статус заявки
def change_status():
    db = My_db_Default()
    while True:
        try:
            id_request = int(input("Укажите номер заявки\n"))
            __select_status_request(db, str(id_request))
            new_status = __select_status()
            db.query(f"UPDATE requests SET status = '{new_status}' WHERE ID = "
                     f"{str(id_request)}")
            db._connect.commit()
            __select_status_request(db, str(id_request))
        except ValueError:
            print("Указали неверное значение\n")
        except IndexError:
            print("Указали неверное значение\nСтатус не меняем")
        else:
            break


# поиск в базе установленного апдейта
def find_update():
    db = My_db_Default()
    script_name = input("Укажите номер задачи или название скрипта\n")
    request_list = db.query(f"SELECT * FROM databaseupdatehistory WHERE "
                            f"upd_version LIKE '%{script_name}%'")

    count_of_rows = request_list.fetchall()  # get list of rows
    if count_of_rows:
        print(*count_of_rows, sep='\n')
    else:
        print('Не найден апдейт с описанием: ' + script_name)


# Получение списка карточек клиента #
def get_users_cards():
    cards_list = {}
    param = []
    request = ''
    try:
        idn = input("Укажите идентификационный номер клиента\n")
        with open('sql_requests\cards.sql', 'r+', encoding='utf-8') as sql:
            for line in sql:
                request += line.replace("idn", idn)
        db = My_db_Forpost()
        print('Подождите... формируется писок карточек...')
        response = db.query(request)
        for i in response:
            param.append(i[1])          # номер счета
            param.append(i[2])          # статус в Fp
            param.append(i[3])          # номер контракта
            param.append(i[4])          # номер контракта
            cards_list[i[0]] = param    # номер карточки
            param = []
    except ValueError:
        print("Указали неверное значение\n")
    if not cards_list.keys():
        print("У данного клиента нет активных карточек")
    return cards_list


def get_user_fp_code_from_idn():
    try:
        idn = input("Укажите идентификационный номер клиента\n")
        request = "SELECT ppl_code FROM s_people where ppl_perscode = '" + str(idn) + "'"
        db = My_db_Forpost()
        response = db.query(request)
        for i in response:
            fp_code = str(i[0])
            break
    except ValueError:
        print("Указали неверное значение\n")
        fp_code = ''
    return fp_code
