from datetime import datetime


REQUIRED_FIELDS = (
    "measurement_id",
    "site_id",
    "recorded_at_utc",
    "metric",
    "value",
    "unit",
    "data_source",
)

METRIC_RULES = {
    "temperature": {
        "minimum": -60.0,
        "maximum": 60.0,
        "unit": "celsius",
    },
    "energy_consumption": {
        "minimum": 0.0,
        "maximum": 1000000.0,
        "unit": "kWh",
    },
    "water_consumption": {
        "minimum": 0.0,
        "maximum": 1000000.0,
        "unit": "litres",
    },
}

ALLOWED_DATA_SOURCES = {
    "SIMULATED",
    "MEASURED",
    "ESTIMATED",
}


def validate_timestamp(timestamp_value):
    """Check whether a timestamp is valid ISO 8601 data."""

    if not timestamp_value:
        return False

    try:
        parsed_timestamp = datetime.fromisoformat(
            timestamp_value
        )
    except ValueError:
        return False

    return parsed_timestamp.tzinfo is not None


def validate_measurement(record):
    """Validate one environmental measurement."""

    errors = []

    for field in REQUIRED_FIELDS:
        value = record.get(field)

        if value is None or str(value).strip() == "":
            errors.append(
                f"{field} is required."
            )

    metric = record.get("metric", "").strip()
    unit = record.get("unit", "").strip()
    value_text = record.get("value", "").strip()
    data_source = record.get(
        "data_source",
        "",
    ).strip()

    if metric and metric not in METRIC_RULES:
        errors.append(
            f"Unsupported metric: {metric}."
        )

    if metric in METRIC_RULES:
        expected_unit = METRIC_RULES[metric]["unit"]

        if unit and unit != expected_unit:
            errors.append(
                f"{metric} must use the unit "
                f"{expected_unit}."
            )

    if value_text:
        try:
            numeric_value = float(value_text)
        except ValueError:
            errors.append(
                "value must be numeric."
            )
        else:
            if metric in METRIC_RULES:
                minimum = METRIC_RULES[metric][
                    "minimum"
                ]
                maximum = METRIC_RULES[metric][
                    "maximum"
                ]

                if not minimum <= numeric_value <= maximum:
                    errors.append(
                        f"value for {metric} must be "
                        f"between {minimum} and {maximum}."
                    )

    timestamp_value = record.get(
        "recorded_at_utc",
        "",
    ).strip()

    if timestamp_value and not validate_timestamp(
        timestamp_value
    ):
        errors.append(
            "recorded_at_utc must be a valid "
            "timezone-aware ISO 8601 timestamp."
        )

    if (
        data_source
        and data_source not in ALLOWED_DATA_SOURCES
    ):
        errors.append(
            "data_source must be SIMULATED, "
            "MEASURED or ESTIMATED."
        )

    return errors


def validate_measurements(records):
    """Validate a batch and detect duplicate IDs."""

    validation_results = []
    seen_measurement_ids = set()

    for record in records:
        errors = validate_measurement(record)

        measurement_id = record.get(
            "measurement_id",
            "",
        ).strip()

        if measurement_id in seen_measurement_ids:
            errors.append(
                f"Duplicate measurement_id: "
                f"{measurement_id}."
            )

        if measurement_id:
            seen_measurement_ids.add(
                measurement_id
            )

        validation_results.append(
            {
                "record": record,
                "is_valid": len(errors) == 0,
                "errors": errors,
            }
        )

    return validation_results