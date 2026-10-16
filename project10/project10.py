from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import ttest_ind, chi2_contingency, t


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


print("Dataset shape:", df.shape)

print("\nOutcome counts:")
print(df["Outcome"].value_counts())


# --------------------------------------------------
# 2. Create groups
# --------------------------------------------------

diabetic = df[df["Outcome"] == 1]
non_diabetic = df[df["Outcome"] == 0]

print("\nDiabetic patients:", len(diabetic))
print("Non-diabetic patients:", len(non_diabetic))


# --------------------------------------------------
# 3. Variables for t-tests
# --------------------------------------------------

variables = [
    "Glucose",
    "BMI",
    "Age",
    "BloodPressure",
]

alpha = 0.05

results = []


# --------------------------------------------------
# Helper: Cohen's d
# --------------------------------------------------

def cohens_d(group1, group0):

    n1 = len(group1)
    n0 = len(group0)

    var1 = np.var(
        group1,
        ddof=1
    )

    var0 = np.var(
        group0,
        ddof=1
    )

    pooled_variance = (
        ((n1 - 1) * var1)
        + ((n0 - 1) * var0)
    ) / (
        n1 + n0 - 2
    )

    pooled_sd = np.sqrt(
        pooled_variance
    )

    d = (
        np.mean(group1)
        - np.mean(group0)
    ) / pooled_sd

    return d


# --------------------------------------------------
# Helper: common Cohen's d interpretation
# --------------------------------------------------

def interpret_d(d):

    value = abs(d)

    if value < 0.2:
        return "Very small"

    elif value < 0.5:
        return "Small"

    elif value < 0.8:
        return "Medium"

    else:
        return "Large"


# --------------------------------------------------
# 4. Welch t-tests
# --------------------------------------------------

for variable in variables:

    group1 = (
        diabetic[variable]
        .dropna()
        .to_numpy()
    )

    group0 = (
        non_diabetic[variable]
        .dropna()
        .to_numpy()
    )


    # ----------------------------------------------
    # Basic statistics
    # ----------------------------------------------

    n1 = len(group1)
    n0 = len(group0)

    mean1 = np.mean(group1)
    mean0 = np.mean(group0)

    var1 = np.var(
        group1,
        ddof=1
    )

    var0 = np.var(
        group0,
        ddof=1
    )


    mean_difference = (
        mean1 - mean0
    )


    # ----------------------------------------------
    # Welch independent t-test
    # ----------------------------------------------

    t_statistic, p_value = ttest_ind(
        group1,
        group0,
        equal_var=False
    )


    # ----------------------------------------------
    # Standard Error for mean difference
    # ----------------------------------------------

    se_difference = np.sqrt(
        var1 / n1
        +
        var0 / n0
    )


    # ----------------------------------------------
    # Welch-Satterthwaite degrees of freedom
    # ----------------------------------------------

    numerator = (
        var1 / n1
        +
        var0 / n0
    ) ** 2

    denominator = (
        ((var1 / n1) ** 2)
        / (n1 - 1)
        +
        ((var0 / n0) ** 2)
        / (n0 - 1)
    )

    welch_df = (
        numerator
        / denominator
    )


    # ----------------------------------------------
    # 95% Confidence Interval
    # ----------------------------------------------

    t_critical = t.ppf(
        0.975,
        df=welch_df
    )

    margin_of_error = (
        t_critical
        * se_difference
    )

    ci_lower = (
        mean_difference
        - margin_of_error
    )

    ci_upper = (
        mean_difference
        + margin_of_error
    )


    # ----------------------------------------------
    # Cohen's d
    # ----------------------------------------------

    d = cohens_d(
        group1,
        group0
    )

    d_interpretation = (
        interpret_d(d)
    )


    # ----------------------------------------------
    # Statistical significance
    # ----------------------------------------------

    significant = (
        p_value < alpha
    )


    results.append({
        "Variable": variable,
        "Mean_Diabetic": mean1,
        "Mean_NonDiabetic": mean0,
        "Mean_Difference": mean_difference,
        "SE_Difference": se_difference,
        "T_Statistic": t_statistic,
        "Welch_DF": welch_df,
        "P_Value": p_value,
        "CI_Lower": ci_lower,
        "CI_Upper": ci_upper,
        "Cohens_d": d,
        "Effect_Size": d_interpretation,
        "Significant_0.05": significant,
    })


results_df = pd.DataFrame(
    results
)


# --------------------------------------------------
# 5. Save t-test results
# --------------------------------------------------

results_df.to_csv(
    BASE_DIR
    / "project10_ttest_results.csv",
    index=False
)


print("\nWelch t-test results:")

print(
    results_df.to_string(
        index=False
    )
)


# --------------------------------------------------
# 6. High Glucose variable
# --------------------------------------------------

df["HighGlucose"] = (
    df["Glucose"] >= 140
).astype(int)


# --------------------------------------------------
# 7. Contingency table
# --------------------------------------------------

contingency_table = pd.crosstab(
    df["HighGlucose"],
    df["Outcome"]
)

contingency_table.index = [
    "Glucose < 140",
    "Glucose >= 140",
]

contingency_table.columns = [
    "Non-Diabetic",
    "Diabetic",
]


print(
    "\nHigh Glucose x Diabetes:"
)

print(
    contingency_table
)


contingency_table.to_csv(
    BASE_DIR
    / "project10_contingency_table.csv"
)


# --------------------------------------------------
# 8. Chi-square test
# --------------------------------------------------

chi2_statistic, chi2_p_value, chi2_df, expected = (
    chi2_contingency(
        contingency_table
    )
)


expected_df = pd.DataFrame(
    expected,
    index=contingency_table.index,
    columns=contingency_table.columns
)


expected_df.to_csv(
    BASE_DIR
    / "project10_expected_counts.csv"
)


print(
    "\nChi-square statistic:",
    chi2_statistic
)

print(
    "Chi-square p-value:",
    chi2_p_value
)

print(
    "Degrees of freedom:",
    chi2_df
)

print(
    "\nExpected counts:"
)

print(
    expected_df
)


# --------------------------------------------------
# 9. Multiple-testing threshold
# --------------------------------------------------

number_of_t_tests = len(variables)

bonferroni_alpha = (
    alpha / number_of_t_tests
)


print(
    "\nOriginal alpha:",
    alpha
)

print(
    "Bonferroni alpha:",
    bonferroni_alpha
)


# --------------------------------------------------
# 10. Create Markdown tables
# --------------------------------------------------

report_table = (
    results_df[
        [
            "Variable",
            "Mean_Diabetic",
            "Mean_NonDiabetic",
            "Mean_Difference",
            "T_Statistic",
            "P_Value",
            "CI_Lower",
            "CI_Upper",
            "Cohens_d",
            "Effect_Size",
            "Significant_0.05",
        ]
    ]
    .round(4)
    .to_markdown(
        index=False
    )
)


contingency_markdown = (
    contingency_table
    .to_markdown()
)


# --------------------------------------------------
# 11. Significant variables
# --------------------------------------------------

significant_variables = (
    results_df[
        results_df[
            "Significant_0.05"
        ]
    ]["Variable"]
    .tolist()
)


if significant_variables:

    significant_text = ", ".join(
        significant_variables
    )

else:

    significant_text = (
        "None"
    )


# --------------------------------------------------
# 12. Chi-square interpretation
# --------------------------------------------------

if chi2_p_value < alpha:

    chi_square_conclusion = (
        "The association is statistically "
        "significant at alpha = 0.05."
    )

else:

    chi_square_conclusion = (
        "The association is not statistically "
        "significant at alpha = 0.05."
    )


# --------------------------------------------------
# 13. Generate report
# --------------------------------------------------

report = f"""
# Project 10: Hypothesis Testing in Diabetes

## 1. Introduction

Hypothesis testing is used in medical research to evaluate whether an observed difference or association is likely to represent a real pattern rather than random sampling variation.

In this project, the Pima Indians Diabetes Dataset was used to compare diabetic and non-diabetic patients.

The following variables were studied:

- Glucose
- BMI
- Age
- Blood Pressure

Welch independent t-tests were used for continuous variables.

A Chi-square test was used to examine the association between high glucose and diabetes.

The significance level was:

alpha = 0.05

---

## 2. Groups

The dataset contains:

Diabetic patients:

{len(diabetic)}

Non-diabetic patients:

{len(non_diabetic)}

Total:

{len(df)}

---

## 3. Hypotheses for the t-tests

For each variable, the hypotheses were:

H0:

The mean value is equal between diabetic and non-diabetic patients.

Mean_diabetic = Mean_non_diabetic

H1:

The mean value is different between diabetic and non-diabetic patients.

Mean_diabetic != Mean_non_diabetic

The tests were two-sided.

---

## 4. Welch Independent t-test

Welch's t-test was used because it does not require the two groups to have equal variances.

For each variable, the difference was calculated as:

Mean Difference =
Mean Diabetic - Mean Non-Diabetic

The results were:

{report_table}

At alpha = 0.05, the statistically significant variables were:

{significant_text}

---

## 5. Confidence Interval for the Mean Difference

The Standard Error of the difference between two independent means was calculated as:

SE_difference =
sqrt(
    s1^2 / n1
    +
    s0^2 / n0
)

The 95% Confidence Interval was calculated as:

CI =
Mean Difference
±
t critical × SE_difference

If the confidence interval does not contain zero, this is consistent with a statistically significant difference at approximately the 0.05 level for a two-sided test.

---

## 6. Cohen's d

Cohen's d was used to describe the standardized difference between the two group means.

The formula used was:

d =
(Mean Diabetic - Mean Non-Diabetic)
/
Pooled Standard Deviation

A common descriptive interpretation was used:

- |d| < 0.2: very small
- 0.2 <= |d| < 0.5: small
- 0.5 <= |d| < 0.8: medium
- |d| >= 0.8: large

These categories are statistical conventions and should not automatically be interpreted as clinical importance.

---

## 7. High Glucose and Diabetes

A new binary variable was created:

HighGlucose = 1 when Glucose >= 140

HighGlucose = 0 when Glucose < 140

The contingency table was:

{contingency_markdown}

---

## 8. Chi-square Test

The hypotheses for the Chi-square test were:

H0:

HighGlucose and diabetes status are independent.

H1:

HighGlucose and diabetes status are associated.

Results:

Chi-square statistic:

{chi2_statistic:.4f}

Degrees of freedom:

{chi2_df}

p-value:

{chi2_p_value:.8g}

Conclusion:

{chi_square_conclusion}

---

## 9. Interpretation of the p-value

A p-value measures how compatible the observed data are with the null hypothesis.

A small p-value indicates that the observed result would be relatively unusual if the null hypothesis were true.

In this project:

p < 0.05

was treated as statistically significant.

A statistically significant result does not prove that the alternative hypothesis is true.

It means the data provide evidence against the null hypothesis under the assumptions of the test.

---

## 10. Does a Large p-value Mean There Is No Effect?

No.

A large p-value does not prove that the effect is zero.

Possible reasons for a large p-value include:

- A genuinely small or absent effect
- High variability
- Insufficient sample size
- Low statistical power

Therefore, effect size and Confidence Intervals should also be examined.

---

## 11. Type I and Type II Errors

### Type I Error

A Type I error occurs when the null hypothesis is actually true but we reject it.

In this project, an example would be concluding that a variable differs between diabetic and non-diabetic patients when no real difference exists.

The probability of a Type I error is controlled by alpha.

Here:

alpha = 0.05

### Type II Error

A Type II error occurs when a real difference exists but the statistical test fails to detect it.

This may occur when:

- The sample is too small
- The effect is small
- The data have high variability

Statistical power is related to the probability of detecting a real effect.

---

## 12. Statistical Significance vs Clinical Importance

Statistical significance and clinical importance are not the same.

A very small difference may become statistically significant when the sample size is large.

However, that difference may have little practical or clinical importance.

Conversely, a clinically important effect may fail to reach statistical significance when the study has low power.

Therefore, medical interpretation should consider:

- p-value
- Confidence Interval
- Effect size
- Clinical context

not only statistical significance.

---

## 13. Multiple Testing

Four separate t-tests were performed:

- Glucose
- BMI
- Age
- Blood Pressure

When several statistical tests are performed, the probability of obtaining at least one false-positive result increases.

The original significance level was:

alpha = {alpha}

As a simple reference, a Bonferroni-adjusted threshold for four tests would be:

alpha / 4 = {bonferroni_alpha:.4f}

The project did not require applying a multiple-testing correction to the main conclusions, but this issue should be considered when interpreting several simultaneous tests.

---

## 14. Limitations

This analysis has several limitations.

The Pima dataset is treated directly as provided in the project.

Some variables in the raw dataset can contain values such as zero that may require additional clinical data-quality assessment.

No data-cleaning rule was specified as part of this hypothesis-testing project, so the statistical tests were performed on the supplied dataset without adding a new cleaning procedure.

Statistical significance also does not establish causality.

The analysis compares groups and associations but does not prove that one variable causes diabetes.

---

## 15. Conclusion

This project used hypothesis testing to compare diabetic and non-diabetic patients.

Welch independent t-tests were used to compare continuous variables.

Confidence Intervals were used to describe uncertainty in the differences between group means.

Cohen's d was used to describe standardized effect size.

A Chi-square test was used to examine the relationship between high glucose and diabetes.

The project demonstrates why p-values should be interpreted together with Confidence Intervals, effect sizes, statistical power, multiple-testing considerations, and clinical relevance.
"""


# --------------------------------------------------
# 14. Save report
# --------------------------------------------------

with open(
    BASE_DIR / "report10.md",
    "w",
    encoding="utf-8"
) as file:

    file.write(
        report.strip()
    )


# --------------------------------------------------
# 15. Final output
# --------------------------------------------------

print("\nFiles saved:")

print(
    "project10_ttest_results.csv"
)

print(
    "project10_contingency_table.csv"
)

print(
    "project10_expected_counts.csv"
)

print(
    "report10.md"
)