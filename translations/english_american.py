from translations.base_translation import BaseTranslation


class EnglishAmerican(BaseTranslation):

    TRANSLATIONS: dict[str, str] = {
        "project.file.resume": "summary.md",
        "project.folder.meta": "meta",
        "project.folder.parted": "part_",
        "project.folder.chaptered": "chapters",
        "project.folder.standalone": "text",
    }
