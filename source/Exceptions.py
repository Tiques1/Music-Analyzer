class LinkError(Exception):
    pass


class UnknownLink(LinkError):
    pass


class GetError(LinkError):
    pass
