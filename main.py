from pathlib import Path

from src.ingestion.csv_loader import (
    load_environmental_measurements,
)
from src.validation.environmental_data import (
    validate_measurements,
)


BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "environmental_measurements.csv"
)


def main():
    """Run the EcoData Reliability Hub pipeline."""

    records = load_environmental_measurements(
        DATA_FILE
    )

    validation_results = validate_measurements(
        records
    )

    valid_count = 0
    invalid_count = 0

    print("\n=== ECODATA RELIABILITY HUB ===")
    print("Pipeline stage: INGESTION AND VALIDATION")
    print("Data classification: SIMULATED")
    print(f"Records loaded: {len(records)}")

    for result in validation_results:
        record = result["record"]

        print("\n" + "-" * 50)
        print(
            f"Measurement ID: "
            f"{record['measurement_id']}"
        )
        print(f"Site: {record['site_id']}")
        print(f"Metric: {record['metric']}")
        print(f"Value: {record['value']}")
        print(f"Unit: {record['unit']}")

        if result["is_valid"]:
            valid_count += 1
            print("Validation: VALID")
        else:
            invalid_count += 1
            print("Validation: INVALID")
            print("Problems detected:")

            for error in result["errors"]:
                print(f"- {error}")

    print("\n=== VALIDATION SUMMARY ===")
    print(f"Total records: {len(records)}")
    print(f"Valid records: {valid_count}")
    print(f"Invalid records: {invalid_count}")


if __name__ == "__main__":
    main()