import requests


def xml_read(xml_file):
    """открытие и чтение xml файла"""
    try:
        xml_request = open(xml_file, encoding='utf-8').read()
        return xml_request
    except ValueError:
        print('Не удалось открыть ' + xml_file)
        return False
    except FileNotFoundError:
        print('Не удалось найти ' + xml_file)
        return False


def xml_request(url, xml):
    """Возвращает ответ на xml запрос"""
    response = ""
    if url != "":
        headers = {'Content-Type': 'text/xml'}
        try:
            response = requests.post(url, data=xml.encode('utf-8'), headers=headers,
                                     verify=False).text  # verify=False - для обхода SSL
        except requests.exceptions.HTTPError as error:
            print('Oops. HTTP Error occured')
            print(f'Response is: {error.response.content}')
        except ConnectionRefusedError as error:
            print(f'Oops. Error connection: {error}')
    return response


def xml_replace(parse_xml, search_text, value, new_xml):
    """
    замена номера карточки в xml и его сохранение
    parse_xml: распарсенный xml через et.parse(xml_file)
     """
    parse_xml.find(search_text).text = value
    parse_xml.write(new_xml)


def xml_request_coy(url, xml):
    """Возвращает ответ на xml запрос"""
    param_data = {'xml': xml}
    response = ""
    if url != "":
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        try:
            response = requests.post(url, data=param_data, headers=headers).text
        except requests.exceptions.HTTPError as error:
            print(f'Response is: {error.response.content}')
        except ConnectionRefusedError as error:
            print(f'Oops. Error connection: {error}')
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.InvalidURL:
            pass
    else:
        print("Не удалось сформировать ссылку для отправки запроса\n"
              "Проверьте настройки соединения COY")
    return response