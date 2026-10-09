import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# -----------------------------------
# Load Dataset
# -----------------------------------

url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"

columns = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
    "Outcome"
]

df = pd.read_csv(url, names=columns)


# -----------------------------------
# Variables used in Project 6
# -----------------------------------

variables = [
    "Glucose",
    "BMI",
    "Age",
    "BloodPressure",
    "Insulin",
    "SkinThickness"
]


# -----------------------------------
# Step 1: Descriptive Statistics
# -----------------------------------

descriptive_rows = []

for variable in variables:

    data = df[variable]

    mean = data.mean()
    median = data.median()
    mode = data.mode().iloc[0]

    std = data.std()

    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)

    iqr = q3 - q1

    minimum = data.min()
    maximum = data.max()

    descriptive_rows.append({
        "Variable": variable,
        "Mean": mean,
        "Median": median,
        "Mode": mode,
        "SD": std,
        "Q1": q1,
        "Q3": q3,
        "IQR": iqr,
        "Min": minimum,
        "Max": maximum
    })


descriptive_table = pd.DataFrame(descriptive_rows)

print("\n--- Descriptive Statistics ---")
print(descriptive_table)

descriptive_table.to_csv(
    "descriptive_summary.csv",
    index=False
)


# -----------------------------------
# Step 2: Detect Outliers with IQR
# -----------------------------------

outlier_rows = []

for variable in variables:

    data = df[variable]

    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = data[
        (data < lower_bound) |
        (data > upper_bound)
    ]

    outlier_rows.append({
        "Variable": variable,
        "Q1": q1,
        "Q3": q3,
        "IQR": iqr,
        "Lower Bound": lower_bound,
        "Upper Bound": upper_bound,
        "Outlier Count": len(outliers)
    })


outlier_table = pd.DataFrame(outlier_rows)

print("\n--- Outlier Analysis ---")
print(outlier_table)

outlier_table.to_csv(
    "outlier_summary.csv",
    index=False
)


# -----------------------------------
# Step 3: Skewness
# -----------------------------------

skew_rows = []

for variable in variables:

    data = df[variable]

    skewness = data.skew()
    mean = data.mean()
    median = data.median()

    if skewness > 0:
        direction = "Positive"
    elif skewness < 0:
        direction = "Negative"
    else:
        direction = "Symmetric"

    skew_rows.append({
        "Variable": variable,
        "Mean": mean,
        "Median": median,
        "Skewness": skewness,
        "Direction": direction
    })


skew_table = pd.DataFrame(skew_rows)

print("\n--- Skewness Analysis ---")
print(skew_table)

skew_table.to_csv(
    "skewness_summary.csv",
    index=False
)


# -----------------------------------
# Step 4: Histograms
# -----------------------------------

for variable in variables:

    plt.hist(
        df[variable],
        bins=20
    )

    plt.title(f"{variable} Distribution")
    plt.xlabel(variable)
    plt.ylabel("Frequency")

    plt.savefig(
        f"{variable.lower()}_histogram.png"
    )

    plt.close()


# -----------------------------------
# Step 4: Boxplots
# -----------------------------------

boxplot_variables = [
    "Glucose",
    "BMI",
    "Age"
]

for variable in boxplot_variables:

    plt.boxplot(
        df[variable],
        vert=True
    )

    plt.title(f"{variable} Boxplot")
    plt.ylabel(variable)

    plt.savefig(
        f"{variable.lower()}_boxplot.png"
    )

    plt.close()


# -----------------------------------
# Step 5: Clinical Report
# -----------------------------------

clinical_rows = []

for variable in variables:

    data = df[variable]

    mean = data.mean()
    median = data.median()
    std = data.std()

    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)

    iqr = q3 - q1
    skewness = data.skew()

    # Simple educational rule:
    # low skew -> Mean + SD
    # noticeable skew -> Median + IQR
    #
    # The project brief does not define
    # an exact threshold for this decision.

    if abs(skewness) < 0.5:
        recommendation = "Mean + SD"
    else:
        recommendation = "Median + IQR"

    clinical_rows.append({
        "Variable": variable,
        "Mean": mean,
        "Median": median,
        "SD": std,
        "IQR": iqr,
        "Skewness": skewness,
        "Recommended Measure": recommendation
    })


clinical_report = pd.DataFrame(clinical_rows)

print("\n--- Clinical Report ---")
print(clinical_report)

clinical_report.to_csv(
    "clinical_report.csv",
    index=False
)


# -----------------------------------
# Final Message
# -----------------------------------

print("\nProject 6 completed.")
print("CSV tables and plots were saved.")