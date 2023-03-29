from typing import List

from bootstrapper.endpoint_loader import load_known_endpoints, instantiate_endpoints
from bootstrapper.enrichment_step import Step
from endpoints.abc.BaseProvider import BaseProvider
from endpoints.abc.NoteConsumer import BaseNoteConsumer
from endpoints.abc.NoteProvider import BaseNoteProvider
from bootstrapper.settings_loader import load_settings


def initialize_enrichment_steps() -> List[Step]:
    known_endpoints = load_known_endpoints()
    endpoint_lookup_map = {endpoint.endpoint_name(): endpoint for endpoint in known_endpoints}
    settings = load_settings(endpoint_lookup_map)
    endpoint_instances = instantiate_endpoints(endpoint_lookup_map, settings)
    steps = list()

    for entry in settings.config:
        source = endpoint_instances[entry.source]
        target = endpoint_instances[entry.target]
        enrichment_steps: List[BaseProvider] = list()

        if not isinstance(source, BaseNoteProvider):
            raise f"source {source.endpoint_name()} should be an instance of BaseNoteProvider"

        if not isinstance(target, BaseNoteConsumer):
            raise f"target {target.endpoint_name()} should be an instance of BaseNoteConsumer"

        for step in entry.enrichment:
            step_instance = endpoint_instances[step]
            if not isinstance(step_instance, BaseProvider):
                raise f"step {step_instance.endpoint_name()} should be an instance of BaseProvider"

            enrichment_steps.append(step_instance)

        steps.append(Step(source, target, enrichment_steps))

    return steps
