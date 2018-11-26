import requests
import urllib3
from db_operations.db_requests import get_users_cards
from xml.etree import ElementTree as et

urllib3.disable_warnings()  # для обхода ошибки Unverified HTTPS request is being made.
                            #  Adding certificate verification is strongly advised


def _get_card_status_from_SV():
    headers = {'Content-Type': 'text/xml'}  # set what your server accepts
    try:
        xml_request = open('SV_card_status.xml', encoding='utf-8').read()
        url = 'http://192.168.0.18:18080/itwGateWS/exec/XmlApi'
        response = requests.post(url, data=xml_request.encode('utf-8'),
                                 headers=headers, verify=False).text
    except requests.exceptions.HTTPError as err:
        print('Oops. HTTP Error occured')
        print('Response is: {content}'.format(content=err.response.content))
        response = ''
    except FileNotFoundError:
        print('Не удалось найти файл SV_card_status.xml')
        response = ''
    return response


def send_request_to_SV():
    tree = et.parse('SV_card_status.xml')
    cards_list = get_users_cards()
    for cardNumber in cards_list:
        tree.find('.//parameter[@name="cardNo"]').text = cardNumber
        tree.write('SV_card_status.xml')
        response = _get_card_status_from_SV().split()[7][18:20:]  # оставляем только код карточки
        print(f"card№ {cardNumber} SV_st - {response} Forpost_st - "
              f"{cards_list[cardNumber][0]} # {cards_list[cardNumber][1]}")
