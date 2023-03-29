from typing import Dict, List


class ProcessConfigurationObject:
    source: str = None
    target: str = None
    enrichment: List[str] = list()


class Settings:
    endpoints: Dict[str, Dict]
    config: List[ProcessConfigurationObject]
