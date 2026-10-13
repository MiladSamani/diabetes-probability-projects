from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# Output directory
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent


# --------------------------------------------------
# 1. Create simulated medical data
# --------------------------------------------------

np.random.seed(42)

n = 300

age = np.random.normal(
    loc=55,
    scale=12,
    size=n
).round()

systolic_bp = np.random.normal(
    loc=128,
    scale=18,
    size=n
)

length_of_stay = np.random.exponential(
    scale=4,
    size=n
).round()


# Add a few extreme values
length_of_stay[:5] = [20, 25, 30, 35, 45]


patients = pd.DataFrame({
    "age": age,
    "systolic_bp": systolic_bp,
    "length_of_stay": length_of_stay
})


# --------------------------------------------------
# 2. Basic descriptive statistics
# --------------------------------------------------

print("\nDescriptive statistics:")
print(patients.describe())


# --------------------------------------------------
# 3. IQR, outliers and skewness
# --------------------------------------------------

summary_rows = []

for col in patients.columns:

    q1 = patients[col].quantile(0.25)
    q3 = patients[col].quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = patients[
        (patients[col] < lower)
        | (patients[col] > upper)
    ][col]

    mean = patients[col].mean()
    median = patients[col].median()
    std = patients[col].std()
    skewness = patients[col].skew()

    summary_rows.append({
        "Variable": col,
        "Mean": mean,
        "Median": median,
        "SD": std,
        "IQR": iqr,
        "Skewness": skewness,
        "Lower_Fence": lower,
        "Upper_Fence": upper,
        "Outliers": len(outliers)
    })

    print("\nVariable:", col)
    print("Mean:", mean)
    print("Median:", median)
    print("SD:", std)
    print("IQR:", iqr)
    print("Skewness:", skewness)
    print("Lower fence:", lower)
    print("Upper fence:", upper)
    print("Number of outliers:", len(outliers))


summary = pd.DataFrame(summary_rows)

summary.to_csv(
    BASE_DIR / "summary7.csv",
    index=False
)


# --------------------------------------------------
# 4. Histograms and boxplots
# --------------------------------------------------

plt.figure(figsize=(12, 8))

for i, col in enumerate(patients.columns, start=1):

    plt.subplot(3, 2, 2 * i - 1)

    plt.hist(
        patients[col],
        bins=25,
        edgecolor="black"
    )

    plt.title(f"Histogram of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")


    plt.subplot(3, 2, 2 * i)

    plt.boxplot(
        patients[col],
        vert=True
    )

    plt.title(f"Boxplot of {col}")
    plt.ylabel(col)


plt.tight_layout()

plt.savefig(
    BASE_DIR / "project7_distributions.png",
    dpi=150
)

plt.close()


print("\nFiles saved:")
print("summary7.csv")
print("project7_distributions.png")