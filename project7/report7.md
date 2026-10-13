# Project 7: Descriptive Analysis of Simulated Medical Data

## 1. Objective

The goal of this project was to study descriptive statistics for simulated medical data.

The analysis focused on:

- Measures of central tendency
- Measures of variability
- Skewness
- Outlier detection
- Histograms
- Boxplots
- Choosing appropriate summary statistics

Three variables were analyzed:

- Age
- Systolic blood pressure
- Length of stay

---

## 2. Dataset

A simulated dataset containing 300 patients was created.

The Age and Systolic Blood Pressure variables were generated approximately from Normal distributions.

Length of Stay was generated from an Exponential distribution. Several large values were also added to demonstrate positive skewness and outliers.

---

## 3. Descriptive Statistics

### Age

Approximate results:

- Mean: 54.93
- Median: 56
- Standard deviation: 11.84
- IQR: 16
- Skewness: 0.18
- Number of IQR outliers: 3

The mean and median are close and the skewness is small. Therefore, the Age distribution is approximately symmetric.

Mean and standard deviation are reasonable summary measures for Age.

---

### Systolic Blood Pressure

Approximate results:

- Mean: 127.61
- Median: 127.66
- Standard deviation: 17.31
- IQR: 23.77
- Skewness: 0.13
- Number of IQR outliers: 1

The mean and median are almost equal and skewness is close to zero.

Therefore, Systolic Blood Pressure is approximately symmetric.

Mean and standard deviation are appropriate summary statistics.

---

### Length of Stay

Approximate results:

- Mean: 4.34
- Median: 3
- Standard deviation: 5.40
- IQR: 4.25
- Skewness: 3.32
- Number of IQR outliers: 20

Length of Stay has strong positive skewness.

A small number of patients have much longer hospital stays than most patients. These large values increase the mean.

Therefore, Median and IQR are more appropriate than Mean and Standard Deviation for summarizing Length of Stay.

---

## 4. Outlier Detection

Outliers were detected using the IQR rule:

IQR = Q3 - Q1

Lower Fence = Q1 - 1.5 × IQR

Upper Fence = Q3 + 1.5 × IQR

Values below the lower fence or above the upper fence were considered potential outliers.

An outlier should not automatically be treated as an error, especially in medical data. It may represent a real and clinically important patient.

---

## 5. Histograms and Boxplots

Histograms were used to study the shape of each distribution.

Boxplots were used to visualize the median, quartiles, spread, and potential outliers.

Age and Systolic Blood Pressure appeared approximately symmetric.

Length of Stay showed a long right tail and several high values.

---

## 6. Analytical Questions

### Which variable is approximately symmetric?

Age and Systolic Blood Pressure are approximately symmetric.

Their mean and median values are close and their skewness values are near zero.

### Which variable has positive skewness?

Length of Stay has strong positive skewness.

Its skewness is approximately 3.32 and its distribution has a long right tail.

### Which variable has more outliers?

Length of Stay has the largest number of outliers using the IQR rule.

### Which summary statistics should be used?

For approximately symmetric variables such as Age and Systolic Blood Pressure:

Mean + Standard Deviation

For the strongly skewed Length of Stay variable:

Median + IQR

### Could a log transformation help Length of Stay?

Yes.

Length of Stay is strongly right-skewed. A log transformation may reduce the influence of very large values and make the distribution more symmetric.

However, the usefulness of the transformation should be evaluated after examining the transformed data.

---

## 7. Conclusion

This project showed that descriptive statistics should be selected according to the shape of the data.

Mean and Standard Deviation are useful for approximately symmetric distributions.

Median and IQR are more robust for skewed distributions and distributions containing extreme values.

Histograms, boxplots, skewness, and outlier analysis should therefore be examined before selecting summary statistics or building a statistical or machine learning model.