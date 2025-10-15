# final_201_tests.py
import unittest

# IMPORTANT: this module name must match your combined file name exactly.
# If your combined file is named differently (e.g., final_project.py),
# change the import line accordingly.
from final_201_project_1 import (
    avg_flipper_length_gentoo_by_island,
    sex_ratio_by_species_on_dream,
    percent_fem_bill_over_40_by_island,
    percent_male_flip_under_180_by_species,
    calculate_percentage_of_male_penguins_over_threshold,
    calculate_avg_bill_depth_of_male_on_biscoe,
)

# ──────────────────────────────────────────────────────────────
# John A: avg_flipper_length_gentoo_by_island
# ──────────────────────────────────────────────────────────────
class TestJohnFunctionA(unittest.TestCase):
    def test_usual_two_islands(self):
        data = [
            {"species": "Gentoo", "island": "Biscoe", "flipper_length_mm": 210.0},
            {"species": "Gentoo", "island": "Biscoe", "flipper_length_mm": 200.0},
            {"species": "Gentoo", "island": "Dream", "flipper_length_mm": 220.0},
            {"species": "Adelie", "island": "Biscoe", "flipper_length_mm": 999.0},
        ]
        res = avg_flipper_length_gentoo_by_island(data)
        self.assertIn("Biscoe", res)
        self.assertAlmostEqual(res["Biscoe"], 205.0)
        self.assertIn("Dream", res)
        self.assertAlmostEqual(res["Dream"], 220.0)

    def test_usual_missing_non_gentoo(self):
        data = [
            {"species": "Chinstrap", "island": "Dream", "flipper_length_mm": 190.0},
            {"species": "Adelie", "island": "Biscoe", "flipper_length_mm": 184.0},
        ]
        res = avg_flipper_length_gentoo_by_island(data)
        self.assertEqual(res, {})

    def test_edge_missing_values(self):
        data = [
            {"species": "Gentoo", "island": None, "flipper_length_mm": 210.0},
            {"species": "Gentoo", "island": "Biscoe", "flipper_length_mm": None},
            {"species": "Gentoo", "island": "Biscoe", "flipper_length_mm": 200.0},
        ]
        res = avg_flipper_length_gentoo_by_island(data)
        self.assertIn("Biscoe", res)
        self.assertAlmostEqual(res["Biscoe"], 200.0)
        self.assertNotIn("Dream", res)

    def test_edge_case_insensitive_species(self):
        data = [
            {"species": "gEnToO", "island": "Biscoe", "flipper_length_mm": 210.0},
            {"species": "GENTOO", "island": "Biscoe", "flipper_length_mm": 230.0},
        ]
        res = avg_flipper_length_gentoo_by_island(data)
        self.assertAlmostEqual(res["Biscoe"], 220.0)


# ──────────────────────────────────────────────────────────────
# John B: sex_ratio_by_species_on_dream
# ──────────────────────────────────────────────────────────────
class TestJohnFunctionB(unittest.TestCase):
    def test_usual_mixed_counts(self):
        data = [
            {"species": "Adelie", "sex": "male", "island": "Dream"},
            {"species": "Adelie", "sex": "female", "island": "Dream"},
            {"species": "Adelie", "sex": "male", "island": "Dream"},
            {"species": "Gentoo", "sex": "female", "island": "Dream"},
            {"species": "Gentoo", "sex": "female", "island": "Dream"},
            {"species": "Gentoo", "sex": "male", "island": "Biscoe"},
        ]
        res = sex_ratio_by_species_on_dream(data)
        self.assertIn("Adelie", res)
        self.assertAlmostEqual(round(res["Adelie"]["male_%"], 1), 66.7, places=1)
        self.assertAlmostEqual(round(res["Adelie"]["female_%"], 1), 33.3, places=1)
        self.assertIn("Gentoo", res)
        self.assertAlmostEqual(res["Gentoo"]["male_%"], 0.0)
        self.assertAlmostEqual(res["Gentoo"]["female_%"], 100.0)

    def test_usual_case_insensitive_fields(self):
        data = [
            {"species": "adelie", "sex": "MALE", "island": "dream"},
            {"species": "Adelie", "sex": "Female", "island": "Dream"},
        ]
        res = sex_ratio_by_species_on_dream(data)
        self.assertIn("Adelie", res)
        self.assertAlmostEqual(res["Adelie"]["male_%"], 50.0)
        self.assertAlmostEqual(res["Adelie"]["female_%"], 50.0)

    def test_edge_ignore_unknown_or_missing_sex(self):
        data = [
            {"species": "Adelie", "sex": "unknown", "island": "Dream"},
            {"species": "Adelie", "sex": None, "island": "Dream"},
            {"species": "Adelie", "sex": "male", "island": "Dream"},
        ]
        res = sex_ratio_by_species_on_dream(data)
        self.assertAlmostEqual(res["Adelie"]["male_%"], 100.0)
        self.assertAlmostEqual(res["Adelie"]["female_%"], 0.0)

    def test_edge_no_dream_rows(self):
        data = [
            {"species": "Adelie", "sex": "male", "island": "Biscoe"},
            {"species": "Adelie", "sex": "female", "island": "Torgersen"},
        ]
        res = sex_ratio_by_species_on_dream(data)
        self.assertEqual(res, {})


# ──────────────────────────────────────────────────────────────
# Felicia A: percent_fem_bill_over_40_by_island
# ──────────────────────────────────────────────────────────────
class TestFeliciaFunctionA(unittest.TestCase):
    def test_usual_case(self):
        data = [
            {"sex": "female", "bill_length_mm": 42.0, "island": "Biscoe"},
            {"sex": "female", "bill_length_mm": 38.0, "island": "Biscoe"},
            {"sex": "female", "bill_length_mm": 41.0, "island": "Dream"},
            {"sex": "male", "bill_length_mm": 45.0, "island": "Biscoe"},
        ]
        res = percent_fem_bill_over_40_by_island(data)
        self.assertAlmostEqual(res["Biscoe"], 50.0)
        self.assertAlmostEqual(res["Dream"], 100.0)

    def test_edge_missing_values(self):
        data = [
            {"sex": "female", "bill_length_mm": None, "island": "Biscoe"},
            {"sex": "female", "bill_length_mm": "NA", "island": "Biscoe"},
        ]
        res = percent_fem_bill_over_40_by_island(data)
        self.assertNotIn("Biscoe", res)

    def test_case_insensitive_inputs(self):
        data = [
            {"sex": "FEMALE", "bill_length_mm": 45.0, "island": "dream"},
            {"sex": "female", "bill_length_mm": 30.0, "island": "Dream"},
        ]
        res = percent_fem_bill_over_40_by_island(data)
        self.assertIn("Dream", res)
        self.assertAlmostEqual(res["Dream"], 50.0)

    def test_no_females(self):
        data = [{"sex": "male", "bill_length_mm": 60.0, "island": "Biscoe"}]
        res = percent_fem_bill_over_40_by_island(data)
        self.assertEqual(res, {})


# ──────────────────────────────────────────────────────────────
# Felicia B: percent_male_flip_under_180_by_species
# ──────────────────────────────────────────────────────────────
class TestFeliciaFunctionB(unittest.TestCase):
    def test_usual_case(self):
        data = [
            {"sex": "male", "flipper_length_mm": 170.0, "species": "Adelie"},
            {"sex": "male", "flipper_length_mm": 190.0, "species": "Adelie"},
            {"sex": "male", "flipper_length_mm": 175.0, "species": "Gentoo"},
            {"sex": "female", "flipper_length_mm": 150.0, "species": "Adelie"},
        ]
        res = percent_male_flip_under_180_by_species(data)
        self.assertAlmostEqual(res["Adelie"], 50.0)
        self.assertAlmostEqual(res["Gentoo"], 100.0)

    def test_edge_missing_values(self):
        data = [
            {"sex": "male", "flipper_length_mm": None, "species": "Adelie"},
            {"sex": "male", "flipper_length_mm": "NA", "species": "Adelie"},
        ]
        res = percent_male_flip_under_180_by_species(data)
        self.assertNotIn("Adelie", res)

    def test_case_insensitive_inputs(self):
        data = [
            {"sex": "MALE", "flipper_length_mm": 175.0, "species": "adelie"},
            {"sex": "male", "flipper_length_mm": 185.0, "species": "Adelie"},
        ]
        res = percent_male_flip_under_180_by_species(data)
        self.assertIn("Adelie", res)
        self.assertAlmostEqual(res["Adelie"], 50.0)

    def test_no_males(self):
        data = [{"sex": "female", "flipper_length_mm": 160.0, "species": "Adelie"}]
        res = percent_male_flip_under_180_by_species(data)
        self.assertEqual(res, {})


# ──────────────────────────────────────────────────────────────
# Huy A: calculate_percentage_of_male_penguins_over_threshold
# ──────────────────────────────────────────────────────────────
class TestHuyPercentMaleHeavierThanThreshold(unittest.TestCase):
    def test_usual_mixed(self):
        data = [
            {"species": "Adelie", "sex": "male", "body_mass_g": 4600},
            {"species": "Adelie", "sex": "male", "body_mass_g": 4300},
            {"species": "Gentoo", "sex": "male", "body_mass_g": 5700},
            {"species": "Chinstrap", "sex": "male", "body_mass_g": 4400},
            {"species": "Adelie", "sex": "female", "body_mass_g": 9999},
        ]
        res = calculate_percentage_of_male_penguins_over_threshold(data, 4500)
        self.assertAlmostEqual(res["Adelie"], 50.0)
        self.assertAlmostEqual(res["Gentoo"], 100.0)
        self.assertAlmostEqual(res["Chinstrap"], 0.0)

    def test_edge_missing_masses(self):
        data = [
            {"species": "Adelie", "sex": "male", "body_mass_g": None},
            {"species": "Adelie", "sex": "male", "body_mass_g": "NA"},
        ]
        res = calculate_percentage_of_male_penguins_over_threshold(data, 4500)
        self.assertNotIn("Adelie", res)

    def test_case_insensitive_inputs(self):
        data = [
            {"species": "adelie", "sex": "MALE", "body_mass_g": 5000},
            {"species": "Adelie", "sex": "male", "body_mass_g": 4000},
        ]
        res = calculate_percentage_of_male_penguins_over_threshold(data, 4500)
        self.assertIn("Adelie", res)
        self.assertAlmostEqual(res["Adelie"], 50.0)

    def test_zero_denominator_species_omitted(self):
        data = [
            {"species": "Adelie", "sex": "female", "body_mass_g": 10000},
            {"species": "Adelie", "sex": "female", "body_mass_g": 10000},
        ]
        res = calculate_percentage_of_male_penguins_over_threshold(data, 4500)
        self.assertNotIn("Adelie", res)


# ──────────────────────────────────────────────────────────────
# Huy B: calculate_avg_bill_depth_of_male_on_biscoe
# ──────────────────────────────────────────────────────────────
class TestHuyAvgBillDepthMaleBiscoe(unittest.TestCase):
    def test_usual_avg(self):
        data = [
            {"island": "Biscoe", "sex": "male", "bill_depth_mm": 18.0},
            {"island": "Biscoe", "sex": "male", "bill_depth_mm": 16.0},
            {"island": "Biscoe", "sex": "female", "bill_depth_mm": 99.0},
            {"island": "Dream", "sex": "male", "bill_depth_mm": 45.0},
        ]
        res = calculate_avg_bill_depth_of_male_on_biscoe(data)
        self.assertIn("Biscoe", res)
        self.assertAlmostEqual(res["Biscoe"], 17.0)

    def test_edge_no_valid_rows(self):
        data = [
            {"island": "Biscoe", "sex": "male", "bill_depth_mm": None},
            {"island": "Biscoe", "sex": "female", "bill_depth_mm": 20.0},
        ]
        res = calculate_avg_bill_depth_of_male_on_biscoe(data)
        self.assertEqual(res["Biscoe"], 0.0)

    def test_case_insensitive_island_and_sex(self):
        data = [
            {"island": "biscoe", "sex": "MALE", "bill_depth_mm": 20},
            {"island": "BISCOE", "sex": "male", "bill_depth_mm": 22},
        ]
        res = calculate_avg_bill_depth_of_male_on_biscoe(data)
        self.assertIn("Biscoe", res)
        self.assertAlmostEqual(res["Biscoe"], 21.0)

    def test_ignore_non_numeric(self):
        data = [
            {"island": "Biscoe", "sex": "male", "bill_depth_mm": "abc"},
            {"island": "Biscoe", "sex": "male", "bill_depth_mm": 15.0},
        ]
        res = calculate_avg_bill_depth_of_male_on_biscoe(data)
        self.assertAlmostEqual(res["Biscoe"], 15.0)


if __name__ == "__main__":
    unittest.main()