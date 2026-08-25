class ValidateNotEmpty:

    @staticmethod
    def validate(
        value: str | None,
        message: str | None = None,
    ) -> str:
        if value is None:
            raise ValueError(message or "Value cannot be empty!")

        value = value.strip()

        if not value:
            raise ValueError(message or "Value cannot be empty!")

        return value
