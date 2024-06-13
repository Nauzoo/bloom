from os import system
from sys import exit

system("color")
default_msg = '\033[91m' + '!ERR0r : ' + '\033[0m'


class ERROR:

    @staticmethod
    def throw_error(details, line=None, colon=None):
        message = default_msg + details

        if line is not None and colon is not None:
            message += f' ln:{line}, cl:{colon}'

        print(message)
        exit()
