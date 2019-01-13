import os


def check_files():
    """ проверка наличия необходимых файлов"""
    db_dir = 'sql_requests\\'
    xml_dir = 'xml_request\\'
    db_requests = [
        'cards.sql',
        'Fp_card_balance.sql',
        'ppl_code.sql'
        ]
    xml_requests = [
        'SV_card_status.xml',
        'SV_check_balance.xml',
        'Prerequest.xml',
        'COY_find_info.xml'
        ]
    err_list = []
    if not os.path.isfile('connections.ini'):
        err_list.append('connections.ini')
    for file in db_requests:
        if not os.path.isfile(db_dir + file):
            err_list.append(file)
    for file in xml_requests:
        if not os.path.isfile(xml_dir + file):
            err_list.append(file)
    if err_list:
        print("Для полноценной работы необходимы следующие файлы:", *err_list, sep='\n', end='\n')
