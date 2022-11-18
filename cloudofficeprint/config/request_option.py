class requestOptions:
    def __init__(self,
                 url: str,
                 extraHeaders: object,
                 ):
        super()
        self.url = url
        self.extraHeaders = extraHeaders

    @property
    def as_dict(self):
        result = {}
        result['url'] = self.url
        result['extra_headers'] = self.extraHeaders
        return result
