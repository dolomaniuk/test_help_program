text = """
╔══╗╔══╗╔══╗╔════╗──╔═══╗╔══╗
║╔═╝║╔╗║║╔═╝╚═╗╔═╝──║╔═╗║║╔╗║
║╚═╗║╚╝║║╚═╗──║║────║║─║║║╚╝║
║╔═╝║╔╗║╚═╗║──║║────║║╔╝║║╔╗║
║║──║║║║╔═╝║──║║────║╚╝─║║║║║
╚╝──╚╝╚╝╚══╝──╚╝────╚═══╝╚╝╚╝
"""

import os
import platform

LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

if platform.system() == "Linux":
    os.chdir("/usr/app/main_page")

import db_operations.db_requests as db
import ini_files.ini as ini
from change_connect_settings.change_connect_settings import choice_thing
from prerequest.create_prerequest import request
from check_status_card_in_sv.check_status_card_in_sv import check_balance_status_SV_FP, check_status_SV
from coy.coy_operation import send_coy_request
from main_page.check_nes_files import check_files
from main_page.createHuman import create_human

path = "connections.ini"

# объявление 2х функций для switch-case
class _switch(object):
    value = None

    def __new__(class_, value):
        """ ф-я выбора меню """
        class_.value = value
        return True


def _case(*args):
    """ ф-я возвращает нажатое значение меню """
    return any((arg == _switch.value for arg in args))


while 1:
    check_files()  # проверка необходимых файлов
    def_con = ' '.join([*ini.get_config_parameters(path, "DEFAULT")])
    print(
        """
        
        1. Изменить настройки соединеня (""" + def_con + """)
        2. Изменить статус заявки
        3. Проверить установку обновлений в db
        4. Создать предзаявку
        5. Статус карточек клиента в SV
        6. Баланс карточки по номеру договора
        7. Инфа о клиенте в СОУ
        8. Генерация тестовых данных
        """)
    try:
        choice = int(input('Выберите один из вариантов\n'))
    except ValueError:
        choice = 0
    while _switch(choice):
        if _case(1):
            print("Изменить настройки соединеня")
            try:
                choice_thing()
            except:
                print("Не удалось выполнить команду")
            finally:
                break
        if _case(2):
            print("Изменить статус заявки")
            try:
                db.change_status()
            except:
                print("Не удалось выполнить команду")
            finally:
                break
        if _case(3):
            print("Проверить установку обновлений в db")
            try:
                db.find_update()
            except:
                print("Не удалось выполнить команду")
            finally:
                break
        if _case(4):
            print("Создание предзаявки")
            try:
                request()
            except:
                print("Не удалось выполнить команду")
            finally:
                break
        if _case(5):
            print("Статус карточек клиента в SV")
            try:
                check_status_SV()
            except:
                print("Не удалось выполнить команду")
            finally:
                break
        if _case(6):
            print("Баланс карточки по номеру договора")
            try:
                check_balance_status_SV_FP()
            except:
                print("Не удалось выполнить команду")
            finally:
                break
        if _case(7):
            print("Инфа о клиенте в СОУ")
            try:
                send_coy_request()
            except:
                print("Не удалось выполнить команду")
            finally:
                break
        if _case(8):
            print("Генерация тестовых данных")
            create_human(1)
            keys = str(input('Press "Space" and next "Enter" to repeat\nor "Enter" to exit\n'))
            try:
                while keys[0] == ' ':
                    create_human(1)
                    keys = input('Press "Space" and next "Enter" to create new client again\nor "Enter" to exit\n')
            except:
                pass
            finally:
                break
        print("Указали некорректный вариант")
        break
