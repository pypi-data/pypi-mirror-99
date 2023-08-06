from datamx.models.values import Groups


def find_first(groups: Groups, model_name: str, value_id: str):
    for group in groups.groups:
        value = group.values.get(value_id)
        if value is not None:
            break
    return value if value is not None else None
