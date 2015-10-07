
class DomainException(Exception):
    pass


class SomeVideosDontExistException(DomainException):
    def __init__(self, videos):
        self.arg = videos
    
    def __str__(self):
        return repr('\n'.join(self.arg))


class TooManyCommasException(DomainException):
    def __init__(self, arg):
        self.arg = arg
    
    def __str__(self):
        return repr(self.arg)
