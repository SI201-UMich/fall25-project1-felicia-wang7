# Name: Felicia Wang
# ID: 62645970
# Email: wangfeli@umich.edu
# Collaborators: Huy Pham, John (Yohan) Park

import unittest

from felicia_project import (
    percent_fem_bill_over_40_by_island,
    percent_male_flip_under_180_by_species,
)

class TestFeliciaFunctionA(unittest.TestCase):
    """Tests for percent_fem_bill_over_40_by_island"""

    def test_usual_mixed_counts(self):
        data = [
            {"sex":"FEMALE","bill_length_mm":41.0,"island":"Biscoe"},
            {"sex":"FEMALE","bill_length_mm":39.0,"island":"Biscoe"},
            {"sex":"FEMALE","bill_length_mm":42.0,"island":"Dream"},
            {"sex":"FEMALE","bill_length_mm":38.0,"island":"Dream"},
        ]
        res = percent_fem_bill_over_40_by_island(data)
        self.assertAlmostEqual(res["Biscoe"], 50.0)
        self.assertAlmostEqual(res["Dream"], 50.0)

    def test_boundary_equals_40_not_included(self):
        data = [
            {"sex":"FEMALE","bill_length_mm":40.0,"island":"Torgersen"},
            {"sex":"FEMALE","bill_length_mm":41.0,"island":"Torgersen"},
            {"sex":"FEMALE","bill_length_mm":39.0,"island":"Torgersen"},
        ]
        res = percent_fem_bill_over_40_by_island(data)
        self.assertAlmostEqual(res["Torgersen"], (1/3)*100)

    def test_missing_numeric_skipped(self):
        data = [
            {"sex":"FEMALE","bill_length_mm":None,"island":"Biscoe"},
            {"sex":"FEMALE","bill_length_mm":41.0,"island":"Biscoe"},
            {"sex":"FEMALE","bill_length_mm":39.0,"island":"Biscoe"},
        ]
        res = percent_fem_bill_over_40_by_island(data)
        self.assertAlmostEqual(res["Biscoe"], 50.0)

    def test_no_valid_female_measurements_group_absent(self):
        data = [
            {"sex":"FEMALE","bill_length_mm":None,"island":"Dream"},
            {"sex":"MALE","bill_length_mm":50.0,"island":"Dream"},
        ]
        res = percent_fem_bill_over_40_by_island(data)
        self.assertNotIn("Dream", res)