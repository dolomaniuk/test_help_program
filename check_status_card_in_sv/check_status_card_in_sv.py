import urllib3
from main_page.xml_requests.xml import xml_read, xml_request
# from prettytable import PrettyTable # для вывода в виде таблицы
from db_operations.db_requests import get_users_cards
from db_operations.db_requests import get_Fp_card_balance
from xml.etree import ElementTree as et

urllib3.disable_warnings()  # для обхода ошибки Unverified HTTPS request is being made.
                            #  Adding certificate verification is strongly advised


def manipulation_xml(parse_xml, search_text, card_number, xml_file):
    """  замена номера карточки в xml и его сохранение """
    parse_xml.find(search_text).text = card_number
    parse_xml.write(xml_file)


def check_status_SV():
    """  получение статуса карточки в СВ и вывод на экран """
    # TODO: ckeck print (*cards_list) print(*cards)
    if xml_read('SV_card_status.xml'):
        status_xml_file = 'xml_request/SV_card_status.xml'
        url = 'http://192.168.0.18:18080/itwGateWS/exec/XmlApi'
        tree_status = et.parse(status_xml_file)
        cards_list = get_users_cards()
        # cards = []
        for cardNumber in cards_list:
            manipulation_xml(tree_status, './/parameter[@name="cardNo"]', cardNumber, status_xml_file)
            xml = xml_read(status_xml_file)
            resp_status = xml_request(url, xml).split()[7][18:20:]  # код карточки
            resp_status = '-' if resp_status == '</' else resp_status
            cards_list[cardNumber].append(resp_status)
            # cards.append(cardNumber, cards_list[cardNumber][0], cards_list[cardNumber][2],
            #              cards_list[cardNumber][1], resp_status)
        print(*cards_list, sep='\t')
        # print(*cards, sep='\t')


def check_balance_status_SV_FP():
    """  получение баланса и статуса карточки в форпост и в смартвиста """
    url = 'http://192.168.0.18:18080/itwGateWS/exec/XmlApi'
    status_xml_file = 'xml_request/SV_card_status.xml'
    balance_xml_file = 'xml_request/SV_check_balance.xml'
    if xml_read(status_xml_file) and xml_read(balance_xml_file):
        tree_status = et.parse(status_xml_file)
        tree_balance = et.parse(balance_xml_file)
        cards_list = get_Fp_card_balance()
        cards = []
        for cardNumber in cards_list:
            manipulation_xml(tree_status, './/parameter[@name="cardNo"]', cardNumber, status_xml_file)
            manipulation_xml(tree_balance, './/parameter[@name="2"]', cardNumber, balance_xml_file)
            request_status = xml_read(status_xml_file)
            request_balance = xml_read(balance_xml_file)
            card_status = xml_request(url, request_status).split()[7][18:20:]  # код карточки
            card_balance = xml_request(url, request_balance).split()[-5][10:21:]  # баланс карточки
            cards.append(cardNumber, cards_list[cardNumber][0], cards_list[cardNumber][2],
                         cards_list[cardNumber][1], card_status, card_balance, cards_list[cardNumber][3])
        print(*cards, sep='\t')
