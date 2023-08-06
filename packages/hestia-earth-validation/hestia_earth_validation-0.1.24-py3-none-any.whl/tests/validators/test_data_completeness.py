import unittest
import json

from hestia_earth.schema import SiteSiteType

from tests.utils import fixtures_path
from hestia_earth.validation.validators.data_completeness import validate_dataCompleteness, _validate_all_values, \
    _validate_site_type


class TestValidatorsDataCompleteness(unittest.TestCase):
    def test_validate_dataCompleteness_valid(self):
        with open(f"{fixtures_path}/dataCompleteness/valid.json") as f:
            data = json.load(f)
        self.assertEqual(validate_dataCompleteness(data), [True] * 2)

    def test_validate_all_values_valid(self):
        with open(f"{fixtures_path}/dataCompleteness/valid.json") as f:
            data = json.load(f)
        self.assertEqual(_validate_all_values(data), True)

    def test_validate_all_values_warning(self):
        with open(f"{fixtures_path}/dataCompleteness/all-values/warning.json") as f:
            data = json.load(f)
        self.assertEqual(_validate_all_values(data), {
            'level': 'warning',
            'dataPath': '.dataCompleteness',
            'message': 'may not all be set to false'
        })

    def test_validate_site_type_valid(self):
        with open(f"{fixtures_path}/dataCompleteness/site-type/site.json") as f:
            site = json.load(f)
        with open(f"{fixtures_path}/dataCompleteness/site-type/valid.json") as f:
            data = json.load(f)
        self.assertEqual(_validate_site_type(data, site), True)

        # also works if siteType is not cropland
        site['siteType'] = SiteSiteType.POND.value
        data['manureManagement'] = False
        self.assertEqual(_validate_site_type(data, site), True)

    def test_validate_site_type_warning(self):
        with open(f"{fixtures_path}/dataCompleteness/site-type/site.json") as f:
            site = json.load(f)
        with open(f"{fixtures_path}/dataCompleteness/site-type/warning.json") as f:
            data = json.load(f)
        self.assertEqual(_validate_site_type(data, site), {
            'level': 'warning',
            'dataPath': '.dataCompleteness.manureManagement',
            'message': 'should be true for site of type cropland'
        })
