import urllib3
import main_page.xml_requests.xml as my_xml
from prettytable import PrettyTable # для вывода в виде таблицы
from db_operations.db_requests import get_users_cards
from db_operations.db_requests import get_Fp_card_balance
from xml.etree import ElementTree as et

urllib3.disable_warnings()  # для обхода ошибки Unverified HTTPS request is being made.
                            #  Adding certificate verification is strongly advised

def _get_SV_card_status(card_number):
    """
    Ф-я отправки запроса в СВ и получения статуса карточки
    :return: статус карточки
    """
    xml_file = 'xml_requests/SV_card_status.xml'
    url = 'http://192.168.0.18:18080/itwGateWS/exec/XmlApi'
    tree_status = et.parse(xml_file)
    my_xml.xml_replace(tree_status, './/parameter[@name="cardNo"]', card_number, xml_file)
    xml = my_xml.xml_read(xml_file)
    card_status = my_xml.xml_request(url, xml).split()[7][18:20:]  # код карточки
    return '-' if card_status == '</' else card_status


def _get_SV_card_balance(card_number):
    """
    Ф-я отправки запроса в СВ и получения баланса карточки
    :return: баланс карточки
    """
    xml_file = 'xml_requests/SV_check_balance.xml'
    url = 'http://192.168.0.18:18080/itwGateWS/exec/XmlApi'
    tree_status = et.parse(xml_file)
    my_xml.xml_replace(tree_status, './/parameter[@name="2"]', card_number, xml_file)
    xml = my_xml.xml_read(xml_file)
    card_status = my_xml.xml_request(url, xml).split()[-5][10:21:]  # баланс карточки
    return '-' if card_status == '</' else card_status


def check_status_SV():
    """  Вывод на экран карточек и их параметров """
    xml_file = 'xml_requests/SV_card_status.xml'
    if my_xml.xml_read(xml_file):
        cards_table = PrettyTable()
        cards_table.field_names = ["card", "accaunt", "contract", "Fp", "SV"]
        cards_list = get_users_cards()
        for card_number in cards_list:
            card_status = _get_SV_card_status(card_number)
            cards_list[card_number].append(card_status)
            cards_table.add_row([card_number, cards_list[card_number][0], cards_list[card_number][2],cards_list[card_number][1], card_status])
            # print(card_number, cards_list[card_number][0], cards_list[card_number][2],cards_list[card_number][1], card_status)
        print(cards_table)


def check_balance_status_SV_FP():
    """  получение баланса и статуса карточки в форпост и в смартвиста """
    status_xml_file = 'xml_requests/SV_card_status.xml'
    balance_xml_file = 'xml_requests/SV_check_balance.xml'
    if my_xml.xml_read(status_xml_file) and my_xml.xml_read(balance_xml_file):
        cards_table = PrettyTable()
        cards_table.field_names = ["card", "accaunt", "contract", "Fp", "SV", "SV_balance", "Fp_balance"]
        cards_list = get_Fp_card_balance()
        for card_number in cards_list:
            card_status = _get_SV_card_status(card_number)
            card_balance = _get_SV_card_balance(card_number)
            cards_table.add_row([card_number, cards_list[card_number][0], cards_list[card_number][2],
                                 cards_list[card_number][1], card_status, card_balance, cards_list[card_number][3]])
        print(cards_table)