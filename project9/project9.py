from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import t


# --------------------------------------------------
# Output directory
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent


# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

url = (
    "https://raw.githubusercontent.com/jbrownlee/"
    "Datasets/master/pima-indians-diabetes.data.csv"
)

columns = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
    "Outcome",
]

df = pd.read_csv(
    url,
    names=columns
)


# --------------------------------------------------
# 2. Define population
# --------------------------------------------------

glucose = df["Glucose"]

population_size = len(glucose)
population_mean = glucose.mean()

# Population standard deviation
population_std = glucose.std(ddof=0)


print("Population size:", population_size)
print("Population mean:", population_mean)
print("Population standard deviation:", population_std)


# --------------------------------------------------
# 3. Take samples with different sizes
# --------------------------------------------------

sample_sizes = [10, 30, 50, 100, 300]

rng = np.random.default_rng(42)

results = []


for n in sample_sizes:

    # Random sample without replacement
    sample = rng.choice(
        glucose.to_numpy(),
        size=n,
        replace=False
    )

    sample_mean = np.mean(sample)

    # Sample standard deviation
    sample_std = np.std(
        sample,
        ddof=1
    )

    # Standard Error
    se = sample_std / np.sqrt(n)

    # Critical t value for 95% CI
    t_critical = t.ppf(
        0.975,
        df=n - 1
    )

    margin_of_error = (
        t_critical * se
    )

    ci_lower = (
        sample_mean
        - margin_of_error
    )

    ci_upper = (
        sample_mean
        + margin_of_error
    )

    ci_width = (
        ci_upper
        - ci_lower
    )

    contains_population_mean = (
        ci_lower
        <= population_mean
        <= ci_upper
    )

    results.append({
        "Sample_Size": n,
        "Sample_Mean": sample_mean,
        "Sample_SD": sample_std,
        "SE": se,
        "T_Critical": t_critical,
        "CI_Lower": ci_lower,
        "CI_Upper": ci_upper,
        "CI_Width": ci_width,
        "Contains_Population_Mean":
            contains_population_mean,
    })


results_df = pd.DataFrame(
    results
)


# --------------------------------------------------
# 4. Save results
# --------------------------------------------------

results_df.to_csv(
    BASE_DIR / "project9_results.csv",
    index=False
)


print("\nSampling results:")
print(results_df.to_string(index=False))


# --------------------------------------------------
# 5. Plot CI width vs sample size
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    results_df["Sample_Size"],
    results_df["CI_Width"],
    marker="o"
)

plt.xlabel("Sample Size")
plt.ylabel("95% CI Width")
plt.title(
    "95% Confidence Interval Width "
    "vs Sample Size"
)

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    BASE_DIR
    / "ci_width_vs_sample_size.png",
    dpi=150
)

plt.close()


# --------------------------------------------------
# 6. Plot sample means and confidence intervals
# --------------------------------------------------

lower_errors = (
    results_df["Sample_Mean"]
    - results_df["CI_Lower"]
)

upper_errors = (
    results_df["CI_Upper"]
    - results_df["Sample_Mean"]
)

plt.figure(figsize=(9, 5))

plt.errorbar(
    results_df["Sample_Size"],
    results_df["Sample_Mean"],
    yerr=[
        lower_errors,
        upper_errors
    ],
    fmt="o",
    capsize=5,
    label="Sample mean + 95% CI"
)

plt.axhline(
    population_mean,
    linestyle="--",
    label="Population mean"
)

plt.xlabel("Sample Size")
plt.ylabel("Glucose")
plt.title(
    "Sample Means and 95% Confidence Intervals"
)

plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    BASE_DIR / "ci_intervals.png",
    dpi=150
)

plt.close()


# --------------------------------------------------
# 7. Central Limit Theorem
# --------------------------------------------------

clt_rng = np.random.default_rng(123)

number_of_samples = 1000
clt_sample_size = 50

sample_means = []


for _ in range(number_of_samples):

    sample = clt_rng.choice(
        glucose.to_numpy(),
        size=clt_sample_size,
        replace=False
    )

    sample_means.append(
        np.mean(sample)
    )


sample_means = np.array(
    sample_means
)

clt_mean = sample_means.mean()

clt_sd = sample_means.std(
    ddof=1
)


print(
    "\nMean of 1000 sample means:",
    clt_mean
)

print(
    "SD of sample means:",
    clt_sd
)


# --------------------------------------------------
# 8. Plot CLT histogram
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.hist(
    sample_means,
    bins=30,
    edgecolor="black"
)

plt.axvline(
    population_mean,
    linestyle="--",
    label="Population mean"
)

plt.xlabel("Sample Mean of Glucose")
plt.ylabel("Frequency")
plt.title(
    "Sampling Distribution of Mean "
    "(1000 Samples, n=50)"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    BASE_DIR / "clt_sample_means.png",
    dpi=150
)

plt.close()


# --------------------------------------------------
# 9. Generate report automatically
# --------------------------------------------------

table_text = results_df[
    [
        "Sample_Size",
        "Sample_Mean",
        "Sample_SD",
        "SE",
        "CI_Lower",
        "CI_Upper",
        "CI_Width",
        "Contains_Population_Mean",
    ]
].round(4).to_markdown(
    index=False
)


report = f"""
# Project 9: Sampling, Confidence Intervals and Generalizability in Diabetes

## 1. Introduction

Sampling is important in medical research because researchers usually cannot measure every individual in a population.

A sample is therefore used to estimate unknown characteristics of the population.

In this project, the Glucose variable from the Pima Indians Diabetes Dataset was used to study:

- Population and sample statistics
- Sampling error
- Standard Error
- 95% Confidence Intervals
- Sample size
- Central Limit Theorem

---

## 2. Population

For this project, the complete dataset was treated as the population.

Population size:

{population_size}

Population mean of Glucose:

{population_mean:.4f}

Population standard deviation:

{population_std:.4f}

The population mean is a parameter because it describes the full population used in this project.

A mean calculated from a random sample is a statistic.

---

## 3. Sampling

Random samples were selected without replacement.

The following sample sizes were studied:

- 10
- 30
- 50
- 100
- 300

Because each sample contains only part of the population, its mean is not expected to be exactly equal to the population mean.

This difference is an example of sampling variability.

---

## 4. Standard Error

For each sample, the Standard Error of the mean was calculated as:

SE = s / sqrt(n)

where:

- s is the sample standard deviation
- n is the sample size

Standard Error represents the uncertainty of the sample mean as an estimate of the population mean.

As sample size increases, Standard Error generally becomes smaller.

---

## 5. 95% Confidence Interval

The 95% Confidence Interval was calculated using the t distribution:

CI = sample mean ± t critical × SE

The t distribution was used because the population standard deviation is not assumed to be known when calculating the interval from a sample.

---

## 6. Results

{table_text}

The results show that sample means vary because of random sampling.

In general, larger samples produce smaller Standard Errors and narrower Confidence Intervals.

Therefore, larger samples usually provide more precise estimates of the population mean.

---

## 7. Confidence Interval Width

The plot `ci_width_vs_sample_size.png` shows the relationship between sample size and Confidence Interval width.

As the sample size increases, the Confidence Interval generally becomes narrower.

This occurs because:

SE = s / sqrt(n)

As n increases, the denominator becomes larger and SE decreases.

---

## 8. Population Mean and Confidence Intervals

The plot `ci_intervals.png` compares the sample mean and 95% Confidence Interval for each sample size with the population mean.

A Confidence Interval may or may not contain the true population mean in a particular sample.

A 95% Confidence Interval does not mean that there is a 95% probability that the fixed population mean is inside one particular calculated interval.

Instead, if the sampling procedure were repeated many times, approximately 95% of intervals constructed by this method would contain the true population mean.

---

## 9. Central Limit Theorem

To examine the Central Limit Theorem, 1000 random samples were generated.

Each sample contained 50 observations.

The mean Glucose value was calculated for every sample.

Mean of the 1000 sample means:

{clt_mean:.4f}

Standard deviation of sample means:

{clt_sd:.4f}

The histogram of sample means is stored in:

`clt_sample_means.png`

The sampling distribution of the mean tends to be more approximately Normal than the distribution of individual observations.

Its center is also close to the population mean.

This demonstrates the Central Limit Theorem.

---

## 10. Analytical Questions

### 1. Why is the sample mean not exactly equal to the population mean?

A random sample contains only part of the population.

Different random samples contain different observations, so their means vary.

This is called sampling variability.

---

### 2. What happens to CI width when sample size increases?

The Confidence Interval generally becomes narrower.

Larger samples reduce the Standard Error and increase the precision of the estimate.

---

### 3. What is the difference between SD and SE?

Standard Deviation describes the variability of individual observations.

Standard Error describes the variability or uncertainty of the sample mean.

SD describes the data.

SE describes the precision of the estimated mean.

---

### 4. What is the correct interpretation of a 95% CI?

If the same sampling and Confidence Interval procedure were repeated many times, approximately 95% of the calculated intervals would contain the true population mean.

---

### 5. What does the Central Limit Theorem say?

As sample size becomes sufficiently large, the sampling distribution of the sample mean tends toward a Normal distribution under appropriate conditions.

Its center approaches the population mean.

---

### 6. Does a 95% CI always contain the population mean?

No.

A particular 95% Confidence Interval can miss the true population mean.

The 95% refers to the long-run performance of the interval-building procedure.

---

### 7. Why can a large but biased sample be misleading?

A large sample reduces random sampling error, but it does not automatically remove systematic bias.

If the sample is not representative of the target population, a very large sample can still provide a precise but incorrect estimate.

---

## 11. Limitations

The full dataset was treated as the population for educational purposes.

In real medical research, the observed dataset is normally itself a sample from a much larger target population.

The quality of an estimate depends not only on sample size but also on:

- Sampling method
- Representativeness
- Measurement quality
- Missing data
- Selection bias

A large sample cannot automatically correct these problems.

---

## 12. Conclusion

This project demonstrated the relationship between sample size, Standard Error and Confidence Interval width.

Small samples showed greater uncertainty.

Larger samples generally produced narrower Confidence Intervals and more precise estimates.

The simulation of 1000 sample means also demonstrated the Central Limit Theorem.

Therefore, both sample size and sampling quality are important when generalizing medical research results from a sample to a population.
"""


with open(
    BASE_DIR / "report9.md",
    "w",
    encoding="utf-8"
) as file:

    file.write(
        report.strip()
    )


print("\nFiles saved:")
print("project9_results.csv")
print("ci_width_vs_sample_size.png")
print("ci_intervals.png")
print("clt_sample_means.png")
print("report9.md")