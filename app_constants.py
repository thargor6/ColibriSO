# Language Constants
LANGUAGE_EN = 'en'
LANGUAGE_FA = 'fa'
LANGUAGE_DE = 'de'
LANGUAGE_FR = 'fr'

PART_URL = 'url'
PART_CONTENT = 'content'
PART_SUMMARY = 'summary'

METADATA_TITLE = 'title'
METADATA_LANGUAGE = 'language'

def getLanguageName(language_id):
    if language_id == LANGUAGE_EN:
        return "English"
    if language_id == LANGUAGE_FA:
        return "Farsi"
    if language_id == LANGUAGE_DE:
        return "German"
    if language_id == LANGUAGE_FR:
        return "French"
    return "Unknown"
