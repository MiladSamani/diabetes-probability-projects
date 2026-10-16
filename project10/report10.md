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

268

Non-diabetic patients:

500

Total:

768

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

| Variable      |   Mean_Diabetic |   Mean_NonDiabetic |   Mean_Difference |   T_Statistic |   P_Value |   CI_Lower |   CI_Upper |   Cohens_d | Effect_Size   | Significant_0.05   |
|:--------------|----------------:|-------------------:|------------------:|--------------:|----------:|-----------:|-----------:|-----------:|:--------------|:-------------------|
| Glucose       |        141.257  |           109.98   |           31.2775 |       13.7515 |    0      |    26.8079 |    35.7471 |     1.1053 | Large         | True               |
| BMI           |         35.1425 |            30.3042 |            4.8383 |        8.6193 |    0      |     3.7358 |     5.9409 |     0.6414 | Medium        | True               |
| Age           |         37.0672 |            31.19   |            5.8772 |        6.9207 |    0      |     4.2092 |     7.5451 |     0.5142 | Medium        | True               |
| BloodPressure |         70.8246 |            68.184  |            2.6406 |        1.7131 |    0.0874 |    -0.3883 |     5.6696 |     0.1366 | Very small    | False              |

At alpha = 0.05, the statistically significant variables were:

Glucose, BMI, Age

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

|                |   Non-Diabetic |   Diabetic |
|:---------------|---------------:|-----------:|
| Glucose < 140  |            438 |        133 |
| Glucose >= 140 |             62 |        135 |

---

## 8. Chi-square Test

The hypotheses for the Chi-square test were:

H0:

HighGlucose and diabetes status are independent.

H1:

HighGlucose and diabetes status are associated.

Results:

Chi-square statistic:

129.9382

Degrees of freedom:

1

p-value:

4.2273662e-30

Conclusion:

The association is statistically significant at alpha = 0.05.

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

alpha = 0.05

As a simple reference, a Bonferroni-adjusted threshold for four tests would be:

alpha / 4 = 0.0125

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