from enum import Enum

class ExceptionEnum(Enum):
    BAD_REQUEST = ("Bad Request: Invalid request data", 400)
    USER_UNAUTHORIZED = ("유저 권한이 없습니다", 401)
    INVALID_TOKEN = ("토큰이 유효하지 않습니다.", 403)
    ITEM_NOT_FOUND = ("Item Not Found", 404)
    LOGIN_FAILED = ("아이디 또는 비밀번호를 잘못 입력하였습니다.", 404)
    USER_NOT_FOUND = ("사용자를 찾을 수 없습니다.", 404)
    USER_EXISTS = ("이미 사용 중인 ID입니다.", 409)
    TOKEN_EXPIRED = ("로그인 세션이 만료되었습니다.", 401)
    ITSOKEY_ERROR = ("도어락 KEY 연동에 실패하였습니다", 500)

    def __init__(self, detail, status_code):
        self.detail = detail
        self.status_code = status_code

class CustomException(Exception):
    def __init__(self, exception_enum: ExceptionEnum):
        self.detail = exception_enum.detail
        self.status_code = exception_enum.status_code

