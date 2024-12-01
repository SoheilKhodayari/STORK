from urllib.parse import urlparse, unquote, parse_qsl
from .logging import get_logger


class Parameter:
    def __init__(self, name, type, encoding):
        self.name = name
        self.type = type
        self.encoding = encoding

    def __repr__(self):
        return f"{self.name}={self.type}:{self.encoding}"

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__
            and self.name == other.name
            and self.type == other.type
            and self.encoding == other.encoding
        )

    def __hash__(self):
        return hash((self.name, self.type, self.encoding))

    BASE_TYPES = [
        ("URL", (lambda x: urlparse(x).scheme)),
        ("NUMBER", (lambda x: x.isnumeric())),
        ("RESOURCE", (lambda x: x.count(".") == 1)),
        ("PATH", (lambda x: not urlparse(x).scheme and "/" in x)),
        ("VALUE", (lambda x: not urlparse(x).scheme)),
    ]

    @classmethod
    def deduce(cls, value):
        for identifier, predicate in cls.BASE_TYPES:
            try:
                if predicate(value):
                    return (identifier, predicate)
            except Exception as e:
                error_msg = repr(e)
                get_logger(__name__).warn(error_msg)
        error_msg = f"Unknow value type for parameter value {value}"
        get_logger(__name__).warn(error_msg)
        get_logger(__name__).warn(f"Falling back to type: VALUE")
        return cls.BASE_TYPES[-1]

    @classmethod
    def is_url_encoded(cls, value):
        return value != unquote(value)

    @classmethod
    def is_double_url_encoded(cls, value):
        if Parameter.is_url_encoded(value):
            unquoted = unquote(value)
            return unquoted != unquote(unquoted)

    @classmethod
    def from_url(cls, url):
        parameters = set()
        parsed_url = urlparse(url)
        qsl = parse_qsl(parsed_url.query, keep_blank_values=True)
        for key, value in qsl:
            # Retain original encoding
            if value not in url:
                tmp = parsed_url.query.partition(f"{key}=")[2]
                value = tmp.partition("&")[0]
            name = key
            type, _ = Parameter.deduce(value)
            encoding = None
            if Parameter.is_double_url_encoded(value):
                encoding = "DOUBLE_ULR_ENCODED"
                value = unquote(unquote(value))
                type, _ = Parameter.deduce(value)
            elif Parameter.is_url_encoded(value):
                encoding = "URL_ENCODED"
                value = unquote(value)
                type, _ = Parameter.deduce(unquote(value))
            parameters.add(Parameter(name, type, encoding))
        return parameters
