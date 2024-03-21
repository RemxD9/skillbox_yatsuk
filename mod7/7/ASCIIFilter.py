import logging


class ASCIIFilter(logging.Filter):
    def filter(self, record):
        try:
            record.msg.encode('ascii')
        except UnicodeEncodeError:
            return False
        return True
