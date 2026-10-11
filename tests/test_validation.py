import unittest

from src.validation.environmental_data import (
    validate_measurement,
    validate_measurements,
)


class TestEnvironmentalValidation(
    unittest.TestCase
):
    def setUp(self):
        self.valid_record = {
            "measurement_id": "TEST-001",
            "site_id": "BER-001",
            "recorded_at_utc": (
                "2026-10-11T06:00:00+00:00"
            ),
            "metric": "temperature",
            "value": "18.5",
            "unit": "celsius",
            "data_source": "SIMULATED",
        }

    def test_valid_record_has_no_errors(self):
        errors = validate_measurement(
            self.valid_record
        )

        self.assertEqual(errors, [])

    def test_negative_energy_is_rejected(self):
        record = self.valid_record.copy()
        record["metric"] = "energy_consumption"
        record["value"] = "-10"
        record["unit"] = "kWh"

        errors = validate_measurement(record)

        self.assertTrue(errors)

    def test_missing_timestamp_is_rejected(self):
        record = self.valid_record.copy()
        record["recorded_at_utc"] = ""

        errors = validate_measurement(record)

        self.assertIn(
            "recorded_at_utc is required.",
            errors,
        )

    def test_duplicate_id_is_detected(self):
        first_record = self.valid_record.copy()
        second_record = self.valid_record.copy()

        results = validate_measurements(
            [first_record, second_record]
        )

        self.assertTrue(
            results[0]["is_valid"]
        )

        self.assertFalse(
            results[1]["is_valid"]
        )

        self.assertIn(
            "Duplicate measurement_id: TEST-001.",
            results[1]["errors"],
        )


if __name__ == "__main__":
    unittest.main()