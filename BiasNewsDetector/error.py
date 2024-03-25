def error_handler(error_code):
    if error_code == -2:
        return "HTTP 403 Forbidden"
    else:
        return f"Unidentified Error. Please contact JTCX\nTraceback: {error_code}"
        
def error_parser(exception):
    if exception == 1:
        return -2
    else:
        print(exception)
        return -1