text = """
╔══╗╔══╗╔══╗╔════╗──╔═══╗╔══╗
║╔═╝║╔╗║║╔═╝╚═╗╔═╝──║╔═╗║║╔╗║
║╚═╗║╚╝║║╚═╗──║║────║║─║║║╚╝║
║╔═╝║╔╗║╚═╗║──║║────║║╔╝║║╔╗║
║║──║║║║╔═╝║──║║────║╚╝─║║║║║
╚╝──╚╝╚╝╚══╝──╚╝────╚═══╝╚╝╚╝
"""

import db_operations.db_requests as db
from change_connect_settings.change_connect_settings import choice_thing
from prerequest.create_prerequest import request
from check_status_card_in_sv.check_status_card_in_sv import check_balance_SV_FP, check_status_FP_SV
from coy.coy_operation import send_coy_request

path = "connect_to_base.ini"


# объявление 2х функций для switch-case
class _switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True


def _case(*args):
    return any((arg == _switch.value for arg in args))


print(text)

while 1:
    print(
        """
        1. Изменить настройки соединеня
        2. Изменить статус заявки
        3. Проверить установку обновлений в db
        4. Создать предзаявку
        5. Статус карточек клиента в SV
        6. Баланс карточки по номеру договора
        7. Инфа о клиенте в СОУ
        """)
    try:
        choice = int(input('Выберите один из вариантов\n'))
    except ValueError:
        choice = 0
    while _switch(choice):
        if _case(1):
            print("Изменить настройки соединеня")
            choice_thing()
            print('\n\n')
            break
        if _case(2):
            print("Изменить статус заявки")
            db.change_status()
            print('\n\n')
            break
        if _case(3):
            print("Проверить установку обновлений в db")
            db.find_update()
            print('\n\n')
            break
        if _case(4):
            print("Создание предзаявки")
            request()
            print('\n\n')
            break
        if _case(5):
            print("Статус карточек клиента в SV")
            check_status_FP_SV()
            # check_balance_SV_FP()
            print('\n\n')
            break
        if _case(6):
            print("Баланс карточки по номеру договора")
            check_balance_SV_FP()
            print('\n\n')
            break
        if _case(7):
            print("Инфа о клиенте в СОУ")
            send_coy_request()
            print('\n\n')
            break
        print("Указали некорректный вариант")
        break
