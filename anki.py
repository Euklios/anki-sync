import json
from typing import Dict

import requests

from data.NoteDetails import NoteDetails
from data.Settings import Settings
from utils import map_fields

ANKI_HOST = "http://localhost:8765/"
PRONUNCIATION_FIELD = 'Pronunciation'


def anki_request(settings: Settings, action: str, **params):
    request_payload = json.dumps({'action': action, 'params': params, 'version': 6}).encode('UTF-8')
    response = requests.request('get', ANKI_HOST, data=request_payload)

    if 200 > response.status_code or response.status_code >= 300:
        raise IOError("Failed to communicate with anki")

    response_json = response.json()

    if response_json['error'] is not None:
        raise IOError(f"Failed to call anki action {action}: {response_json['error']}")

    return response_json


def update_anki_note(settings: Settings, note, query: str, content_info: NoteDetails):
    filename = f'{query}.mp3'

    anki_request(settings, 'addTags', notes=[note['noteId']], tags=' '.join(content_info.tags))

    fields = map_fields(settings.anki.field_mappings, content_info.fields)

    if content_info.pronunciation:
        anki_request(settings, 'storeMediaFile', filename=filename, url=content_info.pronunciation)
        fields[PRONUNCIATION_FIELD] = f'[sound:{filename}]'
    else:
        fields[PRONUNCIATION_FIELD] = ''

    anki_request(settings, 'updateNoteFields', note={
        'id': note['noteId'],
        'fields': fields
    })
