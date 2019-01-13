import requests
import urllib3
import time
import ini_files.ini as ini

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


def _send_request(url, xml, count_requests):
    """  отправка сигнала для создания предзаявки и вывод ответа """
    headers = {'Content-Type': 'text/xml'}
    start_time = time.time()
    for i in range(count_requests):
        try:
            req = requests.post(url, data=xml.encode('utf-8'), headers=headers,
                                verify=False).text  # verify=False - для обхода SSL
            print(req)
            print(
                f"Заявка: {i+1} - {req.split()[4].lstrip('<RequestId>').rstrip('</RequestId>')}")
        except requests.exceptions.HTTPError as error:
            print('Oops. HTTP Error occured')
            print(f'Response is: {error.response.content}')
        except ConnectionRefusedError as error:
            print(f'Oops. Error connection: {error}')
    print(
        f"Время создания {i+1} предзаявок составило: {time.time() - start_time}")


def request():
    """  создание соединения и отправка сигнала для создания предзаявки """
    #TODO: разделить на несколько ф-ций
    path = "connections.ini"
    try:
        xml_request = open('xml_request\Prerequest.xml', encoding='utf-8').read()
        print("Выберите нужное соединение, где создавать предзаявку")
        connection_name = ini.get_connections_list(path)
        try:
            answer = int(input("Укажите номер соединения\n"))
            parameters = ini.get_config_parameters(path,
                                                   connection_name[answer - 1])
            server = parameters[1]
            port = parameters[2]
            count = _input_count_of_request()
            url = 'https://' + server + ':' + port + '/itwCredo/seam/resource/rest/CreateRequestService'
            _send_request(url, xml_request, count)
        except ValueError:
            print("Нет сохраненных соединений, либо указали неверный номер")
    except ValueError:
        print('Не удалось открыть Prerequest.xml файл с запросом')
    except FileNotFoundError:
        print('Не удалось найти файл Prerequest.xml')





