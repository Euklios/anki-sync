import json
from typing import Dict, Any, List, Type

from data.Settings import Settings, ProcessConfigurationObject
from endpoints.abc.BaseEndpoint import BaseEndpoint


def load_settings(known_endpoints: Dict[str, Type[BaseEndpoint]]):
    with open("settings.json") as in_file:
        settings_struct = json.load(in_file)

    return parse_settings(settings_struct, known_endpoints)


def parse_module_settings(module_settings, settings_struct: Dict[str, Any]):
    for key in dir(module_settings):
        if key.startswith("_"):
            continue

        if key in settings_struct:
            setattr(module_settings, key, settings_struct[key])


def parse_endpoint_settings(endpoints, known_endpoints: Dict[str, Type[BaseEndpoint]]):
    endpoint_settings = dict()

    for endpoint_key in endpoints:
        endpoint_config_class = known_endpoints[endpoint_key].config_class()
        endpoint_config = endpoint_config_class()

        parse_module_settings(endpoint_config, endpoints[endpoint_key])

        endpoint_settings[endpoint_key] = endpoint_config

    return endpoint_settings


def parse_config_settings(configurations) -> List[ProcessConfigurationObject]:
    config_objects = list()

    for configuration in configurations:
        config_obj = ProcessConfigurationObject()
        config_obj.source = configuration['source']
        config_obj.target = configuration['target']
        config_obj.enrichment = configuration.get('enrichment', list())

        config_objects.append(config_obj)

    return config_objects


def parse_settings(global_settings: Dict[str, Any], known_endpoints: Dict[str, Type[BaseEndpoint]]):
    settings_obj = Settings()
    settings_obj.endpoints = parse_endpoint_settings(global_settings['endpoints'], known_endpoints)
    settings_obj.config = parse_config_settings(global_settings['config'])

    return settings_obj
