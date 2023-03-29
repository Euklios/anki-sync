def map_fields(field_mappings, data):
    return {field_mappings.get(k, k): v for k, v in data.items()}
