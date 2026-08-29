from translations.base_translation import BaseTranslation


class PortugueseEuropean(BaseTranslation):

    TRANSLATIONS: dict[str, str] = {
        "project.file.resume": "resumo.md",
        "project.folder.meta": "meta",
        "project.folder.parted": "parte_",
        "project.folder.chaptered": "capitulos",
        "project.folder.standalone": "texto",
    }
