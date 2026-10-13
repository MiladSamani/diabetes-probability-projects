from pathlib import Path

import numpy as np
import pandas as pd


# --------------------------------------------------
# Output directory
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent


# --------------------------------------------------
# 1. Create simulated medical data
# --------------------------------------------------

np.random.seed(42)

n = 200

patients = pd.DataFrame({
    "patient_id": np.arange(1, n + 1),

    "age": np.random.normal(
        55,
        15,
        n
    ).round(),

    "sex": np.random.choice(
        ["Male", "Female", "M", "F", "male", "female"],
        n
    ),

    "systolic_bp": np.random.normal(
        130,
        20,
        n
    ).round(),

    "hba1c": np.random.normal(
        5.8,
        0.8,
        n
    ).round(1),

    "spo2": np.random.normal(
        96,
        3,
        n
    ).round()
})


# --------------------------------------------------
# 2. Add artificial data problems
# --------------------------------------------------

patients.loc[[5, 12, 30], "age"] = [
    150,
    -5,
    999
]

patients.loc[[8, 20, 40], "systolic_bp"] = [
    500,
    20,
    np.nan
]

patients.loc[[10, 25, 60], "hba1c"] = [
    999,
    np.nan,
    18
]

patients.loc[[15, 35], "spo2"] = [
    120,
    -10
]


# Add duplicate records
patients = pd.concat(
    [patients, patients.iloc[[0, 1]]],
    ignore_index=True
)


# Save raw data before cleaning
patients.to_csv(
    BASE_DIR / "raw_patients.csv",
    index=False
)


print("Original shape:", patients.shape)

print("\nOriginal missing percent:")
print(patients.isna().mean() * 100)


# --------------------------------------------------
# 3. Replace special missing codes
# --------------------------------------------------

patients = patients.replace({
    999: np.nan
})


# --------------------------------------------------
# 4. Remove exact duplicate rows
# --------------------------------------------------

before_duplicates = len(patients)

patients = patients.drop_duplicates()

duplicates_removed = before_duplicates - len(patients)

print("\nDuplicates removed:", duplicates_removed)


# --------------------------------------------------
# 5. Clean sex coding
# --------------------------------------------------

sex_map = {
    "male": "Male",
    "m": "Male",
    "female": "Female",
    "f": "Female"
}

patients["sex_clean"] = (
    patients["sex"]
    .str.lower()
    .map(sex_map)
)


# --------------------------------------------------
# 6. Define valid clinical ranges
# --------------------------------------------------

valid_ranges = {
    "age": (0, 120),
    "systolic_bp": (50, 300),
    "hba1c": (3, 20),
    "spo2": (0, 100)
}


# --------------------------------------------------
# 7. Find invalid values
# --------------------------------------------------

for col, (lower, upper) in valid_ranges.items():

    invalid_col = f"{col}_invalid"

    patients[invalid_col] = (
        (patients[col] < lower)
        | (patients[col] > upper)
    )

    patients.loc[
        patients[invalid_col],
        col
    ] = np.nan


# --------------------------------------------------
# 8. Missing indicators and median imputation
# --------------------------------------------------

summary_rows = []

for col in valid_ranges.keys():

    missing_col = f"{col}_missing"
    filled_col = f"{col}_filled"
    invalid_col = f"{col}_invalid"

    patients[missing_col] = (
        patients[col]
        .isna()
        .astype(int)
    )

    median_value = patients[col].median()

    patients[filled_col] = (
        patients[col]
        .fillna(median_value)
    )

    summary_rows.append({
        "Variable": col,
        "Invalid_Count": int(
            patients[invalid_col].sum()
        ),
        "Missing_Count_After_Validation": int(
            patients[col].isna().sum()
        ),
        "Median_Used_For_Imputation": median_value
    })


# --------------------------------------------------
# 9. Cleaning summary
# --------------------------------------------------

cleaning_summary = pd.DataFrame(summary_rows)

cleaning_summary.to_csv(
    BASE_DIR / "cleaning_summary.csv",
    index=False
)


# --------------------------------------------------
# 10. Save cleaned data
# --------------------------------------------------

patients.to_csv(
    BASE_DIR / "cleaned_patients.csv",
    index=False
)


# --------------------------------------------------
# 11. Final results
# --------------------------------------------------

print("\nCleaned shape:", patients.shape)

print("\nMissing percent after cleaning:")
print(patients.isna().mean() * 100)

print("\nInvalid value counts:")

for col in valid_ranges.keys():

    print(
        col,
        patients[f"{col}_invalid"].sum()
    )


print("\nCleaning summary:")
print(cleaning_summary)


print("\nFiles saved:")
print("raw_patients.csv")
print("cleaned_patients.csv")
print("cleaning_summary.csv")