"""Project 11 - Correlation and simple linear regression on Pima diabetes data.
Run: python project11.py
The script saves figures, numerical results, and report11.md beside itself.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Save figures without opening windows.
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import pearsonr, spearmanr, jarque_bera
from statsmodels.stats.diagnostic import het_breuschpagan


BASE_DIR = Path(__file__).resolve().parent
DATA_URL = (
    "https://raw.githubusercontent.com/jbrownlee/Datasets/"
    "master/pima-indians-diabetes.data.csv"
)
COLUMNS = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome",
]
ALPHA = 0.05
COOKS_THRESHOLD = 0.01  # Threshold specified in the assignment.


def as_p(value):
    return f"{value:.3e}" if value < 0.001 else f"{value:.5f}"


def strength(r):
    """Descriptive labels only; these cutoffs are not universal."""
    a = abs(r)
    if a < 0.2:
        return "very weak"
    if a < 0.4:
        return "weak"
    if a < 0.6:
        return "moderate"
    if a < 0.8:
        return "strong"
    return "very strong"


def markdown_table(headers, rows):
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    lines += ["| " + " | ".join(str(x) for x in row) + " |" for row in rows]
    return "\n".join(lines)


# 1. Load data. The assignment does not request cleaning zero values.
df = pd.read_csv(DATA_URL, names=COLUMNS)
data = df[["Age", "Glucose"]].dropna().copy()

age = data["Age"]
glucose = data["Glucose"]

# 2. Covariance, Pearson, and Spearman correlations.
covariance = age.cov(glucose)
pearson_r, pearson_p = pearsonr(age, glucose)
spearman_r, spearman_p = spearmanr(age, glucose)

# 3. Simple linear regression: Glucose = intercept + slope * Age.
X = sm.add_constant(data[["Age"]], has_constant="add")
model = sm.OLS(glucose, X).fit()

intercept = float(model.params["const"])
slope = float(model.params["Age"])
r_squared = float(model.rsquared)
ci = model.conf_int(alpha=ALPHA)
slope_lower, slope_upper = ci.loc["Age"].to_numpy()
intercept_lower, intercept_upper = ci.loc["const"].to_numpy()

print("Dataset size:", len(data))
print(f"Covariance (sample): {covariance:.4f}")
print(f"Pearson r: {pearson_r:.4f}; p-value: {as_p(pearson_p)}")
print(f"Spearman rho: {spearman_r:.4f}; p-value: {as_p(spearman_p)}")
print(f"Intercept: {intercept:.4f}")
print(f"Age slope: {slope:.4f}")
print(f"R-squared: {r_squared:.4f}")
print("\nOLS summary:\n")
print(model.summary())

(BASE_DIR / "project11_ols_summary.txt").write_text(
    model.summary().as_text(), encoding="utf-8"
)

# 4. Scatter plot and fitted regression line.
ordered = np.argsort(age.to_numpy())
plt.figure(figsize=(9, 6))
plt.scatter(age, glucose, alpha=0.5, s=24, label="Patients")
plt.plot(
    age.to_numpy()[ordered],
    model.fittedvalues.to_numpy()[ordered],
    linewidth=2,
    label="OLS fitted line",
)
plt.xlabel("Age (years)")
plt.ylabel("Glucose")
plt.title("Project 11: Age vs Glucose")
plt.legend()
plt.tight_layout()
plt.savefig(BASE_DIR / "scatter_age_glucose.png", dpi=150)
plt.close()

# 5. Residual diagnostics.
residuals = model.resid
fitted = model.fittedvalues

plt.figure(figsize=(9, 5))
plt.scatter(fitted, residuals, alpha=0.5, s=24)
plt.axhline(0, linestyle="--", color="black")
plt.xlabel("Fitted Glucose")
plt.ylabel("Residual (observed - fitted)")
plt.title("Residuals vs Fitted")
plt.tight_layout()
plt.savefig(BASE_DIR / "residuals_vs_fitted.png", dpi=150)
plt.close()

fig = sm.qqplot(residuals, line="s", fit=True)
fig.set_size_inches(7, 6)
fig.suptitle("Q-Q Plot of OLS Residuals")
fig.tight_layout()
fig.savefig(BASE_DIR / "qq_plot_residuals.png", dpi=150)
plt.close(fig)

# Statistical tests supplement the visual checks; they cannot replace them.
bp_stat, bp_p, _, _ = het_breuschpagan(residuals, model.model.exog)
jb_result = jarque_bera(residuals)
jb_stat = float(jb_result.statistic)
jb_p = float(jb_result.pvalue)

# 6. Influential observations using Cook's Distance.
cooks_d = model.get_influence().cooks_distance[0]
influential = cooks_d > COOKS_THRESHOLD
influential_count = int(np.sum(influential))

cooks_df = pd.DataFrame({
    "Row_Number": data.index.to_numpy() + 1,
    "Age": age.to_numpy(),
    "Glucose": glucose.to_numpy(),
    "Cook_Distance": cooks_d,
    "Above_0_01": influential,
})
cooks_df.to_csv(BASE_DIR / "project11_cooks_distance.csv", index=False)

plt.figure(figsize=(10, 5))
plt.scatter(cooks_df["Row_Number"], cooks_d, s=16)
plt.axhline(COOKS_THRESHOLD, color="black", linestyle="--", label="Cook's D = 0.01")
plt.xlabel("Row number (starting at 1)")
plt.ylabel("Cook's Distance")
plt.title("Influential Observations")
plt.legend()
plt.tight_layout()
plt.savefig(BASE_DIR / "cooks_distance.png", dpi=150)
plt.close()

results = pd.DataFrame([{
    "N": len(data),
    "Covariance": covariance,
    "Pearson_r": pearson_r,
    "Pearson_p": pearson_p,
    "Spearman_rho": spearman_r,
    "Spearman_p": spearman_p,
    "Intercept": intercept,
    "Intercept_CI_Lower": intercept_lower,
    "Intercept_CI_Upper": intercept_upper,
    "Age_Slope": slope,
    "Age_Slope_p": model.pvalues["Age"],
    "Age_Slope_CI_Lower": slope_lower,
    "Age_Slope_CI_Upper": slope_upper,
    "R_squared": r_squared,
    "Adjusted_R_squared": model.rsquared_adj,
    "Breusch_Pagan_p": bp_p,
    "Jarque_Bera_p": jb_p,
    "Cook_D_Above_0_01": influential_count,
    "Glucose_Zero_Count": int((glucose == 0).sum()),
}])
results.to_csv(BASE_DIR / "project11_results.csv", index=False)

# 7. Prepare report answers based on actual results.
direction = "positive" if pearson_r > 0 else "negative" if pearson_r < 0 else "zero"
association = (
    f"a {strength(pearson_r)} {direction} linear association"
    if pearson_r != 0 else "no linear association"
)
linear_significance = (
    "statistically significant" if model.pvalues["Age"] < ALPHA
    else "not statistically significant"
)
hetero_conclusion = (
    "evidence against constant residual variance (possible heteroscedasticity)"
    if bp_p < ALPHA else
    "no strong statistical evidence against constant residual variance"
)
normality_conclusion = (
    "evidence against normally distributed residuals"
    if jb_p < ALPHA else
    "insufficient evidence to reject residual normality"
)

best_rows = cooks_df.nlargest(5, "Cook_Distance")
top_cooks = markdown_table(
    ["Row", "Age", "Glucose", "Cook's D"],
    [
        [int(row.Row_Number), int(row.Age), f"{row.Glucose:.1f}", f"{row.Cook_Distance:.5f}"]
        for row in best_rows.itertuples(index=False)
    ],
)

report = f"""# Project 11: Correlation and Simple Linear Regression in Diabetes

## 1. Introduction

This project examines the relationship between Age (independent variable) and Glucose (dependent variable) in the Pima Indians Diabetes Dataset. The objectives are to measure covariance, Pearson and Spearman correlation, fit an ordinary least squares (OLS) regression, and examine model assumptions and influential observations.

## 2. Data and scatter plot

- Data source: {DATA_URL}
- Number of observations used: **{len(data)}**
- Predictor X: **Age**
- Response Y: **Glucose**
- Zero Glucose values retained in the raw data: **{int((glucose == 0).sum())}**

![Age vs Glucose](scatter_age_glucose.png)

The scatter plot shows individual Age/Glucose pairs and the OLS regression line. The line summarizes a **linear association**, not a causal relationship.

## 3. Covariance and correlation

{markdown_table(
    ["Statistic", "Value", "p-value"],
    [
        ["Sample covariance", f"{covariance:.4f}", "Not applicable"],
        ["Pearson r", f"{pearson_r:.4f}", as_p(pearson_p)],
        ["Spearman rho", f"{spearman_r:.4f}", as_p(spearman_p)],
    ],
)}

**Interpretation:** The Pearson coefficient indicates **{association}**. Pearson measures linear association between numerical variables, while Spearman measures monotonic association using ranks. Both can be statistically tested; neither proves causation. Descriptive strength labels are approximate conventions, not fixed clinical rules.

## 4. Simple linear regression (OLS)

The mathematical model is:

`Glucose_i = beta0 + beta1 * Age_i + error_i`

The fitted prediction equation is:

`Predicted Glucose = {intercept:.4f} + ({slope:.4f}) * Age`

{markdown_table(
    ["Measure", "Result"],
    [
        ["Intercept (beta0)", f"{intercept:.4f}"],
        ["95% CI, intercept", f"[{intercept_lower:.4f}, {intercept_upper:.4f}]"],
        ["Slope for Age (beta1)", f"{slope:.4f}"],
        ["95% CI, Age slope", f"[{slope_lower:.4f}, {slope_upper:.4f}]"],
        ["Age coefficient p-value", as_p(float(model.pvalues["Age"]))],
        ["R-squared", f"{r_squared:.4f} ({100*r_squared:.2f}%)"],
        ["Adjusted R-squared", f"{model.rsquared_adj:.4f}"],
    ],
)}

**Slope interpretation:** An additional year of age is associated with an estimated **{slope:.4f}-unit** change in Glucose on average in this simple linear model. The Age slope is **{linear_significance}** at alpha = 0.05.

**R-squared interpretation:** Age explains approximately **{100*r_squared:.2f}%** of the variation in Glucose *within this sample and linear model*. R-squared is not the probability a person has diabetes, does not establish causality, and does not measure predictive accuracy on new data by itself.

The complete statsmodels OLS output is saved in `project11_ols_summary.txt`.

## 5. Residual diagnostics

A residual is `Observed Glucose - Predicted Glucose`. A useful residual-versus-fitted plot has no clear systematic curve or changing spread; a funnel may suggest non-constant variance, and a curve may suggest nonlinearity.

![Residuals vs Fitted](residuals_vs_fitted.png)

Breusch-Pagan p-value: **{as_p(float(bp_p))}**. This provides **{hetero_conclusion}** at alpha = 0.05. The residual plot should also be inspected visually.

![Q-Q Plot](qq_plot_residuals.png)

A Q-Q plot close to its reference line is consistent with approximately normal residuals. Jarque-Bera p-value: **{as_p(jb_p)}**, providing **{normality_conclusion}** at alpha = 0.05. With a large sample, even relatively small departures can be detected. Statistical tests and visual checks should be interpreted together.

## 6. Cook's Distance and influential observations

Cook's Distance describes how much the fitted regression may change if one observation is removed.

The assignment-defined flag is `Cook's D > 0.01`.

- Number above 0.01: **{influential_count}**
- Largest Cook's D: **{np.max(cooks_d):.5f}**

Five largest values:

{top_cooks}

![Cook's Distance](cooks_distance.png)

Flagged observations require investigation; they should not automatically be removed. The complete table is saved as `project11_cooks_distance.csv`.

## 7. Answers to analytical questions

1. **Direction and strength:** Age and Glucose show {association} (Pearson r = {pearson_r:.4f}).
2. **Pearson vs Spearman:** Pearson quantifies a linear relationship using original values; Spearman quantifies a monotonic relationship using ranked values.
3. **Slope:** Each additional year of Age is associated with an average change of {slope:.4f} Glucose units according to this simple model.
4. **R-squared:** R-squared = {r_squared:.4f} is the proportion of sample Glucose variation explained by a linear Age predictor; it does not prove causation or guarantee good prediction for new patients.
5. **Causality:** A statistically significant Age coefficient does **not** prove Age causes Glucose to change. This is an observational analysis.
6. **Residual plot:** It is used to look for curvature, unequal spread (heteroscedasticity), outliers, and other structure. Here, the Breusch-Pagan test gives p = {as_p(float(bp_p))}; visually inspect `residuals_vs_fitted.png` before making a stronger claim.
7. **Normality:** The Q-Q plot and Jarque-Bera test assess residual normality. Jarque-Bera p = {as_p(jb_p)}; this indicates {normality_conclusion}, rather than guaranteeing perfect normality/non-normality.
8. **Influential observations:** **{influential_count}** observations have Cook's D > 0.01.

## 8. Clinical interpretation and limitations

These associations describe the observed dataset, not a treatment effect or a causal effect of aging. Other factors (BMI, pregnancy history, medications, lifestyle and selection effects) may contribute to Glucose values. The analysis uses the assignment's raw data, including **{int((glucose == 0).sum())}** Glucose entries equal to zero, which are clinically suspicious and can affect coefficients and diagnostics. No rule for handling them was supplied by the assignment, so they were not silently changed.

Observations may not represent all populations, and OLS assumes an adequately specified mean relationship and appropriate error conditions. Out-of-sample predictive ability was not evaluated.

## 9. Conclusion

The project measured correlation between Age and Glucose, fitted a simple OLS regression, reported a 95% confidence interval for the slope and R-squared, examined residual diagnostics, and counted observations with Cook's D > 0.01. Results indicate **{association}**, with important limitations for clinical and causal interpretation.
"""

(BASE_DIR / "report11.md").write_text(report.strip() + "\n", encoding="utf-8")

print(f"\nCook's D > 0.01: {influential_count}")
print("Breusch-Pagan p:", as_p(float(bp_p)))
print("Jarque-Bera p:", as_p(jb_p))
print("\nSaved: project11_results.csv, project11_cooks_distance.csv,")
print("project11_ols_summary.txt, 4 PNG figures, report11.md")
