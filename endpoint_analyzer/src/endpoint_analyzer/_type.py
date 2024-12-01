class Type:

    BASE_TYPES = [
        ("ROOT", (lambda x: not x)),
        ("NUMBER", (lambda x: x.isnumeric())),
        ("RESOURCE", (lambda x: "." in x)),
        ("SIMPLE", (lambda x: x.isalnum())),
        ("COMPOSITE", (lambda x: "-" in x or "_" in x)),
        ("COMPLEX", (lambda x: x)),
    ]

    @classmethod
    def deduce(cls, value):
        for identifier, predicate in cls.BASE_TYPES:
            if predicate(value):
                return (identifier, predicate)
        return cls.exact(value)

    @classmethod
    def exact(cls, value):
        return (f"'{value}'", lambda x: x == value)

    @classmethod
    def is_exact(cls, type_name):
        return type_name.startswith("'")

    @classmethod
    def is_root(cls, type_name):
        return type_name == "ROOT"

    @classmethod
    def is_resource(cls, type_name):
        return type_name == "RESOURCE"

    @classmethod
    def is_number(cls, type_name):
        return type_name == "NUMBER"

    @classmethod
    def is_instance(cls, left_type, right_type):
        if not (Type.is_exact(left_type) and not Type.is_exact(right_type)):
            return False
        value = left_type.strip("'")
        return Type.deduce(value) == right_type

    @classmethod
    def regex_for(cls, type_name):
        regex = ""
        if type_name == "NUMBER":
            regex = "\\d+"
        elif type_name == "RESOURCE":
            regex = ".+\\..+"
        elif type_name == "SIMPLE":
            regex = "[a-zA-Z0-9]+"
        elif type_name == "COMPOSITE":
            regex = "[a-zA-Z0-9\\-\\_]+"
        elif type_name == "COMPLEX":
            regex = ".+"
        return regex
