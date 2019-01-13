from db_operations.db_requests import get_user_fp_code_from_idn


class Client(object):
    def __init__(self):
        self.idn = ""
        self.fp_code = ""

    def set_idn(self):
        """ устанавливает и возвращает л.н. клиента """
        while self.idn == "":
            self.idn = input("Укажите идентификационный номер клиента\n")
        return self.idn

    def get_idn(self):
        return self.idn

    def get_fp_code(self):
        fp_code = get_user_fp_code_from_idn(self.idn)
        return fp_code
