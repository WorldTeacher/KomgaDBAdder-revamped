#create a logger
import logging
import os

class log:
    def __init__(self) -> None:
        logging.basicConfig(filename='program_log.log',level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.api=logging.getLogger('API')
        self.main=logging.getLogger('Main')
        self.webrequest=logging.getLogger('WebRequest')
        self.db=logging.getLogger('DB')
    def info_api(self,message):
        self.api.info(message)
    def error_api(self,message):
        self.api.error(message)
    def debug_api(self,message):
        self.api.debug(message)
    def warning_api(self,message):
        self.api.warning(message)
    def critical_api(self,message):
        self.api.critical(message)
    def fatal_api(self,message):
        self.api.fatal(message)
    def info_main(self,message):
        self.main.info(message)
    def error_main(self,message):
        self.main.error(message)
    def debug_main(self,message):
        self.main.debug(message)
    def warning_main(self,message):
        self.main.warning(message)
    def critical_main(self,message):
        self.main.critical(message)
    def fatal_main(self,message):
        self.main.fatal(message)
    def info_webrequest(self,message):
        self.webrequest.info(message)
    def error_webrequest(self,message):
        self.webrequest.error(message)
    def debug_webrequest(self,message):
        self.webrequest.debug(message)
    def warning_webrequest(self,message):
        self.webrequest.warning(message)
    def critical_webrequest(self,message):
        self.webrequest.critical(message)
    def fatal_webrequest(self,message):
        self.webrequest.fatal(message)



        

