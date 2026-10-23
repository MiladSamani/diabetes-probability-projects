"""Project 13: Logistic regression for diabetes (Pima dataset).

Run from the repository root:
    python project13/project13.py

Optional offline data file (9 columns, no header):
    python project13/project13.py --data /path/to/pima-indians-diabetes.data.csv

Reports, figures and tables are saved next to this script.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
)

BASE_DIR = Path(__file__).resolve().parent
DATA_URL = (
    "https://raw.githubusercontent.com/jbrownlee/Datasets/"
    "master/pima-indians-diabetes.data.csv"
)
COLUMNS = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin",
    "BMI", "DiabetesPedigreeFunction", "Age", "Outcome",
]
FEATURES = ["Glucose", "BMI", "Age", "Pregnancies"]
ALPHA = 0.05
THRESHOLD = 0.5
PATIENT = {"Glucose": 150, "BMI": 32, "Age": 55, "Pregnancies": 3}


def md_table(headers, rows):
    lines = [
        "| " + " | ".join(str(h) for h in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(str(v) for v in row) + " |" for row in rows)
    return "\n".join(lines)


def p_text(p):
    return f"{p:.3e}" if p < 0.001 else f"{p:.5f}"


def read_data(source):
    try:
        df = pd.read_csv(source, names=COLUMNS, header=None)
    except Exception as exc:
        raise SystemExit(
            "Could not load the Pima dataset. Check your internet connection, "
            "or download the CSV locally and run with --data /path/to/file.csv. "
            f"Details: {exc}"
        ) from exc
    if df.shape[1] != len(COLUMNS):
        raise ValueError(f"Expected {len(COLUMNS)} columns, got {df.shape[1]}")
    for name in COLUMNS:
        df[name] = pd.to_numeric(df[name], errors="raise")
    if not set(df["Outcome"].dropna().unique()).issubset({0, 1}):
        raise ValueError("Outcome must contain only 0 and 1")
    return df


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=DATA_URL, help="Local Pima CSV (without header) or URL")
    args = parser.parse_args()

    df = read_data(args.data)
    data = df[FEATURES + ["Outcome"]].dropna().copy()
    y = data["Outcome"].astype(int)
    X = sm.add_constant(data[FEATURES], has_constant="add")

    # The assignment does not prescribe a train/test split or special-zero cleaning.
    # Hence model fitting and class evaluation use the same rows; report this limitation.
    model = sm.Logit(y, X).fit(disp=False, maxiter=200)
    print("Rows used:", len(data))
    print("Diabetes prevalence:", f"{y.mean() * 100:.2f}%")
    print("\nLogit summary:\n", model.summary())

    (BASE_DIR / "project13_logit_summary.txt").write_text(
        model.summary().as_text(), encoding="utf-8"
    )

    # Odds ratio = exp(beta). CI limits are exponentiated on the same scale.
    ci = model.conf_int(alpha=ALPHA)
    estimates = pd.DataFrame({
        "Variable": model.params.index,
        "Coef": model.params.values,
        "OR": np.exp(model.params.values),
        "CI_Lower": np.exp(ci.iloc[:, 0].values),
        "CI_Upper": np.exp(ci.iloc[:, 1].values),
        "P_Value": model.pvalues.values,
    })
    estimates.to_csv(BASE_DIR / "project13_odds_ratios.csv", index=False)

    # Compare associations on a comparable scale: increase of one sample SD.
    sd_by_feature = data[FEATURES].std(ddof=1)
    std_log_odds = model.params[FEATURES] * sd_by_feature
    standardized = pd.DataFrame({
        "Variable": FEATURES,
        "SD": sd_by_feature.loc[FEATURES].values,
        "Log_Odds_Change_Per_1SD": std_log_odds.loc[FEATURES].values,
        "OR_Per_1SD": np.exp(std_log_odds.loc[FEATURES].values),
        "Abs_Log_Odds_Per_1SD": np.abs(std_log_odds.loc[FEATURES].values),
    }).sort_values("Abs_Log_Odds_Per_1SD", ascending=False)
    standardized.to_csv(BASE_DIR / "project13_standardized_effects.csv", index=False)
    strongest = str(standardized.iloc[0]["Variable"])

    # New patient: column order must exactly match fitted design matrix.
    new_patient = pd.DataFrame([PATIENT], columns=FEATURES)
    new_X = sm.add_constant(new_patient, has_constant="add").reindex(columns=X.columns)
    new_patient_prob = float(model.predict(new_X).iloc[0])

    # In-sample classification: useful for demonstrating metrics but optimistic.
    probabilities = np.asarray(model.predict(X))
    predicted = (probabilities >= THRESHOLD).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, predicted, labels=[0, 1]).ravel()
    auc_value = roc_auc_score(y, probabilities)
    report_cls = classification_report(y, predicted, labels=[0, 1], digits=4, zero_division=0)
    (BASE_DIR / "project13_classification_report.txt").write_text(
        report_cls, encoding="utf-8"
    )

    pd.DataFrame({
        "Patient_Index": data.index,
        "Outcome": y.values,
        "Predicted_Probability": probabilities,
        "Predicted_Class_0_5": predicted,
    }).to_csv(BASE_DIR / "project13_predictions.csv", index=False)

    fpr, tpr, _ = roc_curve(y, probabilities)
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.plot(fpr, tpr, linewidth=2, label=f"Logistic model (AUC={auc_value:.3f})")
    ax.plot([0, 1], [0, 1], linestyle="--", linewidth=1, label="Random ranking")
    ax.set(xlabel="False Positive Rate", ylabel="True Positive Rate",
           title="Project 13 - ROC Curve")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(BASE_DIR / "project13_roc_curve.png", dpi=150)
    plt.close(fig)

    or_rows = [
        [str(r.Variable), f"{r.Coef:.4f}", f"{r.OR:.4f}",
         f"{r.CI_Lower:.4f}", f"{r.CI_Upper:.4f}", p_text(r.P_Value)]
        for r in estimates.itertuples(index=False)
    ]
    or_table = md_table(
        ["Variable", "coef", "OR", "CI lower", "CI upper", "p-value"], or_rows
    )
    standardized_rows = [
        [str(r.Variable), f"{r.SD:.3f}", f"{r.OR_Per_1SD:.4f}",
         f"{r.Abs_Log_Odds_Per_1SD:.4f}"]
        for r in standardized.itertuples(index=False)
    ]
    standardized_table = md_table(
        ["Variable", "Feature SD", "OR per +1 SD", "abs(beta * SD)"],
        standardized_rows,
    )

    clinical_lines = []
    for f in FEATURES:
        row = estimates.loc[estimates["Variable"] == f].iloc[0]
        direction = "higher" if row["OR"] > 1 else "lower"
        clinical_lines.append(
            f"- **{f}:** OR={row['OR']:.4f} (95% CI "
            f"{row['CI_Lower']:.4f} to {row['CI_Upper']:.4f}). "
            f"A one-unit increase is associated with {direction} *odds* of diabetes, "
            "holding the other modeled predictors constant. This is not a causal statement."
        )

    # Explicit odds and odds-ratio example for the predicted patient's probability.
    patient_odds = new_patient_prob / (1 - new_patient_prob)
    patient_class = int(new_patient_prob >= THRESHOLD)

    report = f"""# Project 13: Logistic Regression for Diabetes Prediction

## 1. Introduction

The Pima Indians Diabetes Dataset contains {len(data)} usable rows. The binary
outcome is `Outcome` (0 = no diabetes, 1 = diabetes). Logistic regression is
appropriate for modeling the probability of a binary outcome. Predictors:
Glucose, BMI, Age and Pregnancies. The observed prevalence is {y.mean():.2%}.

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

{or_table}

Interpretation: OR > 1 denotes greater odds, OR < 1 lower odds, and OR = 1
no multiplicative change in odds, assuming other modeled variables are held
constant. These ORs are per *one unit* of the corresponding feature.

### Variable-specific clinical interpretations

{chr(10).join(clinical_lines)}

## 4. New patient prediction

Patient values: Glucose=150, BMI=32, Age=55, Pregnancies=3.

- Model-predicted diabetes probability: **{new_patient_prob:.4f} ({new_patient_prob:.2%})**
- Predicted odds: **{patient_odds:.4f}**
- Class at threshold 0.5: **{patient_class}**

This is a model estimate, not a medical diagnosis or an individually validated risk prediction.

## 5. Confusion matrix and ROC-AUC (in-sample)

At threshold 0.5:

{md_table(["Actual \\ Predicted", "Predicted 0", "Predicted 1"], [
    ["Actual 0", tn, fp], ["Actual 1", fn, tp]
])}

- True negatives: {tn}
- False positives: {fp}
- False negatives: {fn}
- True positives: {tp}
- Sensitivity/recall: {tp / (tp + fn):.4f}
- Specificity: {tn / (tn + fp):.4f}
- ROC-AUC: **{auc_value:.4f}**

Classification report:

```text
{report_cls.rstrip()}
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
   **{estimates.loc[estimates.Variable == 'BMI', 'OR'].iloc[0]:.4f}**. A one-unit BMI increase
   multiplies diabetes odds by this amount with the other predictors held constant.
3. **Odds ratio versus risk ratio:** OR compares odds `p/(1-p)`;
   RR compares probabilities/risks `p1/p0`. They are not generally equal,
   especially when outcomes are common.
4. **New patient probability:** **{new_patient_prob:.2%}** for the specified values.
5. **Confusion matrix errors:** FP={fp} are non-diabetic records predicted
   diabetic; FN={fn} are diabetic records predicted non-diabetic.
6. **ROC-AUC:** It summarizes the model's capacity to rank positives above
   negatives over all classification thresholds, here **{auc_value:.4f}**.
7. **Why is 0.5 not always optimal?** The threshold trades off false negatives
   and false positives. Screening may prefer sensitivity, requiring a lower
   threshold depending on practical costs and validation results.
8. **Which predictor has the strongest association?** Raw ORs cannot be ranked
   fairly across features with different units. Comparing the magnitude of
   the log-odds change for a one-SD increase ranks **{strongest}** highest in
   this model. This is a standardized *association*, not causal importance.

## 7. Standardized coefficient comparison

{standardized_table}

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
"""
    (BASE_DIR / "report13.md").write_text(report.strip() + "\n", encoding="utf-8")

    print("\nOdds-ratio results:\n", estimates.to_string(index=False))
    print(f"\nNew patient predicted probability: {new_patient_prob:.4f} ({new_patient_prob:.2%})")
    print(f"Confusion matrix at 0.5: TN={tn}, FP={fp}, FN={fn}, TP={tp}")
    print(f"In-sample ROC-AUC: {auc_value:.4f}")
    print("\nSaved: project13_odds_ratios.csv, project13_standardized_effects.csv,")
    print("       project13_predictions.csv, project13_logit_summary.txt,")
    print("       project13_classification_report.txt, project13_roc_curve.png, report13.md")


if __name__ == "__main__":
    main()
