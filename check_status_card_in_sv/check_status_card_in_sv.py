import requests
import urllib3
# from prettytable import PrettyTable # для вывода в виде таблицы
from db_operations.db_requests import get_users_cards
from db_operations.db_requests import get_Fp_card_balance
from xml.etree import ElementTree as et
urllib3.disable_warnings()  # для обхода ошибки Unverified HTTPS request is being made.
                            #  Adding certificate verification is strongly advised


def _get_card_status_from_SV(xml_file):
    headers = {'Content-Type': 'text/xml'}  # set what your server accepts
    try:
        xml_request = open(xml_file, encoding='utf-8').read()
        url = 'http://192.168.0.18:18080/itwGateWS/exec/XmlApi'
        response = requests.post(url, data=xml_request.encode('utf-8'),
                                 headers=headers, verify=False).text
    except requests.exceptions.HTTPError as err:
        print('Oops. HTTP Error occured')
        print('Response is: {content}'.format(content=err.response.content))
        response = ''
    except FileNotFoundError:
        print('Не удалось найти файл: ' + xml_file)
        response = ''
    return response


def manipulation_xml(parse_xml, search_text, card_number, xml_file):
    parse_xml.find(search_text).text = card_number
    parse_xml.write('xml_request\'' + xml_file)


def check_status_SV():
    status_xml_file = 'xml_request\SV_card_status.xml'
    tree_status = et.parse(status_xml_file)
    cards_list = get_users_cards()
    for cardNumber in cards_list:
        manipulation_xml(tree_status, './/parameter[@name="cardNo"]', cardNumber, status_xml_file)
        resp_status = _get_card_status_from_SV('xml_request\SV_card_status.xml').split()[7][18:20:]     # код карточки
        resp_status = '-' if resp_status == '</' else resp_status
        cards_list[cardNumber].append(resp_status)
        print(f"{cardNumber}\t{cards_list[cardNumber][0]} \t{cards_list[cardNumber][2]}"
              f" \t{cards_list[cardNumber][1]} \t{resp_status}")


def check_balance_SV_FP():
    status_xml_file = 'xml_request\SV_card_status.xml'
    balance_xml_file = 'xml_request\SV_check_balance.xml'
    tree_status = et.parse(status_xml_file)
    tree_balance = et.parse(balance_xml_file)
    cards_list = get_Fp_card_balance()
    for cardNumber in cards_list:
        manipulation_xml(tree_status, './/parameter[@name="cardNo"]', cardNumber, status_xml_file)
        manipulation_xml(tree_balance, './/parameter[@name="2"]', cardNumber, balance_xml_file)
        card_status = _get_card_status_from_SV(status_xml_file).split()[7][18:20:]  # код карточки
        card_balance = _get_card_status_from_SV(balance_xml_file).split()[-5][10:21:]  # баланс карточки
        print(f"{cardNumber}\t{cards_list[cardNumber][0]} \t{cards_list[cardNumber][2]}"
              f" \t{cards_list[cardNumber][1]} \t{card_status} \t{card_balance}"
              f"\t\t{cards_list[cardNumber][3]}  ")
