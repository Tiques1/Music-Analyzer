class LinkError(Exception):
    pass


class UnknownLink(LinkError):
    pass


class GetError(LinkError):
    pass


class WrongLink(LinkError):
    pass


class IncorrectlySpecified(LinkError):
    pass
