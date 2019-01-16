import urllib3
import main_page.xml_requests.xml_operations as my_xml
from prettytable import PrettyTable
from db_operations.db_requests import get_users_cards
from db_operations.db_requests import get_Fp_card_balance
from xml.etree import ElementTree as et

urllib3.disable_warnings()  # для обхода ошибки Unverified HTTPS request is being made.
                            #  Adding certificate verification is strongly advised

STATUS_XML_FILE = 'xml_requests/SV_card_status.xml'
BALANCE_XML_FILE = 'xml_requests/SV_check_balance.xml'
URL = 'http://192.168.0.18:18080/itwGateWS/exec/XmlApi'

def _get_SV_card_status(card_number):
    """
    Ф-я отправки запроса в СВ и получения статуса карточки
    :return: статус карточки
    """
    tree_status = et.parse(STATUS_XML_FILE)
    my_xml.xml_replace(tree_status, './/parameter[@name="cardNo"]', card_number, STATUS_XML_FILE)
    xml = my_xml.xml_read(STATUS_XML_FILE)
    response_sv = my_xml.xml_request(URL, xml).split()[7]
    start_pos_status = response_sv.find('statusCode">') + 12
    end_pos_status = response_sv.find("</param")
    card_status = response_sv[start_pos_status:end_pos_status]
    return '-' if card_status == '' else card_status


def _get_SV_card_balance(card_number):
    """
    Ф-я отправки запроса в СВ и получения баланса карточки
    :return: баланс карточки
    """
    tree_status = et.parse(BALANCE_XML_FILE)
    my_xml.xml_replace(tree_status, './/parameter[@name="2"]', card_number, BALANCE_XML_FILE)
    xml = my_xml.xml_read(BALANCE_XML_FILE)
    response_sv = my_xml.xml_request(URL, xml).split()[-5]  # баланс карточки
    start_pos_balance = response_sv.find("4") + 3
    end_pos_balance = response_sv.find("</param")
    card_balance = float(response_sv[start_pos_balance:end_pos_balance]) / 100
    return card_balance


def check_status_SV():
    """  Вывод на экран карточек и их параметров """
    if my_xml.xml_read(STATUS_XML_FILE):
        cards_table = PrettyTable()
        cards_table.field_names = ["card", "accaunt", "contract", "Fp", "SV"]
        cards_list = get_users_cards()
        for card_number in cards_list:
            card_status = _get_SV_card_status(card_number)
            cards_list[card_number].append(card_status)
            cards_table.add_row([card_number, cards_list[card_number][0], cards_list[card_number][2],
                                 cards_list[card_number][1], card_status])
        print(cards_table)


def check_balance_status_SV_FP():
    """  получение баланса и статуса карточки в форпост и в смартвиста """
    if my_xml.xml_read(STATUS_XML_FILE) and my_xml.xml_read(BALANCE_XML_FILE):
        cards_table = PrettyTable()
        cards_table.field_names = ["card", "accaunt", "contract", "Fp", "SV", "SV_balance", "Fp_balance"]
        cards_list = get_Fp_card_balance()
        for card_number in cards_list:
            card_status = _get_SV_card_status(card_number)
            card_balance = _get_SV_card_balance(card_number)
            cards_table.add_row([card_number, cards_list[card_number][0], cards_list[card_number][2],
                                 cards_list[card_number][1], card_status, card_balance, cards_list[card_number][3]])
        print(cards_table)
