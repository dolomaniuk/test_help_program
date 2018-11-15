import configparser
import os


def create_config(config, path):
    config.add_section("DEFAULT1")
    config.set("DEFAULT1", "SERVER", "192.168.0.1")
    config.set("DEFAULT1", "PORT", "12345")
    config.set("DEFAULT1", "SID", "sid")
    config.set("DEFAULT1", "USERNAME", "username")
    config.set("DEFAULT1", "PASSWORD", "password")
    write_config(config, path)


def get_config(path):
    conf = configparser.ConfigParser()
    if not os.path.exists(path):
        create_config(conf, path)
    conf.read(path)
    return conf


def get_config_parameters(path, section):
    config = get_config(path)
    server = config.get(section, "SERVER")
    port = config.get(section, "PORT")
    sid = config.get(section, "SID")
    username = config.get(section, "USERNAME")
    password = config.get(section, "PASSWORD")
    connection_parameters = section, server, port, sid, username, password
    return connection_parameters

def get_setting(path, section, setting):
    conf = get_config(path)
    value = conf.get(section, setting)
    msg = f"{section} {setting} is {value}"
    print(msg)


def update_setting(path, section, setting, value):
    config = get_config(path)
    config.set(section, setting, value)
    write_config(config, path)


def update_default_section(path, parameters):
    config = get_config(path)
    section = "DEFAULT"
    config.set(section, "SERVER", parameters[1])
    config.set(section, "PORT", parameters[2])
    config.set(section, "SID", parameters[3])
    config.set(section, "USERNAME", parameters[4])
    config.set(section, "PASSWORD", parameters[5])
    write_config(config, path)
    print("Обновили default значения текущими")


def create_new_section(path):
    config = get_config(path)
    section = input_section()
    config.add_section(section)
    server = input_server()
    config.set(section, "SERVER", server)
    port = input_port()
    config.set(section, "PORT", port)
    sid = input_sid()
    config.set(section, "SID", sid)
    username = input_username()
    config.set(section, "USERNAME", username)
    password = input_password()
    config.set(section, "PASSWORD", password)
    write_config(config, path)
    print("\nЗаписали новое подключение")
    get_config_parameters(path, section)
    connection_parameters = section, server, port, sid, username, password
    return connection_parameters


def write_config(config, path):
    with open(path, "w") as config_file:
        config.write(config_file)


# Input connection's parameters


def input_section():
    section = input("Укажите название соединения):\n").upper()
    return section


def input_server():
    server = input("Укажите server (пример: 192.168.0.1):\n")
    return server


def input_port():
    port = input("Укажите port (пример: 1234):\n")
    return port


def input_sid():
    sid = input("Укажите SID:\n")
    return sid


def input_username():
    username = input("Укажите username:\n").lower()
    return username


def input_password():
    password = input("Укажите password:\n").lower()
    return password


def get_connections_list(path):
    config = get_config(path)
    sections = config.sections()
    i = 1  # count of connections
    for x in sections:
        parameters = get_config_parameters(path, x)
        print(f"{i}. {parameters[0]}\n{parameters[1]}:{parameters[2]}:{parameters[3]} {parameters[4]} {parameters[5]}", sep='\n')
        i += 1
    return sections
