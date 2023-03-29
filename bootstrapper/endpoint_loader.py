import importlib
import inspect
import os
from typing import List, Type, Dict

from data.Settings import Settings
from endpoints.abc.BaseEndpoint import BaseEndpoint


def load_known_endpoints() -> List[Type]:
    package = "endpoints"
    project_root = os.path.dirname(os.path.dirname(__file__))
    endpoints_package = os.path.join(project_root, package)

    collected_providers = list()

    for file_name in os.listdir(endpoints_package):
        file = os.path.join(endpoints_package, file_name)

        if not os.path.isfile(file):
            continue

        module = importlib.import_module(f"{package}.{file_name.replace('.py', '')}")
        for pair in inspect.getmembers(module):
            obj = pair[1]

            if inspect.isclass(obj) and issubclass(obj, BaseEndpoint) and not inspect.isabstract(obj):
                collected_providers.append(obj)

    return collected_providers


def instantiate_endpoints(endpoints: Dict[str, Type], settings: Settings) -> Dict[str, BaseEndpoint]:
    endpoint_instances = dict()

    for endpoint_key in settings.endpoints:
        endpoint_class = endpoints[endpoint_key]
        endpoint_settings = settings.endpoints[endpoint_key]

        endpoint_instances[endpoint_key] = endpoint_class(endpoint_settings)

    return endpoint_instances
