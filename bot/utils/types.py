from enum import Enum, auto

class HttpMethod(Enum):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    PATCH = 'patch'
    DELETE = 'delete'

class ResponseType(Enum):
    JSON = 'json'
    TEXT = 'text'
    RAW = 'raw'

class Action(Enum):
    MAIN = auto()
    REGISTRATION = auto()
    TRANSACTION = auto()
                


