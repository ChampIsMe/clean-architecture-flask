class CovidCaseRequest:
    def __init__(self, filters=None, payload=None, errors=[]):
        self.errors = []
        self.filters = filters
        self.payload = payload

    def add_error(self, parameter, message):
        self.errors.append({"parameter": parameter, "message": message})

    def has_errors(self):
        return len(self.errors) > 0

    def __bool__(self):
        # if true, means this is a valid request else it is an invalid request with errors
        return not self.has_errors()


def build_covidcase_list_request(filters=None):
    return CovidCaseRequest(filters=filters)


def build_save_covidcase_request(payload):
    req = CovidCaseRequest()
    try:
        if payload is None:
            req.add_error("InvalidPayload", 'Error parsing payload')
            return req
        return CovidCaseRequest(payload=payload)
    except Exception as ex:
        req.add_error("InvalidPayload", 'Error parsing payload')
        return req
