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


preg_counts = df["Pregnancies"].value_counts().sort_index()

preg_probs = preg_counts / len(df)

expected_preg = sum(
    x * p
    for x, p in preg_probs.items()
)

expected_square = sum(
    (x ** 2) * p
    for x, p in preg_probs.items()
)

variance_preg = expected_square - (expected_preg ** 2)

print("E[X]:", expected_preg)
print("E[X^2]:", expected_square)
print("Var(X):", variance_preg)

bmi_mean = df["BMI"].mean()
bmi_variance = df["BMI"].var()

print("BMI Mean:", bmi_mean)
print("BMI Variance:", bmi_variance)

p = df["Outcome"].mean()

print("p:", p)

theoretical_mean = p
theoretical_variance = p * (1 - p)

samples = np.random.binomial(
    n=1,
    p=p,
    size=10000
)

simulation_mean = samples.mean()
simulation_variance = samples.var()

print("Theoretical Mean:", theoretical_mean)
print("Simulation Mean:", simulation_mean)

print("Theoretical Variance:", theoretical_variance)
print("Simulation Variance:", simulation_variance)

preg_counts.plot(kind="bar")

plt.title("Pregnancies Distribution")
plt.xlabel("Number of Pregnancies")
plt.ylabel("Count")

plt.savefig("pregnancies_distribution.png")
plt.close()

plt.hist(df["BMI"], bins=20)

plt.title("BMI Distribution")
plt.xlabel("BMI")
plt.ylabel("Frequency")

plt.savefig("bmi_distribution.png")
plt.close()

unique, counts = np.unique(samples, return_counts=True)

plt.bar(unique, counts)

plt.title("Bernoulli Simulation")
plt.xlabel("Outcome")
plt.ylabel("Count")

plt.xticks([0, 1])

plt.savefig("bernoulli_simulation.png")
plt.close()