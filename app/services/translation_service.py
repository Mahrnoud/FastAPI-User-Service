import json
from pathlib import Path
from ..core.config import settings


class TranslationService:
    def __init__(self, locale: str = None):
        # Use provided locale or default language from settings
        self.locale = locale or settings.DEFAULT_LANGUAGE
        self.translations = self.load_translations()

    def load_translations(self):
        locale_file = Path(__file__).parent.parent / "locales" / f"{self.locale}.json"

        try:
            with open(locale_file, "r", encoding="utf-8") as file:
                translations = json.load(file)
                if not translations:  # Handle empty file case
                    raise ValueError("Translation file is empty")
                return translations
        except (FileNotFoundError, ValueError):
            # Fallback to the default locale if the file is missing, empty, or invalid
            default_locale_file = Path(__file__).parent.parent / "locales" / f"{settings.DEFAULT_LANGUAGE}.json"
            try:
                with open(default_locale_file, "r", encoding="utf-8") as file:
                    return json.load(file)
            except FileNotFoundError:
                raise Exception(f"Default translation file '{settings.DEFAULT_LANGUAGE}.json' not found.")

    def get(self, key: str):
        keys = key.split(".")
        result = self.translations
        for k in keys:
            result = result.get(k)
            if result is None:
                return key  # Fallback to the key itself if translation is missing
        return result
