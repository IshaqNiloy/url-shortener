from rest_framework.response import Response


def response(code: dict, status: str, data=None):
    if data:
        code['data'] = data

    return Response(data=code, status=status)
