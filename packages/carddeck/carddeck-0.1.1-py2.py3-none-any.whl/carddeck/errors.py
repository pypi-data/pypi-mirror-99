#define Python obj exceptions

class Error(Exception):
    """Base class for other exceptions"""
    pass


class NeedHands(Error):
    """Need deck class as input"""
    pass
