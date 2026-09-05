from translations.base_translation import BaseTranslation


class EnglishAmerican(BaseTranslation):

    TRANSLATIONS: dict[str, str] = {
        "project.file.resume": "summary.md",
        "project.folder.meta": "meta",
        "project.folder.parted": "part_",
        "project.folder.chaptered": "chapters",
        "project.folder.standalone": "text",
        "date.long_format": "«day» «month» «year»",
        "date.month.01": "January",
        "date.month.02": "February",
        "date.month.03": "March",
        "date.month.04": "April",
        "date.month.05": "May",
        "date.month.06": "June",
        "date.month.07": "July",
        "date.month.08": "August",
        "date.month.09": "September",
        "date.month.10": "October",
        "date.month.11": "November",
        "date.month.12": "December",
    }
