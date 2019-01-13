""""
Database module.
"""

import cx_Oracle
import ini_files.ini as ini
from main_page.client import Client


class My_db_Default(object):
    """ класс создания подключения к баззе """
    def __init__(self, section):
        parameter = ini.get_config_parameters('connections.ini', section)
        _dbUrl = parameter[4] + '/' + parameter[5] + '@' + parameter[1] + '/' + \
                 parameter[3]
        try:
            self._connect = cx_Oracle.connect(_dbUrl)
            self._cursor = self._connect.cursor()
        except:
            print('Не удалось установить соединение')

    def query(self, query):
        """ выполнение sql запроса """
        try:
            request = self._cursor.execute(query)
        except:
            print("Не удалось выполнить запрос")
            request = None
        return request


    def __del__(self):
        try:
            self._connect.close()
        except:
            pass


def prepare_sql_file(sql_file, text_for_replase, value):
    """
    :return: sql с измененным idn клиента
    """
    sql_request = ""
    with open(sql_file, 'r+', encoding='utf-8') as sql:
        for line in sql:
            sql_request.join(line.replace(text_for_replase, value))
    return sql_request


def __select_status_request(db_obj, id):
    """ выводит статуса заявки """
    try:
        request_list = db_obj.query(
        f"select id, status from requests where ID = {id}").fetchone()
        print(request_list)
    except:
        print("Не удалось выполнить запрос.")
        # request_list = ''


def __select_status():
    """  возвращает выбранный статус """
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


def change_status():
    """  обновляет статус заявки в БД """
    db = My_db_Default("DEFAULT")
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


def find_update():
    """  поиск в базе установленного апдейта """
    db = My_db_Default("DEFAULT")
    script_name = input("Укажите номер задачи или название скрипта\n")
    request_list = db.query(f"SELECT * FROM databaseupdatehistory WHERE "
                            f"upd_version LIKE '%{script_name}%'")

    count_of_rows = request_list.fetchall()  # get list of rows
    if count_of_rows:
        print(*count_of_rows, sep='\n')
    else:
        print('Не найден апдейт с описанием: ' + script_name)


def get_users_cards():
    """ Получение списка карточек клиента из БД """
    cards_list = {}
    param = []
    sql_file = 'sql_requests/cards.sql'
    user = Client()
    idn = user.set_idn()
    try:
        request = prepare_sql_file(sql_file, "idn", idn)
        db = My_db_Default("FORPOST")
        print('Подождите... формируется список карточек...')
        response = db.query(request)
        for i in response:
            param.append(i[1])          # номер счета
            param.append(i[2])          # статус в Fp
            param.append(i[3])          # номер контракта
            cards_list[i[0]] = param    # номер карточки
            param = []
    except ValueError:
        print("Указали неверное значение\n")
    except TypeError:
        pass
    if not cards_list.keys():
        print("У данного клиента нет активных карточек")
    else:
        print("№ card\t\t\t\t Accaunt \t\t\t\t\t\tcontract\tFp\tSV")
    return cards_list


def get_Fp_card_balance():
    """  получение списка карточек вместе со статусом и балансом в форпост """
    cards_list = {}
    param = []
    sql_file = 'sql_requests/Fp_card_balance.sql'
    try:
        deal_nr = input("Укажите номер контракта\n")
        request = prepare_sql_file(sql_file, "contract_nr", deal_nr)
        db = My_db_Default("FORPOST")
        response = db.query(request)
        for i in response:
            param.append(i[1])          # номер счета
            param.append(i[2])          # статус в Fp
            param.append(i[3])          # номер контракта
            param.append(i[4])          # баланс в Fp
            cards_list[i[0]] = param    # номер карточки
            param = []
    except ValueError:
        print("Указали неверное значение\n")
    if not cards_list.keys():
        print("У данного контракта нет активных карточек")
    else:
        print("№ card\t\t\t\t Accaunt \t\t\t\t\t\tcontract\tFp\tSV\tSV_balance\tFp_balance")
    return cards_list


def get_user_fp_code_from_idn(idn):
    """  получение кода форпост через idn клиента """
    sql_file = 'sql_requests/ppl_code.sql'
    try:
        request = prepare_sql_file(sql_file, "idn", idn)
        db = My_db_Default("FORPOST")
        response = db.query(request)
        for i in response:
            fp_code = str(i[0])
    except:
        print("Не удалось определить fp_code\n")
        fp_code = ''
    return fp_code
