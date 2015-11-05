
class DomainException(Exception):
    def __init__(self, arg):
        self.arg = arg
    
    def __str__(self):
        return repr(self.arg)


class TooManyCommasException(DomainException):
    pass


class FailedToGetVideosFromPlaylistException(DomainException):
    pass