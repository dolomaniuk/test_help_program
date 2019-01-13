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
