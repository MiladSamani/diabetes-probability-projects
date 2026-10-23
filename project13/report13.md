# Project 13: Logistic Regression for Diabetes Prediction

## 1. Introduction

The Pima Indians Diabetes Dataset contains 768 usable rows. The binary
outcome is `Outcome` (0 = no diabetes, 1 = diabetes). Logistic regression is
appropriate for modeling the probability of a binary outcome. Predictors:
Glucose, BMI, Age and Pregnancies. The observed prevalence is 34.90%.

## 2. Model and hypotheses

Log-odds model:

`log(p / (1 - p)) = beta0 + beta1*Glucose + beta2*BMI + beta3*Age + beta4*Pregnancies`

`p = 1 / (1 + exp(-linear_predictor))`

`Odds = p / (1 - p)`

`OR for a one-unit increase = exp(beta)`

`95% OR CI = [exp(beta_CI_lower), exp(beta_CI_upper)]`

A coefficient p-value tests H0: beta = 0 against a nonzero coefficient.
The full model summary is in `project13_logit_summary.txt`.

## 3. Coefficients, odds ratios and 95% CIs

| Variable | coef | OR | CI lower | CI upper | p-value |
| --- | --- | --- | --- | --- | --- |
| const | -8.3974 | 0.0002 | 0.0001 | 0.0008 | 8.940e-36 |
| Glucose | 0.0332 | 1.0338 | 1.0270 | 1.0406 | 5.885e-23 |
| BMI | 0.0829 | 1.0865 | 1.0575 | 1.1162 | 1.716e-09 |
| Age | 0.0129 | 1.0130 | 0.9952 | 1.0311 | 0.15318 |
| Pregnancies | 0.1135 | 1.1202 | 1.0536 | 1.1910 | 2.830e-04 |

Interpretation: OR > 1 denotes greater odds, OR < 1 lower odds, and OR = 1
no multiplicative change in odds, assuming other modeled variables are held
constant. These ORs are per *one unit* of the corresponding feature.

### Variable-specific clinical interpretations

- **Glucose:** OR=1.0338 (95% CI 1.0270 to 1.0406). A one-unit increase is associated with higher *odds* of diabetes, holding the other modeled predictors constant. This is not a causal statement.
- **BMI:** OR=1.0865 (95% CI 1.0575 to 1.1162). A one-unit increase is associated with higher *odds* of diabetes, holding the other modeled predictors constant. This is not a causal statement.
- **Age:** OR=1.0130 (95% CI 0.9952 to 1.0311). A one-unit increase is associated with higher *odds* of diabetes, holding the other modeled predictors constant. This is not a causal statement.
- **Pregnancies:** OR=1.1202 (95% CI 1.0536 to 1.1910). A one-unit increase is associated with higher *odds* of diabetes, holding the other modeled predictors constant. This is not a causal statement.

## 4. New patient prediction

Patient values: Glucose=150, BMI=32, Age=55, Pregnancies=3.

- Model-predicted diabetes probability: **0.5710 (57.10%)**
- Predicted odds: **1.3312**
- Class at threshold 0.5: **1**

This is a model estimate, not a medical diagnosis or an individually validated risk prediction.

## 5. Confusion matrix and ROC-AUC (in-sample)

At threshold 0.5:

| Actual \ Predicted | Predicted 0 | Predicted 1 |
| --- | --- | --- |
| Actual 0 | 440 | 60 |
| Actual 1 | 117 | 151 |

- True negatives: 440
- False positives: 60
- False negatives: 117
- True positives: 151
- Sensitivity/recall: 0.5634
- Specificity: 0.8800
- ROC-AUC: **0.8269**

Classification report:

```text
              precision    recall  f1-score   support

           0     0.7899    0.8800    0.8325       500
           1     0.7156    0.5634    0.6305       268

    accuracy                         0.7695       768
   macro avg     0.7528    0.7217    0.7315       768
weighted avg     0.7640    0.7695    0.7620       768
```

See `project13_roc_curve.png`. ROC-AUC measures discrimination/ranking across
thresholds (1 = perfect, 0.5 approximately random).

**Important:** The same rows were used to fit and evaluate the model, as the
assignment did not specify a holdout split. These are *in-sample* metrics and
are likely more optimistic than performance on unseen patients.

## 6. Required analytical questions

1. **Why logistic regression?** Diabetes Outcome is binary. Logistic
   regression maps a linear predictor to a valid probability between 0 and 1.
2. **How is the BMI odds ratio interpreted?** The per-unit BMI OR is
   **1.0865**. A one-unit BMI increase
   multiplies diabetes odds by this amount with the other predictors held constant.
3. **Odds ratio versus risk ratio:** OR compares odds `p/(1-p)`;
   RR compares probabilities/risks `p1/p0`. They are not generally equal,
   especially when outcomes are common.
4. **New patient probability:** **57.10%** for the specified values.
5. **Confusion matrix errors:** FP=60 are non-diabetic records predicted
   diabetic; FN=117 are diabetic records predicted non-diabetic.
6. **ROC-AUC:** It summarizes the model's capacity to rank positives above
   negatives over all classification thresholds, here **0.8269**.
7. **Why is 0.5 not always optimal?** The threshold trades off false negatives
   and false positives. Screening may prefer sensitivity, requiring a lower
   threshold depending on practical costs and validation results.
8. **Which predictor has the strongest association?** Raw ORs cannot be ranked
   fairly across features with different units. Comparing the magnitude of
   the log-odds change for a one-SD increase ranks **Glucose** highest in
   this model. This is a standardized *association*, not causal importance.

## 7. Standardized coefficient comparison

| Variable | Feature SD | OR per +1 SD | abs(beta * SD) |
| --- | --- | --- | --- |
| Glucose | 31.973 | 2.8907 | 1.0615 |
| BMI | 7.884 | 1.9230 | 0.6539 |
| Pregnancies | 3.370 | 1.4660 | 0.3825 |
| Age | 11.760 | 1.1637 | 0.1516 |

The standardized comparison uses `abs(beta * sample_SD)` for each predictor;
`OR_Per_1SD = exp(beta * sample_SD)`. It is scale-comparable but still cannot
prove causality or capture all forms of predictor importance.

## 8. Limitations and clinical interpretation

- This is an observational dataset; associations are not evidence of causation.
- No cleaning or replacement of clinically implausible zeros was required in
  this Project 13 assignment. Their presence may affect results.
- The project fit and evaluated the model on the same records (in-sample).
- Probabilities and ROC-AUC need independent testing and calibration analysis
  before any practical use.
- Predictors can be correlated; adjusted ORs refer to the specified model.

## 9. Conclusion

Logistic regression estimated diabetes probability from Glucose, BMI, Age and
Pregnancies. Coefficients were converted to ORs with 95% CIs; a new-patient
probability and classification metrics were produced. The model is an
educational exercise, not a validated clinical decision tool.
