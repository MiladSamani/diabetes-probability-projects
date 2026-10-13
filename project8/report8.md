# Project 8: Cleaning and Preparing Simulated Medical Data

## 1. Objective

The goal of this project was to examine and clean a simulated medical dataset.

The main data quality problems included:

- Missing values
- Special missing-value codes
- Invalid clinical values
- Inconsistent categorical coding
- Duplicate records

The final goal was to prepare a cleaner dataset for future statistical or machine learning analysis.

---

## 2. Dataset

A simulated dataset containing 200 patients was generated.

The variables included:

- Patient ID
- Age
- Sex
- Systolic Blood Pressure
- HbA1c
- SpO2

Artificial data quality problems were then added.

Two duplicate records were also added, resulting in an initial dataset containing 202 rows.

---

## 3. Special Missing Values

The value 999 was used as a special missing-value code in some variables.

These values were converted to NaN before further analysis.

This is important because missing information is not always stored directly as NaN in real medical datasets.

---

## 4. Duplicate Records

Two exact duplicate records were added to the simulated dataset.

The original dataset therefore contained:

202 rows

After removing exact duplicate rows:

200 rows remained.

Therefore:

2 duplicate records were removed.

In real medical datasets, duplicate records should not always be deleted automatically because the same patient may have multiple legitimate visits or measurements.

---

## 5. Cleaning the Sex Variable

The Sex variable contained several different representations:

- Male
- male
- M
- Female
- female
- F

These values were standardized into two categories:

- Male
- Female

This prevents different spellings from being treated as separate categories.

---

## 6. Clinical Valid Ranges

The following educational valid ranges were used:

- Age: 0 to 120 years
- Systolic Blood Pressure: 50 to 300 mmHg
- HbA1c: 3 to 20 percent
- SpO2: 0 to 100 percent

Values outside these ranges were flagged as invalid and converted to NaN.

These ranges are educational examples and should not be considered universal clinical rules.

In real medical research, valid ranges should be defined using clinical knowledge, the study population, measurement devices, and the purpose of the analysis.

---

## 7. Invalid Values

In this simulation, the approximate number of invalid values detected was:

- Age: 2
- Systolic Blood Pressure: 2
- HbA1c: 1
- SpO2: 8

SpO2 had the largest number of values outside the defined valid range.

Some invalid values were deliberately inserted, while others could occur naturally because the data were randomly simulated.

---

## 8. Missing Values After Validation

Some missing values existed in the original dataset.

Additional missing values were created during cleaning because invalid values were converted to NaN.

After validation, the approximate missing counts were:

- Age: 3
- Systolic Blood Pressure: 3
- HbA1c: 3
- SpO2: 8

This demonstrates that not all missing values must exist in the original raw dataset.

Some may be created during data validation when impossible or unacceptable measurements are identified.

---

## 9. Missing Indicators

For every numerical variable, a missing indicator was created.

For example:

age_missing = 0

means the value was available.

age_missing = 1

means the original value was missing or became missing after validation.

A missing indicator allows a future model or analysis to retain information about which measurements were originally unavailable.

---

## 10. Median Imputation

Missing numerical values were replaced using the median of the valid observations.

Median imputation was selected because the median is more resistant to extreme values and skewed distributions than the mean.

However, simple median imputation also has limitations.

It can reduce the natural variability of the data and may weaken relationships between variables.

Therefore, it should not automatically be considered the best method for every medical dataset.

---

## 11. Analytical Questions

### How many duplicate records were removed?

Two exact duplicate records were removed.

### Which variable had the largest number of invalid values?

In this simulated dataset, SpO2 had the largest number of values outside the specified valid range.

### What happened to invalid values?

Invalid values were first flagged and then converted to NaN.

They were later handled using median imputation.

### Were all missing values missing from the beginning?

No.

Some values were already missing in the raw dataset.

Other missing values were created during data validation after invalid measurements were converted to NaN.

### Why was median imputation used?

The median is less sensitive to extreme values than the mean.

This makes it a simple and relatively robust choice for this educational project.

### What risks would remain before using the data for disease prediction?

Several risks still remain.

The missing-data mechanism has not been fully studied.

Median imputation can reduce real variability.

The valid clinical ranges used here are simplified educational ranges.

The simulated dataset may not represent a real clinical population.

Relationships between missingness and patient characteristics should also be examined.

If longitudinal data were used, temporal leakage would also need to be checked.

Therefore, cleaning the dataset does not automatically guarantee that the dataset is appropriate for machine learning.

---

## 12. Conclusion

This project demonstrated that medical data cleaning involves more than simply deleting unusual values.

A proper cleaning process should:

1. Preserve the raw dataset.
2. Identify missing values.
3. Recognize special missing codes.
4. Check valid clinical ranges.
5. Standardize categorical variables.
6. Investigate duplicate records.
7. Flag invalid measurements.
8. Handle missing data carefully.
9. Document all cleaning decisions.

Medical outliers and unusual measurements should not automatically be removed because they may represent clinically important patients.

Data cleaning should combine statistical reasoning with clinical knowledge.