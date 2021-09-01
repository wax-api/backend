from aiohttp.web import Request


class Mapper:
    def __init__(self, request: Request):
        self.request = request
