from telegram.ext import BaseFilter
from config import PASSWORD


class PassFilter(BaseFilter):
    def filter(self, message):
        return PASSWORD == message.text


class DBPassFilter(BaseFilter):
    def __init__(self,command):
        self.command = command
        super(DBPassFilter,self).__init__()

    def filter(self, message):
        if message:
            return True


class AddDBFilter(BaseFilter):
    def filter(self, message):
        global last_command
        if last_command == '/add_db':
            last_command = ""
            return True

pass_filter = PassFilter()
add_db_filter = AddDBFilter()
