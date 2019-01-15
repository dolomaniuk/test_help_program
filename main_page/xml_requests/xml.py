import requests
import logging

logging.basicConfig(filename="logs/request.log", filemode="w", level=logging.INFO)
log = logging.getLogger("xml")

def xml_read(xml_file):
    """открытие и чтение xml файла"""
    try:
        xml_request = open(xml_file, encoding='utf-8').read()
        log.info("Прочитали " + xml_file)
        return xml_request
    except ValueError:
        print('Не удалось открыть ' + xml_file)
        log.exception(ValueError)
        return False
    except FileNotFoundError:
        print('Не удалось найти ' + xml_file)
        log.exception(FileNotFoundError)
        return False


def xml_request(url, xml):
    """Возвращает ответ на xml запрос"""
    response = ""
    if url != "":
        headers = {'Content-Type': 'text/xml'}
        try:
            response = requests.post(url, data=xml.encode('utf-8'), headers=headers,
                                     verify=False).text  # verify=False - для обхода SSL
            log.info("Получили ответ на xml запрос")
        except:
            log.exception()
    return response


def xml_replace(parse_xml, search_text, value, new_xml):
    """
    замена номера карточки в xml и его сохранение
    parse_xml: распарсенный xml через et.parse(xml_file)
     """
    parse_xml.find(search_text).text = value
    parse_xml.write(new_xml)
    log.info("Перезаписали xml файл")

def xml_request_coy(url, xml):
    """Возвращает ответ на xml запрос"""
    param_data = {'xml': xml}
    response = ""
    if url != "":
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        try:
            response = requests.post(url, data=param_data, headers=headers).text
            log.info("Получили ответ на xml запрос")
        except:
            log.exception()
            pass
    else:
        print("Не удалось сформировать ссылку для отправки запроса\n"
              "Проверьте настройки соединения COY")
        log.error("Не удалось сформировать ссылку для отправки запроса")
    return response
