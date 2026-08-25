from pathlib import Path
from tempfile import gettempdir
from uuid import uuid4


def get_temp_folder() -> Path:
    folder = Path(gettempdir()) / "writit"
    folder.mkdir(parents=True, exist_ok=True)

    return folder


def create_temp_file(folder: str | Path, extension: str) -> Path:
    folder = Path(folder)
    extension = extension.lstrip(".")

    filename = f"{uuid4().hex}.{extension}"
    file = folder / filename

    file.touch()

    return file
