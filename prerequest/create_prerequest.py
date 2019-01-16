import urllib3
import time
from main_page.xml_requests.xml_operations import xml_read, xml_request

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
    answer = input("Укажите сервер и порт вашего сервера, так как он указан в адресной строке браузера\n")
    url = 'https://' + answer + '/itwCredo/seam/resource/rest/CreateRequestService'
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
