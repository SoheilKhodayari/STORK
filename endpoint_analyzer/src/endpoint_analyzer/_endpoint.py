class Endpoint:
    def __init__(self, domain_type_trace, path_type_trace):
        self.domain_type_trace = domain_type_trace
        self.path_type_trace = path_type_trace
        self.parameters = set()

    def add_parameter(self, parameter):
        self.parameters.add(parameter)

    def __repr__(self):
        domain = ".".join(self.domain_type_trace)
        path = "/".join(self.path_type_trace)
        params = "&".join([str(p) for p in self.parameters])
        return f"{domain}/{path}?{params}"

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__
            and self.domain_type_trace == other.domain_type_trace
            and self.path_type_trace == other.path_type_trace
        )

    def __hash__(self):
        return hash((self.domain_type_trace, self.path_type_trace))
