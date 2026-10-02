import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

print(df.head())

df["Test_Positive"] = (df["Glucose"] >= 140).astype(int)
print(df[["Glucose", "Outcome", "Test_Positive"]].head(10))

tp = ((df["Outcome"] == 1) & (df["Test_Positive"] == 1)).sum()

fp = ((df["Outcome"] == 0) & (df["Test_Positive"] == 1)).sum()

tn = ((df["Outcome"] == 0) & (df["Test_Positive"] == 0)).sum()

fn = ((df["Outcome"] == 1) & (df["Test_Positive"] == 0)).sum()

print("TP:", tp)
print("FP:", fp)
print("TN:", tn)
print("FN:", fn)

sensitivity = tp / (tp + fn)
specificity = tn / (tn + fp)
fpr = 1 - specificity

print("Sensitivity:", sensitivity)
print("Specificity:", specificity)
print("False Positive Rate:", fpr)

print("Sensitivity (%):", sensitivity * 100)
print("Specificity (%):", specificity * 100)
print("False Positive Rate (%):", fpr * 100)

prevalence = (df["Outcome"] == 1).mean()

print("Prevalence:", prevalence)
print("Prevalence (%):", prevalence * 100)

ppv = tp / (tp + fp)

print("PPV:", ppv)
print("PPV (%):", ppv * 100)

npv = tn / (tn + fn)

print("NPV:", npv)
print("NPV (%):", npv * 100)

p_test_positive = (
    sensitivity * prevalence
    + fpr * (1 - prevalence)
)

print("P(Test Positive):", p_test_positive)
print("P(Test Positive %):", p_test_positive * 100)

ppv_bayes = (
    sensitivity * prevalence
    / p_test_positive
)

print("PPV with Bayes:", ppv_bayes)
print("PPV with Bayes (%):", ppv_bayes * 100)


p_test_negative = (
    specificity * (1 - prevalence)
    + (1 - sensitivity) * prevalence
)

print("P(Test Negative):", p_test_negative)
print("P(Test Negative %):", p_test_negative * 100)

npv_bayes = (
    specificity * (1 - prevalence)
    / p_test_negative
)

print("NPV with Bayes:", npv_bayes)
print("NPV with Bayes (%):", npv_bayes * 100)


prevalences = np.arange(0.01, 0.61, 0.01)

print("Prevalences:")
print(prevalences)


ppv_values = []

for p in prevalences:
    p_test_positive = (
        sensitivity * p
        + fpr * (1 - p)
    )

    ppv_current = (
        sensitivity * p
        / p_test_positive
    )

    ppv_values.append(ppv_current)

    ppv_values = []

for p in prevalences:
    p_test_positive = (
        sensitivity * p
        + fpr * (1 - p)
    )

    ppv_current = (
        sensitivity * p
        / p_test_positive
    )

    ppv_values.append(ppv_current)

print("PPV values:")
print(ppv_values)

plt.plot(prevalences, ppv_values)

plt.xlabel("Prevalence")
plt.ylabel("PPV")
plt.title("PPV vs Prevalence")

plt.axvline(
    x=prevalence,
    linestyle="--"
)

plt.savefig("ppv_vs_prevalence.png")
plt.show()