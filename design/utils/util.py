class ReturnCode():
    SUCCESS = 0
    FAILED = -100
    UNAUHORIZED = -500
    @classmethod
    def message(cls,code):
        if code == cls.SUCCESS:
            return "success"
        elif code == cls.FAILED:
            return "failed"
        elif code == cls.UNAUHORIZED:
            return 'unauthrized'
        else:
            return ''

def wrap_json_response(data=None,code=None,message=None):
    response = {}
    if not code:
        code = ReturnCode.SUCCESS
    if not message:
        message = ReturnCode.message(code)
    if data:
        response['data'] = data
    response['result_code'] = code
    response['message'] = message
    return response

class CommonResponseMixin():
    @classmethod
    def wrap_json_response(data=None, code=None, message=None):
        response = {}
        if not code:
            code = ReturnCode.SUCCESS
        if not message:
            message = ReturnCode.message(code)
        if data:
            response['data'] = data
        response['result_code'] = code
        response['message'] = message

def is_authorized(request):
    is_authorized = False
    if request.session.get("is_authorized"):
        is_authorized = True
    return is_authorized
