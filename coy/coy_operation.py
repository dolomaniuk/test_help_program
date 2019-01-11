import time

from xml.etree import ElementTree as et
import requests

import ini_files.ini as ini
from db_operations.db_requests import get_user_fp_code_from_idn


class Client:
    def get_fp_code(self):
        idn = get_user_fp_code_from_idn()
        return idn


def __create_xml_coy():
    current_time = time.strftime('%Y%m%d%H%M%S')
    new_client = Client()
    try:
        tree = et.parse('xml_request\COY_find_info.xml')
        tree.find('.//TerminalTime').text = current_time
        tree.find('.//BankId').text = new_client.get_fp_code()
        tree.write('xml_request\COY_find_info.xml')
    except FileNotFoundError:
        pass


def send_coy_request():
    __create_xml_coy()
    path = "connections.ini"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    parameters = ini.get_config_parameters(path, 'COY')
    server = parameters[1]
    port = parameters[2]
    sid = parameters[3]
    url = 'http://' + server + ':' + port + sid
    print(url)
    try:
        xml_request = open('xml_request\COY_find_info.xml', encoding='utf-8').read()
        param_data = {'xml': xml_request}
        response = requests.post(url, data=param_data, headers=headers).text
    except requests.exceptions.HTTPError as err:
        print('Response is: {content}'.format(content=err.response.content))
        response = ''
    except FileNotFoundError:
        print('Не удалось найти файл COY_find_info.xml')
        response = ''
    except requests.exceptions.ConnectionError:
        response = ''
    except requests.exceptions.InvalidURL:
        response = ''
    print(response)



