# Project 14: Evaluating a Diabetes Classifier with Class Imbalance

## 1. Introduction and dataset

This project evaluates a class-weighted logistic classifier when the positive
class is less common than the negative class. We use the **Pima dataset for the
demo** (as permitted by the project sheet), **not the main BRFSS Kaggle
 dataset**. Total observations: **768**. Positive class prevalence:
**34.90%**. This is moderate class imbalance, not an extremely rare
condition.

## 2. Data preprocessing and class distribution

In Glucose, BloodPressure, SkinThickness, Insulin and BMI, zeros were treated
as invalid measurements and replaced by NaN (as instructed by the project):

| Feature | Zeros converted to NaN |
| --- | --- |
| Glucose | 5 |
| BloodPressure | 35 |
| SkinThickness | 227 |
| Insulin | 374 |
| BMI | 11 |

The model uses all eight Pima predictors. Splits are stratified:

| Split | N | Positive | Negative | Positive % |
| --- | --- | --- | --- | --- |
| Training | 460 | 160 | 300 | 34.78% |
| Validation | 154 | 54 | 100 | 35.06% |
| Test | 154 | 54 | 100 | 35.06% |

We used a 60/20/20 training/validation/test design. This includes the
train/test split required by the assignment, plus an independent validation
subset to select a candidate alert threshold **without inspecting test labels**.
The pipeline was:

`SimpleImputer(median) -> StandardScaler -> LogisticRegression(class_weight='balanced')`

Imputation medians and scaling parameters were learned on **training data only**
and reused for validation and test to prevent data leakage.

## 3. Confusion matrix at threshold 0.5 (held-out test)

| Actual \ Predicted | Predicted 0 | Predicted 1 |
| --- | --- | --- |
| Actual 0 | 75 | 25 |
| Actual 1 | 17 | 37 |

At 0.5:

- Sensitivity/recall = **0.6852**
- Specificity = **0.7500**
- Precision = **0.5968**
- F1-score = **0.6379**
- Accuracy = **0.7273**
- Balanced accuracy = **0.7176**
- False positives = **25**
- False negatives = **17**

Classification report:

```text
              precision    recall  f1-score   support

           0     0.8152    0.7500    0.7812       100
           1     0.5968    0.6852    0.6379        54

    accuracy                         0.7273       154
   macro avg     0.7060    0.7176    0.7096       154
weighted avg     0.7386    0.7273    0.7310       154
```

## 4. ROC, PR and Brier metrics

- ROC-AUC = **0.8156**
- PR-AUC (trapezoidal area) = **0.6763**
- Average Precision (AP; stepwise PR summary) = **0.6805**
- Test-class prevalence = **0.3506**
- Brier score = **0.1790** (lower is better; 0 is ideal)

Files: `project14_roc_curve.png`, `project14_pr_curve.png`.
ROC compares true-positive and false-positive rates across thresholds; PR
compares precision and recall and is often more informative when positives are
rare. Trapezoidal PR-AUC and Average Precision are related **but not identical**.

## 5. Threshold analysis (held-out test)

| Threshold | Sensitivity | Specificity | Precision | F1 | FP | FN |
| --- | --- | --- | --- | --- | --- | --- |
| 0.1 | 0.981 | 0.230 | 0.408 | 0.576 | 77 | 1 |
| 0.2 | 0.981 | 0.490 | 0.510 | 0.671 | 51 | 1 |
| 0.3 | 0.889 | 0.580 | 0.533 | 0.667 | 42 | 6 |
| 0.4 | 0.852 | 0.690 | 0.597 | 0.702 | 31 | 8 |
| 0.5 | 0.685 | 0.750 | 0.597 | 0.638 | 25 | 17 |
| 0.6 | 0.500 | 0.810 | 0.587 | 0.540 | 19 | 27 |
| 0.7 | 0.481 | 0.850 | 0.634 | 0.547 | 15 | 28 |

The table describes the tradeoff across thresholds 0.1 to 0.7. Typically,
lowering the cutoff raises sensitivity, while increasing false alarms and
reducing specificity. These are observed test-set results, not a guarantee for
other populations. See `project14_threshold_tradeoff.png`.

## 6. Calibration analysis

Calibration compares predicted probabilities with observed event frequencies.
`project14_calibration_curve.png` uses 10 uniform probability bins; empty bins
are omitted by the plot. The 45-degree line represents perfect calibration.
Brier score averages squared probability errors: `mean((p_hat - y)^2)`.

**Note:** Setting `class_weight='balanced'` can help class sensitivity but may
also distort raw probability calibration; a ROC-AUC score alone does not prove
well-calibrated probabilities. Independent calibration evaluation is necessary.

## 7. Illustrative screening threshold selection

**Selection used validation, not test:** At least 90% sensitivity on validation was achieved among the tested thresholds; among eligible thresholds, we selected the one with greatest validation specificity.

- Chosen candidate threshold: **0.2**
- Validation sensitivity at candidate: **0.9630**
- Validation specificity at candidate: **0.4500**

Independent test performance at candidate threshold:

| Actual \ Predicted | Predicted 0 | Predicted 1 |
| --- | --- | --- |
| Actual 0 | 49 | 51 |
| Actual 1 | 1 | 53 |

- Sensitivity = **0.9815**
- Specificity = **0.4900**
- Precision = **0.5096**
- FP=51; FN=1

The **90% sensitivity target is an educational demonstration**, not a clinical
guideline. Choosing a deployed clinical alarm threshold requires real costs of
FP/FN, subgroup analysis, prospective external validation, and medical review.

## 8. Answers to the required analytical questions

1. **Why can accuracy be misleading?** A model predicting every patient as
   non-diabetic would achieve **64.94% accuracy** on this test set
   while missing all positives. Accuracy hides false-negative cost; compare
   sensitivity, specificity, F1, balanced accuracy and PR metrics.
2. **ROC-AUC versus PR-AUC:** ROC-AUC summarizes rank discrimination using
   TPR/FPR; PR-AUC summarizes precision/recall, putting attention on the
   positive class and false-positive burden. Positive-class prevalence affects
   interpretation of PR results.
3. **How many FN at 0.5?** **17** on this test set.
4. **Threshold for screening?** Generally **lower** the threshold to detect
   more positives, acknowledging more false alarms.
5. **What does calibration show?** Whether events actually occur about as
   often as the probabilities predict (e.g. among predictions around 0.7,
   roughly 70% would be positive in a calibrated setting).
6. **Brier score:** The mean squared difference between predicted probabilities
   and binary outcomes. Here it is **0.1790**; lower is better.
7. **Why balanced class weights?** LogisticRegression gives relatively more
   weight to the less frequent class during fitting, potentially lowering missed
   positives at the cost of more false alarms and possibly poorer calibration.
8. **Suggested clinical-alert candidate:** **0.2**, chosen
   *only as an educational validation-based candidate* using a sensitivity
   objective, with test performance above. It is not a clinically approved cutoff.

## 9. Limitations and conclusion

- Pima demo results should not be labeled as results from BRFSS.
- Pima is a modest-sized observational dataset; class prevalence and feature
  distributions can differ elsewhere, harming generalizability.
- The 90% sensitivity target and validation threshold are illustrative.
- The classification metrics and calibration estimates have sampling uncertainty.
- Class weighting is not a substitute for calibrated, externally validated risk.

This project evaluated a classifier using confusion matrix metrics, ROC-AUC,
PR-AUC/AP, Brier score, calibration, and decision-threshold analysis. Accuracy
alone is insufficient for evaluating a healthcare screening model.
