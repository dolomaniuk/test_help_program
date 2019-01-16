import logging

LOG_FORMAT = "%(asctime)s [%(levelname)s]\t [%(name)s]\t %(message)s"
logging.basicConfig(filename="logs/request.log", format=LOG_FORMAT, datefmt='%H:%M:%S', filemode="w", level=logging.INFO)
log = logging.getLogger("client")


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
