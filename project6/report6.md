# Descriptive Statistics and Clinical Data Analysis

## 1. Introduction

Descriptive statistics help summarize and understand medical data.

Important measures include:

- Mean
- Median
- Standard deviation
- Interquartile range
- Minimum and maximum
- Skewness
- Outliers

The goal of this analysis is to describe the distribution of several medical variables and determine which summary measures are most appropriate.

---

## 2. Dataset

The Pima Indians Diabetes Dataset was used.

The variables analyzed are:

- Glucose
- BMI
- Age
- BloodPressure
- Insulin
- SkinThickness

The dataset contains 768 observations.

---

# 3. Descriptive Statistics

The descriptive statistics are approximately:

| Variable | Mean | Median | SD | IQR | Min | Max |
|---|---:|---:|---:|---:|---:|---:|
| Glucose | 120.89 | 117.0 | 31.97 | 41.25 | 0 | 199 |
| BMI | 31.99 | 32.0 | 7.88 | 9.30 | 0 | 67.1 |
| Age | 33.24 | 29.0 | 11.76 | 17.00 | 21 | 81 |
| BloodPressure | 69.11 | 72.0 | 19.36 | 18.00 | 0 | 122 |
| Insulin | 79.80 | 30.5 | 115.24 | 127.25 | 0 | 846 |
| SkinThickness | 20.54 | 23.0 | 15.95 | 32.00 | 0 | 99 |

The mean represents the average value.

The median represents the middle observation.

Standard deviation describes the spread around the mean.

IQR describes the spread of the middle 50% of the observations.

---

# 4. Interquartile Range

The interquartile range is calculated as:

```text
IQR = Q3 - Q1
```

Outlier boundaries are calculated using:

```text
Lower Bound = Q1 - 1.5 × IQR

Upper Bound = Q3 + 1.5 × IQR
```

Any value below the lower bound or above the upper bound is considered a potential outlier.

---

# 5. Outlier Analysis

Using the IQR method on the raw dataset gives approximately:

| Variable | Outliers |
|---|---:|
| Glucose | 5 |
| BMI | 19 |
| Age | 9 |
| BloodPressure | 45 |
| Insulin | 34 |
| SkinThickness | 1 |

For example, the BMI IQR is approximately 9.3.

Its outlier boundaries are:

```text
Lower Bound = 13.35
Upper Bound = 50.55
```

Values outside these limits are considered potential outliers.

The original BMI distribution contains 19 such observations.

Age has an upper IQR boundary of approximately:

```text
66.5 years
```

and 9 observations are above this boundary.

---

# 6. Why Outliers Should Not Automatically Be Removed

An outlier is an unusual observation, but unusual does not automatically mean incorrect.

In medical data, an extreme observation can represent:

- a high-risk patient
- a rare medical condition
- an unusual but real measurement
- a data-entry or measurement problem

Therefore, an outlier should first be investigated before it is removed.

Automatic removal can cause important clinical information to be lost.

---

# 7. Skewness

Skewness describes the asymmetry of a distribution.

The approximate skewness values are:

| Variable | Skewness | Direction |
|---|---:|---|
| Glucose | 0.174 | Slight positive |
| BMI | -0.428 | Slight negative |
| Age | 1.129 | Positive |
| BloodPressure | -1.844 | Negative |
| Insulin | 2.272 | Strong positive |
| SkinThickness | 0.109 | Slight positive |

A positive skew means the distribution has a longer right tail.

A negative skew means the distribution has a longer left tail.

A value close to zero indicates a more symmetric distribution.

---

# 8. Mean and Median

The relationship between the mean and median can help identify skewness.

For example:

```text
Age:

Mean = 33.24
Median = 29
```

The mean is greater than the median, which is consistent with positive skewness.

For Insulin:

```text
Mean = 79.80
Median = 30.5
```

There is a large difference between the mean and median.

This suggests that high Insulin values strongly affect the mean.

For BMI:

```text
Mean = 31.99
Median = 32
```

The values are very close, indicating much less difference between the two measures of center.

---

# 9. Histograms

A histogram was generated for each variable.

The generated files are:

```text
glucose_histogram.png
bmi_histogram.png
age_histogram.png
bloodpressure_histogram.png
insulin_histogram.png
skinthickness_histogram.png
```

Histograms help show:

- distribution shape
- skewness
- concentration of observations
- unusual values

---

# 10. Boxplots

Boxplots were generated for:

- Glucose
- BMI
- Age

Files:

```text
glucose_boxplot.png
bmi_boxplot.png
age_boxplot.png
```

A boxplot shows:

- Median
- Q1
- Q3
- IQR
- Potential outliers

---

# 11. Clinical Summary

A simple educational rule was used for choosing summary measures:

```text
Low skewness
→ Mean + SD

Noticeable skewness
→ Median + IQR
```

This rule was added for this analysis; the assignment itself does not define a numerical threshold.

Based on this simple rule:

| Variable | Suggested Summary |
|---|---|
| Glucose | Mean + SD |
| BMI | Mean + SD |
| Age | Median + IQR |
| BloodPressure | Median + IQR |
| Insulin | Median + IQR |
| SkinThickness | Mean + SD |

In real clinical analysis, distribution shape, data quality, and clinical meaning should also be considered before choosing a summary measure.

---

# Analytical Questions

## 12. Which variables have positive skewness?

Positive skewness means the right tail is longer.

The clearest positively skewed variables are:

```text
Age
Insulin
```

Insulin has particularly strong positive skewness.

Glucose and SkinThickness also have slightly positive skewness, but their values are much closer to zero.

---

## 13. For which variables is the mean a reasonable summary?

The mean is generally easier to interpret when the distribution is approximately symmetric and is not strongly affected by extreme observations.

Glucose and BMI have relatively small skewness values in the raw dataset.

Therefore, their mean can be useful.

However, the distribution and data quality should still be checked before making a clinical conclusion.

---

## 14. What do the Median and IQR tell us about BMI?

The BMI median is:

```text
32.0
```

This represents the middle BMI value.

The BMI IQR is:

```text
9.3
```

This means that the middle 50% of BMI observations are spread across a range of approximately 9.3 units.

Median and IQR are less affected by extreme observations than mean and standard deviation.

---

## 15. How many Glucose outliers are present?

Using the IQR rule on the raw dataset:

```text
Q1 = 99
Q3 = 140.25

IQR = 41.25
```

Therefore:

```text
Lower Bound = 37.125
Upper Bound = 202.125
```

Five Glucose values are below the lower boundary.

Therefore:

```text
Glucose Outliers = 5
```

---

## 16. Why is automatic outlier removal dangerous in medicine?

Extreme values can contain clinically important information.

For example, an unusually high measurement may represent a high-risk patient rather than a data error.

Automatically deleting such observations can:

- remove important patients
- hide rare conditions
- change the distribution
- create biased conclusions

Therefore, outliers should be investigated rather than automatically removed.

---

## 17. Which measures are appropriate for clinical reporting?

For approximately symmetric variables, useful measures are:

```text
Mean
Standard Deviation
```

For skewed variables or variables strongly affected by extreme values, useful measures are:

```text
Median
IQR
```

Therefore, the shape of the distribution should be examined before choosing the summary statistics.

---

## 18. Is the Mean of Insulin a Good Representative Value?

The mean Insulin value is approximately:

```text
79.80
```

while the median is:

```text
30.5
```

and the skewness is approximately:

```text
2.27
```

The large difference between the mean and median and the strong positive skew indicate that the mean is strongly influenced by high Insulin observations.

Therefore, the mean alone is not a good representation of the typical Insulin value.

Median and IQR are more resistant to extreme values.

---

# 19. Important Limitation

This analysis follows the assignment and uses the raw dataset directly.

No preprocessing or replacement of unusual zero values was requested in the assignment.

Therefore, zero values remain part of the calculations.

These values can affect:

- Mean
- Standard deviation
- Skewness
- Outlier detection

This should be considered when interpreting the results.

---

# 20. Conclusion

Descriptive statistics provide information about both the center and spread of medical data.

The main concepts used were:

```text
Mean
Median
Standard Deviation
IQR
Skewness
Outliers
```

The IQR method was used to identify potential outliers.

Skewness was used to understand the shape of each distribution.

Insulin and Age showed clear positive skewness.

BloodPressure showed negative skewness.

Glucose, BMI, and SkinThickness were closer to symmetry in terms of their raw skewness values.

The most important lesson is that one statistic is not appropriate for every variable.

For approximately symmetric variables:

```text
Mean + SD
```

can be useful.

For skewed variables:

```text
Median + IQR
```

are usually more resistant to extreme values.

Finally, medical outliers should not be automatically removed because they may contain important clinical information.