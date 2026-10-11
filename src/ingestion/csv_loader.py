import csv
from pathlib import Path


def load_environmental_measurements(file_path):
    """Read environmental measurements from a CSV file."""

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Environmental data file not found: {file_path}"
        )

    records = []

    with file_path.open(
        mode="r",
        encoding="utf-8",
        newline="",
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            records.append(dict(row))

    return records