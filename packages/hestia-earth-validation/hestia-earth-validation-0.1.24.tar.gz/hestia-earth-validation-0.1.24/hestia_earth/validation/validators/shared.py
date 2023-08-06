from typing import List
import re

from hestia_earth.validation.geojson import _get_geojson_area
from hestia_earth.validation.gee import _get_region_id
from hestia_earth.validation.utils import _filter_list_errors, _next_error, _same_properties, _value_average
from hestia_earth.validation.utils import _find_linked_node


def validate_dates(node: dict):
    start = node.get('startDate')
    end = node.get('endDate')
    return start is None or end is None or (len(start) <= 7 and len(end) <= 7 and end >= start) or end > start


def validate_list_dates(node: dict, list_key: str):
    def validate(values):
        value = values[1]
        index = values[0]
        return validate_dates(value) or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}].endDate",
            'message': 'must be greater than startDate'
        }

    return _filter_list_errors(list(map(validate, enumerate(node.get(list_key, [])))))


def _compare_min_max(value1, value2): return value1 <= value2


def _compare_list_min_max(list1: list, list2: list):
    def compare_enum(index: int):
        valid = _compare_min_max(list1[index], list2[index])
        return True if valid is True else index

    return len(list1) != len(list2) or \
        next((x for x in list(map(compare_enum, range(len(list1)))) if x is not True), True)


def validate_list_min_max(node: dict, list_key: str):
    def validate(values):
        value = values[1]
        index = values[0]
        min = value.get('min', 0)
        max = value.get('max', 0)
        compare_lists = isinstance(min, list) and isinstance(max, list)
        is_valid = _compare_list_min_max(min, max) if compare_lists else _compare_min_max(min, max)
        return is_valid is True or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}].max",
            'message': 'must be greater than min'
        }

    return _next_error(list(map(validate, enumerate(node.get(list_key, [])))))


def validate_list_duplicates(node: dict, list_key: str, props: List[str]):
    def validate(values):
        value = values[1]
        index = values[0]
        values = node[list_key].copy()
        values.pop(index)
        duplicates = list(filter(_same_properties(value, props), values))
        return len(duplicates) == 0 or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}]",
            'message': f"Duplicates found. Please make sure there is only one entry with the same {', '.join(props)}"
        }

    return _next_error(list(map(validate, enumerate(node.get(list_key, [])))))


def validate_list_term_percent(node: dict, list_key: str):
    def soft_validate(index: int, value): return 0 <= value and value <= 1 and {
            'level': 'warning',
            'dataPath': f".{list_key}[{index}].value",
            'message': 'may be between 0 and 100'
        }

    def hard_validate(index: int, value): return (0 <= value and value <= 100) or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}].value",
            'message': 'should be between 0 and 100 (percentage)'
        }

    def validate(values):
        index = values[0]
        value = values[1]
        units = value.get('term', {}).get('units', '')
        value = _value_average(value, None)
        return units != '% (0-100)' or value is None or type(value) == str or \
            soft_validate(index, value) or hard_validate(index, value)

    return _filter_list_errors(list(map(validate, enumerate(node.get(list_key, [])))))


def validate_region(node: dict, region_key='region'):
    country = node.get('country', {})
    region_id = node.get(region_key, {}).get('@id', '')
    return region_id[0:8] == country.get('@id') or {
        'level': 'error',
        'dataPath': f".{region_key}",
        'message': 'must be within the country',
        'params': {
            'country': country.get('name')
        }
    }


def validate_country(node: dict):
    country_id = node.get('country', {}).get('@id', '')
    # handle additional regions used as country, like region-world
    is_region = country_id.startswith('region-')
    return is_region or bool(re.search(r'GADM-[A-Z]{3}', country_id)) or {
        'level': 'error',
        'dataPath': '.country',
        'message': 'must be a country'
    }


def need_validate_coordinates(node: dict): return 'latitude' in node and 'longitude' in node


def validate_coordinates(node: dict, region_key='region'):
    latitude = node.get('latitude')
    longitude = node.get('longitude')
    country = node.get('country', {})
    region = node.get(region_key)
    gadm_id = region.get('@id') if region else country.get('@id')
    id = _get_region_id(gadm_id, latitude=latitude, longitude=longitude)
    return gadm_id == id or {
        'level': 'error',
        'dataPath': f".{region_key}" if region else '.country',
        'message': 'does not contain latitude and longitude',
        'params': {
            'gadmId': id
        }
    }


def need_validate_area(node: dict): return 'area' in node and 'boundary' in node


def validate_area(node: dict):
    try:
        area = _get_geojson_area(node.get('boundary'))
        return area == round(node.get('area'), 1) or {
            'level': 'error',
            'dataPath': '.area',
            'message': f"must be equal to boundary (~{area})"
        }
    except KeyError:
        # if getting the geojson fails, the geojson format is invalid
        # and the schema validation step will detect it
        return True


N_A_VALUES = [
    '#n/a',
    '#na',
    'n/a',
    'na',
    'n.a',
    'nodata',
    'no data'
]


def validate_empty_fields(node: dict):
    keys = list(filter(lambda key: isinstance(node.get(key), str), node.keys()))

    def validate(key: str):
        return not node.get(key).lower() in N_A_VALUES or {
            'level': 'warning',
            'dataPath': f".{key}",
            'message': 'may not be empty'
        }

    return _filter_list_errors(list(map(validate, keys)), False)


def validate_linked_source_privacy(node: dict, key: str, nodes: list):
    related_source = _find_linked_node(nodes, node.get(key, {}))
    node_privacy = node.get('dataPrivate')
    related_source_privacy = related_source.get('dataPrivate') if related_source else None
    return related_source_privacy is None or node_privacy == related_source_privacy or {
        'level': 'error',
        'dataPath': '.dataPrivate',
        'message': 'should have the same privacy as the related source',
        'params': {
            'dataPrivate': node_privacy,
            key: {
                'dataPrivate': related_source_privacy
            }
        }
    }
