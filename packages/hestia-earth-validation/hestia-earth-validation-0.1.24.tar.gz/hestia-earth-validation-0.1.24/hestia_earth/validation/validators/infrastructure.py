from hestia_earth.utils.date import diff_in_years

from hestia_earth.validation.utils import _filter_list_errors, _list_has_props


def validate_lifespan(infrastructure: list):
    def validate(values):
        value = values[1]
        index = values[0]
        lifespan = diff_in_years(value.get('startDate'), value.get('endDate'))
        return lifespan == round(value.get('lifespan'), 1) or {
            'level': 'error',
            'dataPath': f".infrastructure[{index}].lifespan",
            'message': f"must equal to endDate - startDate in decimal years (~{lifespan})"
        }

    results = list(map(validate, enumerate(_list_has_props(infrastructure, ['lifespan', 'startDate', 'endDate']))))
    return _filter_list_errors(results)
