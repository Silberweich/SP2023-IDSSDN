def ResponseFormat(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorFormat(code, message):
    return {
        "code": code,
        "error": message,
    }