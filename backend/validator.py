import pandas as pd
import numpy as np


def to_python_type(value):
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    return value


def make_json_safe(obj):
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    else:
        return obj


# Read csv file
def load_csv(filename):
    filename.seek(0)
    df = pd.read_csv(filename, encoding="utf-8-sig")
    return df



# Calculates the number of missing (null) values in each column
# Used to identify incomplete data that may affect analysis or ML models
def check_missing_values(df):
    return df.isnull().sum().to_dict()


# Detects the inferred data type of each column
# Helps identify incorrect or inconsistent column types
def check_data_types(df):
    return df.dtypes.astype(str).to_dict()


# Counts the number of duplicate rows in the dataset
# Duplicate records can skew aggregations and analytics
def check_duplicates(df):
    return int(df.duplicated().sum())


# Detects outliers in numeric columns using Z-score method
# An outlier is a value that is more than 3 standard deviations
# away from the column mean, indicating a potential anomaly
def detect_outliers(df):
    outliers = {}
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    for col in numeric_cols:
        mean = df[col].mean()
        std = df[col].std()

        # If standard deviation is zero, all values are identical
        if std == 0:
            outliers[col] = 0
            continue

        # Z-score calculation
        z_scores = ((df[col] - mean) / std).abs()

        # Count values that exceed the threshold
        outliers[col] = int((z_scores > 3).sum())

    return outliers


# Generates column-level statistics to understand data distribution
# Includes data type, missing percentage, uniqueness, and basic stats
def data_profiling(df):
    profile = {}

    for col in df.columns:
        col_data = df[col]

        profile[col] = {
            "data_type": str(col_data.dtype),
            "missing_percentage": round(col_data.isnull().mean() * 100, 2),
            "unique_values": to_python_type(col_data.nunique())
        }

        # Additional statistics for numeric columns
        if col_data.dtype in ["int64", "float64"]:
            profile[col].update({
                "min": col_data.min(),
                "max": col_data.max(),
                "mean": round(col_data.mean(), 2),
                "median": col_data.median()
            })

    return profile


def generate_suggestions(report):
    suggestions = []

    if any(v > 0 for v in report["missing_values"].values()):
        suggestions.append("Handle missing values using mean/median or drop rows.")

    if report["duplicate_rows"] > 0:
        suggestions.append("Remove duplicate rows to improve data quality.")

    if any(v > 0 for v in report["outliers"].values()):
        suggestions.append("Review outliers; consider capping or removal.")

    return suggestions


EXPECTED_SCHEMA = {
    "id": "int64",
    "age": "int64",
    "salary": "float64"
}

# Validates the dataset against an expected schema (if provided)
# Ensures required columns exist and data types match expectations
def validate_schema(df, expected_schema=None):
    if not expected_schema:
        return ["Schema validation skipped"]
    issues = []

    for col, expected_type in EXPECTED_SCHEMA.items():
        if col not in df.columns:
            issues.append(f"Missing column: {col}")
        elif str(df[col].dtype) != expected_type:
            issues.append(
                f"Column '{col}' expected {expected_type} but got {df[col].dtype}"
            )

    return issues


# Calculates an overall data quality score based on detected issues
# The score decreases as missing values, duplicates, and outliers increase
def calculate_quality_score(report):
    score = 100
    score -= sum(report["missing_values"].values())
    score -= report["duplicate_rows"] * 2
    score -= sum(report["outliers"].values())
    return int(max(score, 0))


# Cleans the dataset by removing duplicates and filling missing numeric values
# Median is used to reduce the impact of outliers
def clean_data(df):
    df = df.drop_duplicates()

    for col in df.select_dtypes(include=["int64", "float64"]):
        df[col] = df[col].fillna(df[col].median())

    return df


# Combine everything
def validate_csv(filename):
    df = load_csv(filename)

    report = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": check_missing_values(df),
        "data_types": check_data_types(df),
        "duplicate_rows": check_duplicates(df),
        "outliers": detect_outliers(df),
        "profiling": data_profiling(df),
        "schema_issues": validate_schema(df)
    }

    report["quality_score"] = calculate_quality_score(report)
    report["suggestions"] = generate_suggestions(report)

    return make_json_safe(report)
