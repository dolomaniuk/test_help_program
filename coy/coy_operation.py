import time
import ini_files.ini as ini
import main_page.xml_requests.xml as my_xml
import logging
from xml.etree import ElementTree as et
from main_page.client import Client
from db_operations.db_requests import get_user_fp_code_from_idn as get_fp_code
from prettytable import PrettyTable


logging.basicConfig(filename="logs/request.log", filemode="w", level=logging.INFO)
log = logging.getLogger("coy_operation")

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
        log.exception(FileNotFoundError)
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
        log.info("Сформировали url для отправки запроса")
    except:
        log.exception("Формирование url. Не смогли считать параметры")
        pass
    return url

def send_coy_request():
    """  создание соединения, отправка запроса и вывод результата ответа """
    __create_xml_coy()
    url = __get_url_coy()
    xml = my_xml.xml_read('xml_requests/COY_find_info.xml')
    response = my_xml.xml_request_coy(url, xml)
    user_parameters = parse_response_coy(response)
    user_table = PrettyTable()
    column_names = ["Параметр", "Значение"]
    user_table.add_column(column_names[0], ["Id", "FIO", "Address", "Phone", "Email", "DateOfBirth", "Sex", "BankId",
                                            "PersonalNo", "Document", "Options"])
    second_column = []
    for i in user_parameters:
        second_column.append(i)
    user_table.add_column(column_names[1], second_column)
    print(user_table)
    log.info("Вывели инфу о клиенте")
    return response


def parse_response_coy(response):
    """
    вывод ответа из СОУ в читаемый вид
    :param response: xml
    :return: преобразованная инфа из СОУ
    """
    xml = et.fromstring(response)
    Id = xml.find('.//Id').text
    FIO = xml.find('.//FIO').text
    Address = xml.find('.//Address').text
    Phone = xml.find('.//Phone').text
    try:
        Email = xml.find('.//Email').text
    except:
        Email = "no email"
    DateOfBirth = xml.find('.//DateOfBirth').text
    Sex = xml.find('.//Sex').text
    BankId = xml.find('.//BankId').text
    PersonalNo = xml.find('.//PersonalNo').text
    Document = xml.find('.//Document').text
    try:
        Options = xml.find('.//Options').text
    except:
        Options = "no options"

    user = [Id, FIO, Address, Phone, Email, DateOfBirth, Sex, BankId, PersonalNo, Document, Options]
    log.info("Преобразовали ответ из СОУ в нормальный вид")
    return user
