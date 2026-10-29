class GenerationError(RuntimeError):
    """Safe error raised when story generation cannot produce a valid payload."""

    def __init__(self, user_message: str, cause: Exception | None = None):
        super().__init__(user_message)
        self.user_message = user_message
        self.cause = cause
