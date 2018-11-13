import requests
import urllib3
import time


urllib3.disable_warnings()  # для обхода ошибки Unverified HTTPS request is being made.
                            #  Adding certificate verification is strongly advised


def input_server():
    server = input("Укажите server (пример: 192.168.0.1):\n")
    return server


def input_port():
    port = input("Укажите port (пример: 1234):\n")
    return port


def input_count_of_request():
    try:
        count_request = int(input("Укажите количество предзаявок\n"))
    except ValueError:
        print('Указали некорректное значение. Будет создана 1 предзаявка')
        count_request = 1
    return count_request


def send_request(url, xml, count_requests):
    headers = {'Content-Type': 'text/xml'}  # set what your server accepts
    start_time = time.time()
    for i in range(count_requests):
        try:
            req = requests.post(url, data=xml.encode('utf-8'), headers=headers,
                                verify=False).text  # verify=False - для обхода SSL
            print(
                f"Заявка: {i+1} - {req.split()[4].lstrip('<RequestId>').rstrip('</RequestId>')}")
        except requests.exceptions.HTTPError as err:
            print('Oops. HTTP Error occured')
            print(f'Response is: {err.response.content}')
    print(
        f"Время создания {i+1} предзаявок составило: {time.time() - start_time}")


def request():
    try:
        xml_request = open('request.xml', encoding='utf-8').read()
        server = input_server()
        port = input_port()
        count = input_count_of_request()
        url = 'https://' + server + ':' + port + '/itwCredo/seam/resource/rest/CreateRequestService'
        send_request(url, xml_request, count)
    except ValueError:
        print('Не удалось открыть request.xml файл с запросом')
    except FileNotFoundError:
        print('Не удалось найти файл request.xml')





