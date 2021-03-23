class Path_not_found_exception(Exception):
    """
    Attributes:
        message -- explanation of why the specific transition is not allowed
    """

    def __init__(self, *message):
        self.message = message
