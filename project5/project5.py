import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import norm


# -----------------------------
# Load Dataset
# -----------------------------

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


# -----------------------------
# Step 1: Glucose Parameters
# -----------------------------

glucose_mean = df["Glucose"].mean()
glucose_std = df["Glucose"].std()

print("Glucose Mean:", glucose_mean)
print("Glucose Standard Deviation:", glucose_std)


# -----------------------------
# Step 2: CDF
# -----------------------------

# P(Glucose <= 140)
p_less_equal_140 = norm.cdf(
    140,
    loc=glucose_mean,
    scale=glucose_std
)

# P(Glucose > 140)
p_above_140 = 1 - p_less_equal_140

# P(100 <= Glucose <= 140)
p_100_to_140 = (
    norm.cdf(
        140,
        loc=glucose_mean,
        scale=glucose_std
    )
    -
    norm.cdf(
        100,
        loc=glucose_mean,
        scale=glucose_std
    )
)

print("P(Glucose <= 140):", p_less_equal_140)
print("P(Glucose > 140):", p_above_140)
print("P(100 <= Glucose <= 140):", p_100_to_140)


# -----------------------------
# Step 3: Percentiles
# -----------------------------

percentiles = [0.50, 0.75, 0.90, 0.95, 0.99]

for p in percentiles:

    value = norm.ppf(
        p,
        loc=glucose_mean,
        scale=glucose_std
    )

    print(f"{int(p * 100)}th Percentile:", value)


# -----------------------------
# Step 4: Z-score for Glucose=180
# -----------------------------

patient_glucose = 180

z_score = (
    patient_glucose - glucose_mean
) / glucose_std

patient_percentile = norm.cdf(z_score)

print("Z-score for Glucose=180:", z_score)

print(
    "Percentile for Glucose=180:",
    patient_percentile
)

print(
    "Percentile Percentage:",
    patient_percentile * 100
)


# -----------------------------
# Step 5: CDF Plot
# -----------------------------

x = np.linspace(
    df["Glucose"].min(),
    df["Glucose"].max(),
    500
)

cdf = norm.cdf(
    x,
    loc=glucose_mean,
    scale=glucose_std
)

plt.plot(x, cdf)

# Threshold = 140
plt.axvline(
    x=140,
    linestyle="--"
)

# Patient = 180
plt.axvline(
    x=180,
    linestyle="--"
)

plt.title("Glucose CDF")
plt.xlabel("Glucose")
plt.ylabel("CDF")

plt.savefig("glucose_cdf.png")
plt.close()

print("CDF plot saved as glucose_cdf.png")