# MIT License
#
# ColibriSO - a tool for organizing information of all kinds, written in Python and Streamlit.
# Copyright (C) 2022-2024 Andreas Maschke
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Language Constants
APP_NAME = "ColibriSO"
APP_VERSION = "0.26.0"
APP_VERSION_DATE = "2024-03-16"

LANGUAGE_EN = 'en'
LANGUAGE_FA = 'fa'
LANGUAGE_DE = 'de'
LANGUAGE_FR = 'fr'

LANGUAGE_EN_CAPTION = 'English'
LANGUAGE_FA_CAPTION = 'Farsi'
LANGUAGE_DE_CAPTION = 'German'
LANGUAGE_FR_CAPTION = 'French'

PART_URL = 'url'
PART_CONTENT = 'content'
PART_SUMMARY_BRIEF = 'summary_brief'
PART_SUMMARY_COMPREHENSIVE = 'summary_comprehensive'
PART_EXPLANATION_BRIEF = 'explanation_brief'
PART_EXPLANATION_COMPREHENSIVE = 'explanation_comprehensive'
PART_PRIMARY = 'primary'

METADATA_TITLE = 'title'
METADATA_LANGUAGE = 'language'

SESSION_USER_ID = "user_id"
SESSION_USER_EMAIL = "user_email"
SESSION_USER_OPEN_AI_API_KEY = "user_open_ai_api_key"
SESSION_PASSWORD_CORRECT = "password_correct"

ROUTE_ABOUT = "about"
ROUTE_ADD_PDF = "add_pdf"
ROUTE_ADD_URL = "add_url"
ROUTE_CHAT = "chat"
ROUTE_CONFIGURATION = "configuration"
ROUTE_DOCUMENTS = "documents"
ROUTE_EXPLAIN = "explain"
ROUTE_LOGOUT = "logout"
ROUTE_OPTIONS = "options"
ROUTE_PODCASTS = "podcasts"
ROUTE_TRANSLATE = "translate"

MIMETYPE_PDF = "application/pdf"
MIMETYPE_MP3 = "audio/mp3"

UI_DEFAULT_TEXT_AREA_HEIGHT = 400
UI_DEFAULT_TEXT_AREA_MAX_CHARS = 10000

OPENAI_DFLT_MODEL = 'gpt-4'
OPENAI_DFLT_TEMPERATURE = 0.0

OPENAI_DFLT_SPEECH_CHUNKSIZE = 4000
OPENAI_DFLT_SPEECH_MODEL_SPEED = "tts-1"
OPENAI_DFLT_SPEECH_MODEL_QUALITY = "tts-1-hd"
OPENAI_DFLT_SPEECH_MODEL = OPENAI_DFLT_SPEECH_MODEL_QUALITY


SPEECH_VOICE_ALLOY = 'alloy'
SPEECH_VOICE_ECHO = 'echo'
SPEECH_VOICE_FABLE = 'fable'
SPEECH_VOICE_ONYX = 'onyx'
SPEECH_VOICE_NOVA = 'nova'
SPEECH_VOICE_SHIMMER = 'shimmer'
OPENAI_DFLT_SPEECH_VOICE = SPEECH_VOICE_SHIMMER

def getLanguageCaption(language_id):
    if language_id == LANGUAGE_EN:
        return LANGUAGE_EN_CAPTION
    if language_id == LANGUAGE_FA:
        return LANGUAGE_FA_CAPTION
    if language_id == LANGUAGE_DE:
        return LANGUAGE_DE_CAPTION
    if language_id == LANGUAGE_FR:
        return LANGUAGE_FR_CAPTION
    return None

def getLanguageId(language_caption):
    if language_caption == LANGUAGE_EN:
        return LANGUAGE_EN_CAPTION
    if language_caption == LANGUAGE_FA:
        return LANGUAGE_FA_CAPTION
    if language_caption == LANGUAGE_DE:
        return LANGUAGE_DE_CAPTION
    if language_caption == LANGUAGE_FR:
        return LANGUAGE_FR_CAPTION
    return None
