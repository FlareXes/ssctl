class InvalidDomainError(ValueError):
    """Raised when a domain or domain pattern is invalid."""

    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)
