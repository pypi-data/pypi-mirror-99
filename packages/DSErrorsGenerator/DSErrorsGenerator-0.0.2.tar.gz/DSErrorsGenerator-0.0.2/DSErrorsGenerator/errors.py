class MissingArgument(Exception):
    #  Raised when one of the args is missing
    pass

class BadObjectType(Exception):
    #  Raised when type of object != expected type of object
    pass

class MissingEmoji(Exception):
    #  Raised when emoji hasn't emoji
    pass

class BadLanguage(Exception):
    #  Raised when language != "ru" or "en"
    pass