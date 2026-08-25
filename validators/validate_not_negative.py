class ValidateNotNegative:

    @staticmethod
    def validate(
        value: int,
        message: str | None = None,
    ) -> int:
        if value < 0:
            raise ValueError(message or "Value cannot be negative!")

        return value
