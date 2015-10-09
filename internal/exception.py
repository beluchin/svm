
class DomainException(Exception):
    pass


class TooManyCommasException(DomainException):
    def __init__(self, arg):
        self.arg = arg
    
    def __str__(self):
        return repr(self.arg)
