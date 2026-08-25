from pathlib import Path


class ValidateNotNone:

    @staticmethod
    def validate(
        value: str | Path | None,
        message: str | None = None,
    ) -> str | Path:
        if value is None:
            raise ValueError(message or "Value cannot be null!")

        return value
