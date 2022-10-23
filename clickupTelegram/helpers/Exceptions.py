class CustomException(Exception):
    """Still an exception raised when uncommon things happen"""

    def __init__(self, message, payload=None):
        self.message = message
        self.payload = payload  # you could add more args

    def __str__(self):
        return str(self.message)
