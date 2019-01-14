import time
import ini_files.ini as ini
from xml.etree import ElementTree as et
import main_page.xml_requests.xml as my_xml
from main_page.client import Client
from db_operations.db_requests import get_user_fp_code_from_idn as get_fp_code


def __create_xml_coy():
    """  перезапись xml с новым кодом клента """
    current_time = time.strftime('%Y%m%d%H%M%S')
    xml_file = 'xml_requests/COY_find_info.xml'
    user = Client()
    idn = user.set_idn()
    fp_code = get_fp_code(idn)
    try:
        tree = et.parse('xml_request\COY_find_info.xml')
        tree.find('.//TerminalTime').text = current_time
        tree.find('.//BankId').text = user.get_fp_code()
        tree.write('xml_request\COY_find_info.xml')
    except FileNotFoundError:
        pass


def __get_url_coy():
    """
    Получение url СОУ для отправки запроса
    :return: url
    """
    path = "connections.ini"
    url = ""
    try:
        parameters = ini.get_config_parameters(path, 'COY')
        server = parameters[1]
        port = parameters[2]
        sid = parameters[3]
        url = 'http://' + server + ':' + port + sid
    except:
        pass
    return url

def send_coy_request():
    """  создание соединения, отправка запроса и вывод результата ответа """
    __create_xml_coy()
    url = __get_url_coy()
    xml = my_xml.xml_read('xml_requests/COY_find_info.xml')
    response = my_xml.xml_request_coy(url, xml)
    print(response)
    return response



