from app.core.exceptions import BadRequestError


class ResetTokenValidationError(BadRequestError):
    error_code = "BAD_REQUEST_ERROR"

    def __init__(self, msg) -> None:
        super().__init__(f"{msg}")
