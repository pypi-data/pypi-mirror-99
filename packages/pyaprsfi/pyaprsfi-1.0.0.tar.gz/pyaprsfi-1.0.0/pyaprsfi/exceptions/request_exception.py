class RequestException(Exception):
    def __init__(self):
        super().__init__("Invalid request")
