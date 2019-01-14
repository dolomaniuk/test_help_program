import urllib3
import time
import ini_files.ini as ini
from main_page.xml_requests.xml import xml_read, xml_request

urllib3.disable_warnings()  # для обхода ошибки Unverified HTTPS request is being made.
                            #  Adding certificate verification is strongly advised


def _input_count_of_request():
    """  возвращает кол-во создаваемых предзаявок """
    try:
        count_request = int(input("Укажите количество предзаявок\n"))
    except ValueError:
        print('Указали некорректное значение. Будет создана 1 предзаявка')
        count_request = 1
    return count_request


def _create_url_for_request():
    """ создание url адреса для отправки запроса на создание предзаявки"""
    path = "connections.ini"
    print("Выберите нужное соединение, где создавать предзаявку")
    connection_name = ini.get_connections_list(path)
    try:
        answer = int(input("Укажите номер соединения\n"))
        parameters = ini.get_config_parameters(path, connection_name[answer - 1])
        server = parameters[1]
        port = parameters[2]
        url = 'https://' + server + ':' + port + '/itwCredo/seam/resource/rest/CreateRequestService'
    except ValueError:
        print("Нет сохраненных соединений, либо указали неверный номер")
        url = ""
    return url


def request():
    """  создание соединения и отправка сигнала для создания предзаявки """
    start_time = time.time()
    xml = xml_read('xml_requests/Prerequest.xml')
    if xml is not False:
        url = _create_url_for_request()
        count = _input_count_of_request()
        for i in range(count):
            prerequest = xml_request(url, xml)
            print(f"Заявка: {i + 1} - {prerequest.split()[4].lstrip('<RequestId>').rstrip('</RequestId>')}")
        print(f"Время создания {i + 1} предзаявок составило: {time.time() - start_time}")
