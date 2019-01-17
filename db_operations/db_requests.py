""""
Database module.
"""

import cx_Oracle
import ini_files.ini as ini
import logging
from main_page.client import Client

LOG_FORMAT = "%(asctime)s [%(levelname)s]\t [%(name)s]\t %(message)s"
logging.basicConfig(filename="logs/request.log", format=LOG_FORMAT, datefmt='%H:%M:%S', filemode="w", level=logging.INFO)
log = logging.getLogger("db_request")


class My_db_Default(object):
    """ класс создания подключения к баззе """
    def __init__(self, section):
        parameter = ini.get_config_parameters('connections.ini', section)
        _dbUrl = parameter[4] + '/' + parameter[5] + '@' + parameter[1] + '/' + \
                 parameter[3]
        try:
            self._connect = cx_Oracle.connect(_dbUrl)
            self._cursor = self._connect.cursor()
            log.info("Установили соединение к " + section)
        except:
            log.exception("Не удалось установить соединение к " + section)
            print('Не удалось установить соединение к ' + section)

    def query(self, query):
        """ выполнение sql запроса """
        try:
            request = self._cursor.execute(query)
            log.info("Выполнили sql запрос и получили ответ")
        except:
            print("Не удалось выполнить запрос")
            request = None
            log.exception("Не удалось выполнить sql запрос")
        return request


    def __del__(self):
        try:
            self._connect.close()
        except:
            pass


def prepare_sql_file(sql_file, text_for_replace, value):
    """
    :return: sql с измененным idn клиента
    """
    sql_request = ""
    with open(sql_file, 'r+', encoding='utf-8') as sql:
        for line in sql:
            sql_request += line.replace(text_for_replace, value)
        sql.write()
        log.info("Прочитали sql запрос из файла: " + sql_file)
    return sql_request


def __select_status_request(db_obj, id):
    """ выводит статуса заявки """
    try:
        request_list = db_obj.query(f"select id, status from requests where ID = {id}").fetchone()
        print(request_list)
        log. info("Получили статус заявки")
    except:
        print("Не удалось определить статус заявки")
        log.exception("Не удалось определить статус заявки")


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
        log.info("Выбрали новый статус")
    except ValueError:
        print("Указали неверный номер статуса.\nНа заявку будет"
              " установлен статус 'EXTERNAL_END'")
        log.exception("Указали неверный номер статуса")
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
        except :
            print("Указали неверное значение\n")
            log.exception()
        else:
            log.error("что то передумали вводить...")
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
        log.info("Нашли соответствие в БД")
    else:
        print('Не найден апдейт с описанием: ' + script_name)


def get_users_cards():
    """ Получение списка карточек клиента из БД """
    log.info("get_users_cards() enter")
    cards_list = {}
    param = []
    SQL_FILE = 'sql_requests/cards.sql'
    user = Client()
    idn = user.set_idn()
    try:
        request = prepare_sql_file(SQL_FILE, "idn", idn)
        db = My_db_Default("FORPOST")
        print('Подождите... формируется список карточек...\n'
              'Может занять около минуты...')
        response = db.query(request)
        for i in response:
            param.append(i[1])          # номер счета
            param.append(i[2])          # статус в Fp
            param.append(i[3])          # номер контракта
            cards_list[i[0]] = param    # номер карточки
            param = []
        log.info("get_users_cards() exit")
    except ValueError:
        print("Указали неверное значение\n")
        log.exception("Указали неверное значение\n")
    except TypeError:
        log.exception(TypeError)
        pass
    if not cards_list.keys():
        print("У данного клиента нет активных карточек")
        log.info("У данного клиента нет активных карточек")
    return cards_list


def get_Fp_card_balance():
    """  получение списка карточек вместе со статусом и балансом в форпост """
    cards_list = {}
    param = []
    SQL_FILE = 'sql_requests/Fp_card_balance.sql'
    try:
        deal_nr = input("Укажите номер контракта\n")
        request = prepare_sql_file(SQL_FILE, "contract_nr", deal_nr)
        db = My_db_Default("FORPOST")
        print('Подождите... формируется таблица с данными...')
        response = db.query(request)
        for i in response:
            param.append(i[1])          # номер счета
            param.append(i[2])          # статус в Fp
            param.append(i[3])          # номер контракта
            param.append(i[4])          # баланс в Fp
            cards_list[i[0]] = param    # номер карточки
            param = []
            log.info(f"Получили данные по контракту {deal_nr}")
    except:
        print("Указали неверное значение\n")
        log.exception()
    if not cards_list.keys():
        print("У данного контракта нет активных карточек")
        log.info("У данного контракта нет активных карточек")
    return cards_list


def get_user_fp_code_from_idn(idn):
    """  получение кода форпост через idn клиента """
    SQL_FILE = 'sql_requests/ppl_code.sql'
    try:
        request = prepare_sql_file(SQL_FILE, "idn", idn)
        db = My_db_Default("FORPOST")
        response = db.query(request)
        for i in response:
            fp_code = str(i[0])
        log.info(f"Получили fp_code= {fp_code}")
    except:
        print("Не удалось определить fp_code\n")
        fp_code = ''
        log.exception("Не удалось определить fp_code")
    return fp_code


def get_cards_number_for_auto_credit():
    """
    :param vrc_pdt_mnemo: карточный продукт 'INSTANT_ISSUE_PURCHASE'
    :param vrc_mnemo: карточный вариант 'PS_MC_ST_NFC'
    :return: Группу точек выдачи, точку выдачи, номер карочки
    """
    request_list = []
    cursor = My_db_Default("FORPOST")
    query = """
            
            """
    request_list = cursor.query(query).fetchone()
    log.info(f"Получили точку выдачи и номер карточки для автокредита")
    return request_list