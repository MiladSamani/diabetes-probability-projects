import pandas as pd
import numpy as np
from scipy.stats import binom, poisson, norm
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

p = df["Outcome"].mean()

print("p:", p)

bernoulli_samples = np.random.binomial(
    n=1,
    p=p,
    size=10000
)

print("Bernoulli Mean:", bernoulli_samples.mean())

binomial_samples = np.random.binomial(
    n=50,
    p=p,
    size=10000
)

print("Binomial Mean:", binomial_samples.mean())

poisson_samples = np.random.poisson(
    lam=2,
    size=10000
)

print("Poisson Mean:", poisson_samples.mean())
print("Poisson Variance:", poisson_samples.var())

mu = df["BMI"].mean()
sigma = df["BMI"].std()

print("BMI Mean (mu):", mu)
print("BMI Standard Deviation (sigma):", sigma)

normal_samples = np.random.normal(
    loc=mu,
    scale=sigma,
    size=10000
)

print("Normal Simulation Mean:", normal_samples.mean())
print("Normal Simulation Variance:", normal_samples.var())

prob_7_of_10 = binom.pmf(
    7,
    n=10,
    p=p
)

print("P(exactly 7 out of 10):", prob_7_of_10)

prob_zero_poisson = poisson.pmf(
    0,
    mu=2
)

print("P(0 events with Poisson):", prob_zero_poisson)

prob_bmi_above_35 = norm.sf(
    35,
    loc=mu,
    scale=sigma
)

print("P(BMI > 35):", prob_bmi_above_35)

comparison = pd.DataFrame({
    "Distribution": [
        "Bernoulli",
        "Binomial",
        "Poisson",
        "Normal"
    ],

    "Theoretical Mean": [
        p,
        50 * p,
        2,
        mu
    ],

    "Simulation Mean": [
        bernoulli_samples.mean(),
        binomial_samples.mean(),
        poisson_samples.mean(),
        normal_samples.mean()
    ],

    "Theoretical Variance": [
        p * (1 - p),
        50 * p * (1 - p),
        2,
        sigma ** 2
    ],

    "Simulation Variance": [
        bernoulli_samples.var(),
        binomial_samples.var(),
        poisson_samples.var(),
        normal_samples.var()
    ]
})

print(comparison)


values, counts = np.unique(
    bernoulli_samples,
    return_counts=True
)

plt.bar(values, counts)

plt.title("Bernoulli Distribution")
plt.xlabel("Outcome")
plt.ylabel("Count")

plt.xticks([0, 1])

plt.savefig("bernoulli_distribution_p4.png")
plt.close()

plt.hist(
    binomial_samples,
    bins=20
)

plt.title("Binomial Distribution")
plt.xlabel("Number of Successes")
plt.ylabel("Frequency")

plt.savefig("binomial_distribution_p4.png")
plt.close()

plt.hist(
    poisson_samples,
    bins=range(0, max(poisson_samples) + 2),
    align="left"
)

plt.title("Poisson Distribution")
plt.xlabel("Number of Events")
plt.ylabel("Frequency")

plt.savefig("poisson_distribution_p4.png")
plt.close()

plt.hist(
    normal_samples,
    bins=30
)

plt.title("Normal Distribution")
plt.xlabel("BMI")
plt.ylabel("Frequency")

plt.savefig("normal_distribution_p4.png")
plt.close()