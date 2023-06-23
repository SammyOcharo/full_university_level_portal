
class CustomExceptions(Exception):
    default_detail = 'database error occured.'
    default_code = '4012'

    def __init__(self, detail=None, code=None):
        self.detail = detail or self.default_detail
        self.code = code or self.default_code

        super.__init__(detail)