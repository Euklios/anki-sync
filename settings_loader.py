import json
from typing import Dict, Any

from data.Settings import Settings


def load_settings():
    with open("settings.json") as in_file:
        settings_struct = json.load(in_file)

    return parse_settings(settings_struct)


def parse_module_settings(module_settings, settings_struct: Dict[str, Any]):
    for key in dir(module_settings):
        if key.startswith("_"):
            continue

        if key in settings_struct:
            setattr(module_settings, key, settings_struct[key])


def parse_settings(settings: Dict[str, Any]):
    settings_obj = Settings()

    for key in dir(settings_obj):
        if key.startswith("_"):
            continue

        if key not in settings:
            setattr(settings_obj, key, None)
        else:
            parse_module_settings(getattr(settings_obj, key), settings[key])

    return settings_obj
