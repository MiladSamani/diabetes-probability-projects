"""Project 14: Evaluation of a class-weighted diabetes classifier.

Uses Pima for the demo, as allowed by the assignment. The larger BRFSS Kaggle
file is a distinct dataset; this script does not claim to analyze BRFSS.

Run:
    python project14/project14.py
Optional offline data file (9 columns, no header):
    python project14/project14.py --data /path/to/pima-indians-diabetes.data.csv

Reports, plots, tables and a classification report are saved beside this script.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, average_precision_score, balanced_accuracy_score,
    brier_score_loss, classification_report, confusion_matrix,
    f1_score, precision_recall_curve, precision_score, recall_score,
    roc_auc_score, roc_curve, auc,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parent
DATA_URL = (
    "https://raw.githubusercontent.com/jbrownlee/Datasets/"
    "master/pima-indians-diabetes.data.csv"
)
COLUMNS = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin",
    "BMI", "DiabetesPedigreeFunction", "Age", "Outcome",
]
FEATURES = [c for c in COLUMNS if c != "Outcome"]
ZERO_AS_MISSING = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
THRESHOLDS = [round(x, 1) for x in np.arange(0.1, 0.71, 0.1)]
SEED = 42
SCREENING_SENSITIVITY_TARGET = 0.90  # educational decision objective


def md_table(headers, rows):
    lines = [
        "| " + " | ".join(str(h) for h in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(str(v) for v in row) + " |" for row in rows)
    return "\n".join(lines)


def read_data(source):
    try:
        df = pd.read_csv(source, names=COLUMNS, header=None)
    except Exception as exc:
        raise SystemExit(
            "Could not load the Pima dataset. Check the connection, or download "
            "the CSV and pass --data /path/to/file.csv. "
            f"Details: {exc}"
        ) from exc
    if df.shape[1] != len(COLUMNS):
        raise ValueError(f"Expected {len(COLUMNS)} columns, got {df.shape[1]}")
    for col in COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="raise")
    if not set(df["Outcome"].dropna().unique()).issubset({0, 1}):
        raise ValueError("Outcome must contain only 0 and 1")
    return df


def classification_metrics(y_true, probs, threshold):
    pred = (np.asarray(probs) >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, pred, labels=[0, 1]).ravel()
    return {
        "Threshold": float(threshold),
        "TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp),
        "Sensitivity": float(recall_score(y_true, pred, zero_division=0)),
        "Specificity": float(tn / (tn + fp)) if (tn + fp) else float("nan"),
        "Precision": float(precision_score(y_true, pred, zero_division=0)),
        "F1": float(f1_score(y_true, pred, zero_division=0)),
        "Accuracy": float(accuracy_score(y_true, pred)),
        "Balanced_Accuracy": float(balanced_accuracy_score(y_true, pred)),
    }


def threshold_table(rows):
    return md_table(
        ["Threshold", "Sensitivity", "Specificity", "Precision", "F1", "FP", "FN"],
        [[f"{r['Threshold']:.1f}", f"{r['Sensitivity']:.3f}",
          f"{r['Specificity']:.3f}", f"{r['Precision']:.3f}",
          f"{r['F1']:.3f}", r["FP"], r["FN"]] for r in rows]
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=DATA_URL, help="Local Pima CSV (without header) or URL")
    args = parser.parse_args()

    df = read_data(args.data)
    data = df[FEATURES + ["Outcome"]].dropna(subset=["Outcome"]).copy()
    data[ZERO_AS_MISSING] = data[ZERO_AS_MISSING].replace(0, np.nan)
    y = data["Outcome"].astype(int)
    X = data[FEATURES]
    zero_counts = (df[ZERO_AS_MISSING] == 0).sum()

    # Stratified splits. Validation is separated from the test set so that
    # threshold selection does not use test labels (60% / 20% / 20%).
    X_trainval, X_test, y_trainval, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=SEED
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_trainval, y_trainval, test_size=0.25,
        stratify=y_trainval, random_state=SEED
    )

    # Median is learned ONLY from the training set inside Pipeline.fit().
    pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(
            class_weight="balanced", max_iter=1000, random_state=SEED
        )),
    ])
    pipe.fit(X_train, y_train)
    val_prob = pipe.predict_proba(X_val)[:, 1]
    test_prob = pipe.predict_proba(X_test)[:, 1]

    # The clinical threshold is NOT learned from the test set. We choose the
    # highest threshold meeting an illustrative sensitivity objective on validation.
    val_rows = [classification_metrics(y_val, val_prob, t) for t in THRESHOLDS]
    feasible = [r for r in val_rows if r["Sensitivity"] >= SCREENING_SENSITIVITY_TARGET]
    if feasible:
        choice = max(feasible, key=lambda r: (r["Specificity"], r["Threshold"]))
        selection_note = (
            f"At least {SCREENING_SENSITIVITY_TARGET:.0%} sensitivity on validation "
            "was achieved among the tested thresholds; among eligible thresholds, "
            "we selected the one with greatest validation specificity."
        )
    else:
        choice = max(val_rows, key=lambda r: (r["Sensitivity"], r["Specificity"]))
        selection_note = (
            f"None of the tested thresholds met the illustrative "
            f"{SCREENING_SENSITIVITY_TARGET:.0%} sensitivity target on validation. "
            "The candidate with highest validation sensitivity was selected for "
            "demonstration; it is not a clinically validated alarm threshold."
        )
    selected_threshold = float(choice["Threshold"])

    test_rows = [classification_metrics(y_test, test_prob, t) for t in THRESHOLDS]
    metrics_05 = classification_metrics(y_test, test_prob, 0.5)
    metrics_selected = classification_metrics(y_test, test_prob, selected_threshold)

    roc = roc_auc_score(y_test, test_prob)
    ap = average_precision_score(y_test, test_prob)
    precision_curve, recall_curve, _ = precision_recall_curve(y_test, test_prob)
    pr_auc = auc(recall_curve, precision_curve)
    brier = brier_score_loss(y_test, test_prob)

    pd.DataFrame(val_rows).to_csv(BASE_DIR / "project14_validation_thresholds.csv", index=False)
    pd.DataFrame(test_rows).to_csv(BASE_DIR / "project14_threshold_analysis.csv", index=False)
    pd.DataFrame([
        {"Metric": "ROC_AUC", "Value": roc},
        {"Metric": "PR_AUC_trapezoidal", "Value": pr_auc},
        {"Metric": "Average_Precision_AP", "Value": ap},
        {"Metric": "Brier_Score", "Value": brier},
        {"Metric": "Test_Prevalence", "Value": y_test.mean()},
        {"Metric": "Majority_Class_Accuracy", "Value": 1 - y_test.mean()},
        {"Metric": "Validation_Selected_Threshold", "Value": selected_threshold},
    ]).to_csv(BASE_DIR / "project14_summary_metrics.csv", index=False)
    pd.DataFrame({
        "Outcome": y_test.to_numpy(),
        "Predicted_Probability": test_prob,
        "Predicted_Class_0_5": (test_prob >= 0.5).astype(int),
        "Predicted_Class_Selected": (test_prob >= selected_threshold).astype(int),
    }, index=X_test.index).to_csv(BASE_DIR / "project14_test_predictions.csv", index_label="Original_Row_Index")

    cls_report = classification_report(
        y_test, (test_prob >= 0.5).astype(int),
        labels=[0, 1], digits=4, zero_division=0
    )
    (BASE_DIR / "project14_classification_report.txt").write_text(
        cls_report, encoding="utf-8"
    )

    # ROC curve on held-out test predictions.
    fpr, tpr, _ = roc_curve(y_test, test_prob)
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.plot(fpr, tpr, linewidth=2, label=f"ROC-AUC={roc:.3f}")
    ax.plot([0, 1], [0, 1], "--", linewidth=1, label="Random ranking")
    ax.set(title="Project 14 - ROC curve (test)", xlabel="False Positive Rate",
           ylabel="True Positive Rate")
    ax.grid(alpha=0.25)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(BASE_DIR / "project14_roc_curve.png", dpi=150)
    plt.close(fig)

    # Area under PR curve by trapezoids differs slightly from Average Precision.
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.plot(recall_curve, precision_curve, linewidth=2,
            label=f"PR-AUC={pr_auc:.3f}; AP={ap:.3f}")
    ax.axhline(float(y_test.mean()), linestyle="--", linewidth=1,
               label=f"Prevalence baseline={y_test.mean():.3f}")
    ax.set(title="Project 14 - Precision-Recall curve (test)",
           xlabel="Recall (Sensitivity)", ylabel="Precision", xlim=(0, 1), ylim=(0, 1.05))
    ax.grid(alpha=0.25)
    ax.legend(loc="lower left")
    fig.tight_layout()
    fig.savefig(BASE_DIR / "project14_pr_curve.png", dpi=150)
    plt.close(fig)

    # Calibration: ten uniform-width probability bins (some may be empty).
    frac_pos, mean_pred = calibration_curve(
        y_test, test_prob, n_bins=10, strategy="uniform"
    )
    calib_bins = pd.DataFrame({
        "Mean_Predicted_Probability": mean_pred,
        "Observed_Fraction_Positive": frac_pos,
    })
    calib_bins.to_csv(BASE_DIR / "project14_calibration_bins.csv", index=False)
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot([0, 1], [0, 1], "--", linewidth=1, label="Perfect calibration")
    ax.plot(mean_pred, frac_pos, marker="o", linewidth=2, label="Weighted logistic model")
    ax.set(title="Project 14 - Calibration curve (10 bins; test)",
           xlabel="Mean predicted probability", ylabel="Observed event fraction",
           xlim=(0, 1), ylim=(0, 1))
    ax.legend(loc="upper left")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(BASE_DIR / "project14_calibration_curve.png", dpi=150)
    plt.close(fig)

    # Threshold chart is a complement to the required threshold table.
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.plot(THRESHOLDS, [r["Sensitivity"] for r in test_rows], marker="o", label="Sensitivity")
    ax.plot(THRESHOLDS, [r["Specificity"] for r in test_rows], marker="o", label="Specificity")
    ax.plot(THRESHOLDS, [r["Precision"] for r in test_rows], marker="o", label="Precision")
    ax.axvline(selected_threshold, linestyle="--", linewidth=1,
               label=f"Candidate threshold={selected_threshold:.1f}")
    ax.set(title="Project 14 - Threshold comparison (test)",
           xlabel="Decision threshold", ylabel="Metric", ylim=(0, 1.05))
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(BASE_DIR / "project14_threshold_tradeoff.png", dpi=150)
    plt.close(fig)

    # Expose key results and report all eight assignment questions.
    def cm_table(m):
        return md_table(["Actual \\ Predicted", "Predicted 0", "Predicted 1"], [
            ["Actual 0", m["TN"], m["FP"]],
            ["Actual 1", m["FN"], m["TP"]],
        ])

    size_table = md_table(["Split", "N", "Positive", "Negative", "Positive %"], [
        ["Training", len(y_train), int(y_train.sum()), int((1 - y_train).sum()), f"{y_train.mean():.2%}"],
        ["Validation", len(y_val), int(y_val.sum()), int((1 - y_val).sum()), f"{y_val.mean():.2%}"],
        ["Test", len(y_test), int(y_test.sum()), int((1 - y_test).sum()), f"{y_test.mean():.2%}"],
    ])
    zero_table = md_table(["Feature", "Zeros converted to NaN"], [
        [name, int(zero_counts[name])] for name in ZERO_AS_MISSING
    ])

    report = f"""# Project 14: Evaluating a Diabetes Classifier with Class Imbalance

## 1. Introduction and dataset

This project evaluates a class-weighted logistic classifier when the positive
class is less common than the negative class. We use the **Pima dataset for the
demo** (as permitted by the project sheet), **not the main BRFSS Kaggle
 dataset**. Total observations: **{len(data)}**. Positive class prevalence:
**{y.mean():.2%}**. This is moderate class imbalance, not an extremely rare
condition.

## 2. Data preprocessing and class distribution

In Glucose, BloodPressure, SkinThickness, Insulin and BMI, zeros were treated
as invalid measurements and replaced by NaN (as instructed by the project):

{zero_table}

The model uses all eight Pima predictors. Splits are stratified:

{size_table}

We used a 60/20/20 training/validation/test design. This includes the
train/test split required by the assignment, plus an independent validation
subset to select a candidate alert threshold **without inspecting test labels**.
The pipeline was:

`SimpleImputer(median) -> StandardScaler -> LogisticRegression(class_weight='balanced')`

Imputation medians and scaling parameters were learned on **training data only**
and reused for validation and test to prevent data leakage.

## 3. Confusion matrix at threshold 0.5 (held-out test)

{cm_table(metrics_05)}

At 0.5:

- Sensitivity/recall = **{metrics_05['Sensitivity']:.4f}**
- Specificity = **{metrics_05['Specificity']:.4f}**
- Precision = **{metrics_05['Precision']:.4f}**
- F1-score = **{metrics_05['F1']:.4f}**
- Accuracy = **{metrics_05['Accuracy']:.4f}**
- Balanced accuracy = **{metrics_05['Balanced_Accuracy']:.4f}**
- False positives = **{metrics_05['FP']}**
- False negatives = **{metrics_05['FN']}**

Classification report:

```text
{cls_report.rstrip()}
```

## 4. ROC, PR and Brier metrics

- ROC-AUC = **{roc:.4f}**
- PR-AUC (trapezoidal area) = **{pr_auc:.4f}**
- Average Precision (AP; stepwise PR summary) = **{ap:.4f}**
- Test-class prevalence = **{y_test.mean():.4f}**
- Brier score = **{brier:.4f}** (lower is better; 0 is ideal)

Files: `project14_roc_curve.png`, `project14_pr_curve.png`.
ROC compares true-positive and false-positive rates across thresholds; PR
compares precision and recall and is often more informative when positives are
rare. Trapezoidal PR-AUC and Average Precision are related **but not identical**.

## 5. Threshold analysis (held-out test)

{threshold_table(test_rows)}

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

**Selection used validation, not test:** {selection_note}

- Chosen candidate threshold: **{selected_threshold:.1f}**
- Validation sensitivity at candidate: **{choice['Sensitivity']:.4f}**
- Validation specificity at candidate: **{choice['Specificity']:.4f}**

Independent test performance at candidate threshold:

{cm_table(metrics_selected)}

- Sensitivity = **{metrics_selected['Sensitivity']:.4f}**
- Specificity = **{metrics_selected['Specificity']:.4f}**
- Precision = **{metrics_selected['Precision']:.4f}**
- FP={metrics_selected['FP']}; FN={metrics_selected['FN']}

The **90% sensitivity target is an educational demonstration**, not a clinical
guideline. Choosing a deployed clinical alarm threshold requires real costs of
FP/FN, subgroup analysis, prospective external validation, and medical review.

## 8. Answers to the required analytical questions

1. **Why can accuracy be misleading?** A model predicting every patient as
   non-diabetic would achieve **{1 - y_test.mean():.2%} accuracy** on this test set
   while missing all positives. Accuracy hides false-negative cost; compare
   sensitivity, specificity, F1, balanced accuracy and PR metrics.
2. **ROC-AUC versus PR-AUC:** ROC-AUC summarizes rank discrimination using
   TPR/FPR; PR-AUC summarizes precision/recall, putting attention on the
   positive class and false-positive burden. Positive-class prevalence affects
   interpretation of PR results.
3. **How many FN at 0.5?** **{metrics_05['FN']}** on this test set.
4. **Threshold for screening?** Generally **lower** the threshold to detect
   more positives, acknowledging more false alarms.
5. **What does calibration show?** Whether events actually occur about as
   often as the probabilities predict (e.g. among predictions around 0.7,
   roughly 70% would be positive in a calibrated setting).
6. **Brier score:** The mean squared difference between predicted probabilities
   and binary outcomes. Here it is **{brier:.4f}**; lower is better.
7. **Why balanced class weights?** LogisticRegression gives relatively more
   weight to the less frequent class during fitting, potentially lowering missed
   positives at the cost of more false alarms and possibly poorer calibration.
8. **Suggested clinical-alert candidate:** **{selected_threshold:.1f}**, chosen
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
"""
    (BASE_DIR / "report14.md").write_text(report.strip() + "\n", encoding="utf-8")

    print("Dataset:", len(y), "rows; positive prevalence:", f"{y.mean():.2%}")
    print("Train/Validation/Test:", len(y_train), len(y_val), len(y_test))
    print("\nAt threshold 0.5:",
          f"TN={metrics_05['TN']} FP={metrics_05['FP']} FN={metrics_05['FN']} TP={metrics_05['TP']}")
    print(f"Accuracy={metrics_05['Accuracy']:.4f}; sensitivity={metrics_05['Sensitivity']:.4f}; "
          f"specificity={metrics_05['Specificity']:.4f}; precision={metrics_05['Precision']:.4f}")
    print(f"ROC-AUC={roc:.4f}; PR-AUC={pr_auc:.4f}; AP={ap:.4f}; Brier={brier:.4f}")
    print(f"Validation-selected candidate threshold: {selected_threshold:.1f}")
    print("\nTest threshold table:\n", pd.DataFrame(test_rows).to_string(index=False))
    print("\nSaved: project14_threshold_analysis.csv, project14_validation_thresholds.csv,")
    print("       project14_summary_metrics.csv, project14_test_predictions.csv,")
    print("       project14_calibration_bins.csv, project14_classification_report.txt,")
    print("       4 PNG figures, report14.md")


if __name__ == "__main__":
    main()
