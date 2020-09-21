import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
logFormatter = logging.Formatter("[%(levelname)s] Helpdesk V1 %(asctime)s %(module)s - %(funcName)s:%(lineno)s %(message)s", "%Y-%m-%d %H:%M:%S")

"""to print log on console"""
handler = logging.StreamHandler()
handler.setFormatter(logFormatter)
log.addHandler(handler)


'''to append log in file'''
file_handler = logging.FileHandler("logger.log", mode='a', encoding=None, delay=False)
file_handler.setFormatter(logFormatter)
log.addHandler(file_handler)
