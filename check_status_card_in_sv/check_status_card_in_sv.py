import requests
import urllib3
import ini_files.create_ini_file as ini
import change_request_status.change_status_request as db
from xml.etree import ElementTree as et

urllib3.disable_warnings()  # для обхода ошибки Unverified HTTPS request is being made.
                            #  Adding certificate verification is strongly advised


def get_users_cards():
    cards_list = {}
    param = []
    try:
        idn = input("Укажите идентификационный номер клиента\n")
        request = """SELECT crd_nr, crd_status, crd_deal_nr
                      FROM s_card WHERE
                      crd_deal_nr IN (
                      SELECT crt_mnemo FROM TABLE
                      (itw_sca.getAllCardsOfClient('""" + idn + """')))
                       AND crd_status NOT LIKE 'C' 
                      ORDER BY crd_status"""

        parameters = ini.get_config_parameters('connect_to_base.ini','FORPOST')
        my_connection = db.get_connection(parameters)  # подключаемся к базе
        response = my_connection[1].execute(request)
        for i in response:
            param.append(i[1])
            param.append(i[2])
            cards_list[i[0]] = param
            param = []
    except ValueError:
        print("Указали неверное значение\n")

    if not cards_list.keys():
        print("У данного клиента нет активных карточек")
    return cards_list


def get_card_status_from_SV():
    headers = {'Content-Type': 'text/xml'}  # set what your server accepts
    try:
        xml_request = open('SV_card_status.xml', encoding='utf-8').read()
        url = 'http://192.168.0.18:18080/itwGateWS/exec/XmlApi'
        response = requests.post(url, data=xml_request.encode('utf-8'), headers=headers,
                            verify=False).text
    except requests.exceptions.HTTPError as err:
        print('Oops. HTTP Error occured')
        print('Response is: {content}'.format(content=err.response.content))
    except FileNotFoundError:
        print('Не удалось найти файл SV_card_status.xml')
    return response


def send_request_to_SV():
    tree = et.parse('SV_card_status.xml')
    cards_list = get_users_cards()
    for cardNumber in cards_list:
        tree.find('.//parameter[@name="cardNo"]').text = cardNumber
        tree.write('SV_card_status.xml')
        response = get_card_status_from_SV().split()[7][18:20:]  # оставляем только код карточки
        print(f"card№ {cardNumber} SV_st - {response} Forpost_st - "
              f"{cards_list[cardNumber][0]} # {cards_list[cardNumber][1]}")
