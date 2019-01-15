import logging

logging.basicConfig(filename="logs/request.log", filemode="w", level=logging.INFO)
log = logging.getLogger("Client")

class Client(object):

    def __init__(self):
        self.idn = ""
        self.fp_code = ""

    def set_idn(self):
        """ устанавливает и возвращает л.н. клиента """
        while self.idn == "":
            self.idn = input("Укажите идентификационный номер клиента\n")
            log.info("Указали л.н: " + self.idn)
        return self.idn

    def get_idn(self):
        log.info("Возвращаем л.н: " + self.idn)
        return self.idn
