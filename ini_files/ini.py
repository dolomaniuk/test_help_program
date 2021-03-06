import configparser
import os
import logging
from prettytable import PrettyTable

LOG_FORMAT = "%(asctime)s [%(levelname)s]\t [%(name)s]\t %(message)s"
logging.basicConfig(filename="logs/request.log", format=LOG_FORMAT, datefmt='%H:%M:%S', filemode="w", level=logging.INFO)
log = logging.getLogger("db_request")


def _create_config(config, path):
    section = "DEFAULT1"
    config.add_section(section)
    config.set(section, "SERVER", "192.168.0.1")
    config.set(section, "PORT", "12345")
    config.set(section, "SID", "sid")
    config.set(section, "USERNAME", "username")
    config.set(section, "PASSWORD", "password")
    _write_config(config, path)
    parameters = get_config_parameters(path, section)
    update_default_section(path, parameters)


def get_config(path):
    conf = configparser.ConfigParser()
    if not os.path.exists(path):
        _create_config(conf, path)
    conf.read(path)
    return conf


def get_config_parameters(path, section):
    try:
        config = get_config(path)
        server = config.get(section, "SERVER")
        port = config.get(section, "PORT")
        sid = config.get(section, "SID")
        username = config.get(section, "USERNAME")
        password = config.get(section, "PASSWORD")
        connection_parameters = section, server, port, sid, username, password
    except :
        print(f"Не удалось определить параметры соединения {section}\n")
        log.exception(f"Не удалось определить параметры соединения {section}")
        connection_parameters = create_new_section(path)
    finally:
        return connection_parameters

def get_setting(path, section, setting):
    conf = get_config(path)
    value = conf.get(section, setting)
    msg = f"{section} {setting} is {value}"
    print(msg)


def update_setting(path, section, setting, value):
    config = get_config(path)
    config.set(section, setting, value)
    _write_config(config, path)
    log.info(f"Обновили соединение {section}")


def update_default_section(path, parameters):
    config = get_config(path)
    section = "DEFAULT"
    config.set(section, "SERVER", parameters[1])
    config.set(section, "PORT", parameters[2])
    config.set(section, "SID", parameters[3])
    config.set(section, "USERNAME", parameters[4])
    config.set(section, "PASSWORD", parameters[5])
    _write_config(config, path)
    print("Обновили default значения")


def create_new_section(path):
    config = get_config(path)
    section = _input_section()
    config.add_section(section)
    server = _input_server()
    config.set(section, "SERVER", server)
    port = _input_port()
    config.set(section, "PORT", port)
    sid = _input_sid()
    config.set(section, "SID", sid)
    username = _input_username()
    config.set(section, "USERNAME", username)
    password = _input_password()
    config.set(section, "PASSWORD", password)
    _write_config(config, path)
    print("\nЗаписали новое подключение")
    get_config_parameters(path, section)
    connection_parameters = section, server, port, sid, username, password
    log.info("Добавили новое соединение")
    return connection_parameters


def _write_config(config, path):
    with open(path, "w") as config_file:
        config.write(config_file)
    log.info("обновили конфиг")


# Input connection's parameters
def _input_section():
    section = input("Укажите название соединения:\n").upper()
    return section


def _input_server():
    server = input("Укажите server (пример: 192.168.0.1):\n")
    return server


def _input_port():
    port = input("Укажите port (пример: 1234):\n")
    return port


def _input_sid():
    sid = input("Укажите SID:\n")
    return sid


def _input_username():
    username = input("Укажите username:\n").lower()
    return username


def _input_password():
    password = input("Укажите password:\n").lower()
    return password


def get_connections_list(path):
    config = get_config(path)
    sections = config.sections()
    i = 1  # count of connections
    connections_list = PrettyTable()
    connections_list.field_names = ["№", "Name", "Adress", "User"]
    for x in sections:
        parameters = get_config_parameters(path, x)
        connections_list.add_row([i, parameters[0], parameters[1] + ":" + parameters[2] + ":" + parameters[3],
                                 parameters[4] + " " + parameters[5]])
        i += 1
    print(connections_list)
    log.info("Получили список соединений")
    return sections
