"""Project 12 - Multiple regression, VIF, and Age x BMI interaction.
Run: python project12.py
Creates full reports, results tables, and figures in this directory.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import jarque_bera
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor


BASE_DIR = Path(__file__).resolve().parent
DATA_URL = (
    "https://raw.githubusercontent.com/jbrownlee/Datasets/"
    "master/pima-indians-diabetes.data.csv"
)
COLUMNS = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome",
]
PREDICTORS = ["Age", "BMI", "Pregnancies", "BloodPressure"]
ALPHA = 0.05


def as_p(p):
    return f"{p:.3e}" if p < 0.001 else f"{p:.5f}"


def markdown_table(headers, rows):
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    lines += ["| " + " | ".join(str(value) for value in row) + " |" for row in rows]
    return "\n".join(lines)


def design_matrix(frame, features):
    return sm.add_constant(frame[features], has_constant="add")


# 1. Load data; use the same complete cases for a fair model comparison.
df = pd.read_csv(DATA_URL, names=COLUMNS)
data = df[["Glucose", *PREDICTORS]].dropna().copy()
y = data["Glucose"]

# 2. Simple regression: Glucose ~ Age.
X_simple = design_matrix(data, ["Age"])
simple_model = sm.OLS(y, X_simple).fit()

# 3. Multiple regression: Glucose ~ Age + BMI + Pregnancies + BloodPressure.
X_multiple = design_matrix(data, PREDICTORS)
multiple_model = sm.OLS(y, X_multiple).fit()

# 4. Variance Inflation Factor (VIF) for each predictor (not intercept).
vif_rows = []
for index, feature in enumerate(X_multiple.columns):
    if feature == "const":
        continue
    vif_rows.append({
        "Variable": feature,
        "VIF": float(variance_inflation_factor(X_multiple.to_numpy(), index)),
    })
vif_df = pd.DataFrame(vif_rows)
vif_df.to_csv(BASE_DIR / "project12_vif.csv", index=False)

# 5. Age x BMI interaction (raw product, as specified by the assignment).
data["Age_BMI"] = data["Age"] * data["BMI"]
interaction_features = [*PREDICTORS, "Age_BMI"]
X_interaction = design_matrix(data, interaction_features)
interaction_model = sm.OLS(y, X_interaction).fit()

age_simple = float(simple_model.params["Age"])
age_multiple = float(multiple_model.params["Age"])
age_change = age_multiple - age_simple
age_percent_change = (
    100 * age_change / abs(age_simple) if not np.isclose(age_simple, 0) else float("nan")
)
interaction_coefficient = float(interaction_model.params["Age_BMI"])
interaction_p = float(interaction_model.pvalues["Age_BMI"])

# 6. Save model summaries and numeric tables.
models = {
    "Simple": simple_model,
    "Multiple": multiple_model,
    "Interaction": interaction_model,
}
for title, fitted_model in models.items():
    (BASE_DIR / f"project12_{title.lower()}_summary.txt").write_text(
        fitted_model.summary().as_text(), encoding="utf-8"
    )

comparison_rows = []
coefficient_rows = []
for name, fitted_model in models.items():
    age_ci = fitted_model.conf_int(alpha=ALPHA).loc["Age"]
    comparison_rows.append({
        "Model": name,
        "N": int(fitted_model.nobs),
        "Age_Coefficient": fitted_model.params["Age"],
        "Age_CI_Lower": age_ci.iloc[0],
        "Age_CI_Upper": age_ci.iloc[1],
        "Age_p": fitted_model.pvalues["Age"],
        "R_Squared": fitted_model.rsquared,
        "Adjusted_R_Squared": fitted_model.rsquared_adj,
        "AIC": fitted_model.aic,
    })
    all_ci = fitted_model.conf_int(alpha=ALPHA)
    for feature in fitted_model.params.index:
        coefficient_rows.append({
            "Model": name,
            "Variable": feature,
            "Coefficient": fitted_model.params[feature],
            "SE": fitted_model.bse[feature],
            "p_value": fitted_model.pvalues[feature],
            "CI_Lower": all_ci.loc[feature].iloc[0],
            "CI_Upper": all_ci.loc[feature].iloc[1],
        })

comparison_df = pd.DataFrame(comparison_rows)
coefficients_df = pd.DataFrame(coefficient_rows)
comparison_df.to_csv(BASE_DIR / "project12_model_comparison.csv", index=False)
coefficients_df.to_csv(BASE_DIR / "project12_coefficients.csv", index=False)

# 7. Residual diagnostics for the multiple regression model.
residuals = multiple_model.resid
fitted = multiple_model.fittedvalues

plt.figure(figsize=(9, 5))
plt.scatter(fitted, residuals, alpha=0.5, s=24)
plt.axhline(0, linestyle="--", color="black")
plt.xlabel("Fitted Glucose")
plt.ylabel("Residual (observed - fitted)")
plt.title("Multiple Regression: Residuals vs Fitted")
plt.tight_layout()
plt.savefig(BASE_DIR / "project12_residuals_vs_fitted.png", dpi=150)
plt.close()

fig = sm.qqplot(residuals, fit=True, line="s")
fig.set_size_inches(7, 6)
fig.suptitle("Multiple Regression: Residual Q-Q Plot")
fig.tight_layout()
fig.savefig(BASE_DIR / "project12_qq_plot.png", dpi=150)
plt.close(fig)

bp_stat, bp_p, _, _ = het_breuschpagan(residuals, multiple_model.model.exog)
jb_result = jarque_bera(residuals)
jb_p = float(jb_result.pvalue)

# 8. Interaction curves for BMI=20, 30, 40.
# Pregnancies and BloodPressure are fixed at their dataset means.
pregnancies_fixed = float(data["Pregnancies"].mean())
blood_pressure_fixed = float(data["BloodPressure"].mean())
age_grid = np.linspace(data["Age"].min(), data["Age"].max(), 150)

plt.figure(figsize=(9, 6))
for bmi_value in (20, 30, 40):
    new_data = pd.DataFrame({
        "Age": age_grid,
        "BMI": float(bmi_value),
        "Pregnancies": pregnancies_fixed,
        "BloodPressure": blood_pressure_fixed,
    })
    new_data["Age_BMI"] = new_data["Age"] * new_data["BMI"]
    X_new = design_matrix(new_data, interaction_features)
    predictions = interaction_model.predict(X_new[interaction_model.model.exog_names])
    plt.plot(age_grid, predictions, label=f"BMI = {bmi_value}")

plt.xlabel("Age (years)")
plt.ylabel("Predicted Glucose")
plt.title("Age x BMI Interaction in Predicted Glucose")
plt.legend()
plt.tight_layout()
plt.savefig(BASE_DIR / "project12_interaction_plot.png", dpi=150)
plt.close()

# 9. Model comparison plot for Age, holding other variables at their means.
plot_frame = pd.DataFrame({
    "Age": age_grid,
    "BMI": data["BMI"].mean(),
    "Pregnancies": pregnancies_fixed,
    "BloodPressure": blood_pressure_fixed,
})
simple_predictions = simple_model.predict(design_matrix(plot_frame, ["Age"]))
multiple_predictions = multiple_model.predict(design_matrix(plot_frame, PREDICTORS))

plt.figure(figsize=(9, 6))
plt.plot(age_grid, simple_predictions, label="Simple: Age only")
plt.plot(age_grid, multiple_predictions, label="Multiple: adjusted for BMI, Pregnancies, BP")
plt.xlabel("Age (years)")
plt.ylabel("Predicted Glucose")
plt.title("Simple vs Multiple Regression")
plt.legend()
plt.tight_layout()
plt.savefig(BASE_DIR / "project12_simple_vs_multiple.png", dpi=150)
plt.close()

# 10. Print key results.
print("Dataset size:", len(data))
print("\nSimple regression summary:\n")
print(simple_model.summary())
print("\nMultiple regression summary:\n")
print(multiple_model.summary())
print("\nInteraction regression summary:\n")
print(interaction_model.summary())
print("\nModel comparison:\n", comparison_df.to_string(index=False))
print("\nVIF:\n", vif_df.to_string(index=False))
print(f"\nAge coefficient change: {age_simple:.4f} -> {age_multiple:.4f} ({age_change:+.4f})")
print(f"Age x BMI coefficient: {interaction_coefficient:.6f}, p = {as_p(interaction_p)}")
print(f"Breusch-Pagan p = {as_p(float(bp_p))}; Jarque-Bera p = {as_p(jb_p)}")

# 11. Automatically write report with results from this run.
multiple_coef = multiple_model.params
multi_ci = multiple_model.conf_int(alpha=ALPHA)

main_coef_table = markdown_table(
    ["Term", "Coefficient", "95% CI", "p-value"],
    [
        [feature, f"{multiple_coef[feature]:.4f}",
         f"[{multi_ci.loc[feature].iloc[0]:.4f}, {multi_ci.loc[feature].iloc[1]:.4f}]",
         as_p(float(multiple_model.pvalues[feature]))]
        for feature in multiple_model.params.index
    ],
)

model_table = markdown_table(
    ["Model", "Age slope", "R-squared", "Adj. R-squared"],
    [
        [name, f"{fitted_model.params['Age']:.4f}",
         f"{fitted_model.rsquared:.4f}", f"{fitted_model.rsquared_adj:.4f}"]
        for name, fitted_model in models.items()
    ],
)

vif_table = markdown_table(
    ["Predictor", "VIF"],
    [[row.Variable, f"{row.VIF:.4f}"] for row in vif_df.itertuples(index=False)],
)

max_vif = float(vif_df["VIF"].max())
if max_vif >= 10:
    vif_conclusion = "At least one VIF is at or above 10; severe multicollinearity should be investigated."
elif max_vif >= 5:
    vif_conclusion = "At least one VIF is at or above 5; investigate possible multicollinearity."
else:
    vif_conclusion = "All predictor VIFs are below 5, so there is no strong VIF-based warning of serious multicollinearity in this model."

interaction_conclusion = (
    "The Age x BMI interaction is statistically significant at alpha = 0.05."
    if interaction_p < ALPHA else
    "The Age x BMI interaction is not statistically significant at alpha = 0.05; this does not prove that the interaction is exactly zero."
)

slope_at_bmi = [
    (bmi, float(interaction_model.params["Age"] + bmi * interaction_coefficient))
    for bmi in (20, 30, 40)
]
interaction_slopes_table = markdown_table(
    ["BMI", "Estimated Age slope (interaction model)"],
    [[bmi, f"{value:.4f}"] for bmi, value in slope_at_bmi],
)

resid_hetero = (
    "evidence of non-constant variance (heteroscedasticity)"
    if bp_p < ALPHA else
    "no strong evidence against constant variance"
)
resid_normality = (
    "evidence against normally distributed residuals"
    if jb_p < ALPHA else
    "insufficient evidence to reject residual normality"
)

report = f"""# Project 12: Multiple Regression and Confounding in Diabetes

## 1. Introduction

This project uses the Pima Indians Diabetes Dataset to study the relationship between Age and Glucose while adjusting for BMI, number of Pregnancies and BloodPressure. The study also checks multicollinearity with VIF and investigates an Age x BMI interaction.

- Data source: {DATA_URL}
- Complete-case observations used in every model: **{len(data)}**
- Outcome / dependent variable: **Glucose**, not diabetes diagnosis.

## 2. Simple regression (Age only)

Mathematical model:

`Glucose_i = beta0 + beta1 * Age_i + error_i`

Fitted model:

`Predicted Glucose = {simple_model.params['const']:.4f} + ({age_simple:.4f}) * Age`

- Age coefficient: **{age_simple:.4f}**
- Age coefficient 95% CI: **[{simple_model.conf_int().loc['Age'].iloc[0]:.4f}, {simple_model.conf_int().loc['Age'].iloc[1]:.4f}]**
- Age coefficient p-value: **{as_p(float(simple_model.pvalues['Age']))}**
- R-squared: **{simple_model.rsquared:.4f}**

## 3. Multiple regression

Mathematical model:

`Glucose_i = beta0 + beta1*Age_i + beta2*BMI_i + beta3*Pregnancies_i + beta4*BloodPressure_i + error_i`

Coefficient results:

{main_coef_table}

- R-squared: **{multiple_model.rsquared:.4f}**
- Adjusted R-squared: **{multiple_model.rsquared_adj:.4f}**

**Interpretation of BMI:** Holding Age, Pregnancies, and BloodPressure constant, a one-unit increase in BMI is associated with **{multiple_coef['BMI']:.4f}** units of difference in predicted Glucose, on average. This is an adjusted association, not a causal effect.

Full model summaries: `project12_simple_summary.txt`, `project12_multiple_summary.txt` and `project12_interaction_summary.txt`.

## 4. Comparing simple and multiple regression

{model_table}

- Simple Age coefficient: **{age_simple:.4f}**
- Adjusted (multiple-regression) Age coefficient: **{age_multiple:.4f}**
- Change in the Age coefficient: **{age_change:+.4f}**
- Relative change vs the simple coefficient: **{age_percent_change:+.2f}%**

![Simple vs Multiple Regression](project12_simple_vs_multiple.png)

**Interpretation:** The Age coefficient changes because the adjusted model also accounts for BMI, Pregnancies and BloodPressure. These variables can be correlated with both Age and Glucose. A coefficient change is compatible with confounding or shared variation, but it **does not by itself prove confounding or a causal effect**. The two models answer different conditional questions.

## 5. Multicollinearity and VIF

Variance Inflation Factor (VIF) measures how strongly a predictor can be explained by the other predictors in the model. Larger VIF values indicate more multicollinearity.

{vif_table}

**Interpretation:** {vif_conclusion} The cutoffs 5 and 10 are common practical guidelines rather than universal laws. VIF is calculated for the four predictors in the multiple model, excluding the intercept.

## 6. Age x BMI interaction

A new column is constructed:

`Age_BMI = Age * BMI`

Interaction model:

`Glucose_i = beta0 + beta1*Age_i + beta2*BMI_i + beta3*Pregnancies_i + beta4*BloodPressure_i + beta5*(Age_i*BMI_i) + error_i`

- Age x BMI coefficient (beta5): **{interaction_coefficient:.6f}**
- 95% CI for interaction coefficient: **[{interaction_model.conf_int().loc['Age_BMI'].iloc[0]:.6f}, {interaction_model.conf_int().loc['Age_BMI'].iloc[1]:.6f}]**
- Interaction p-value: **{as_p(interaction_p)}**
- Interaction model R-squared: **{interaction_model.rsquared:.4f}**

**Result:** {interaction_conclusion}

With this raw (not centered) Age x BMI product, the conditional Age slope depends on BMI:

`Age slope at a given BMI = beta1 + beta5 * BMI`

{interaction_slopes_table}

![Interaction Plot](project12_interaction_plot.png)

The figure shows predicted Glucose across Age at BMI = 20, 30 and 40, while Pregnancies and BloodPressure are held at their **sample means** ({pregnancies_fixed:.2f} and {blood_pressure_fixed:.2f}, respectively). These are model predictions, not actual patient trajectories. In the interaction model, the standalone Age coefficient describes the slope at BMI = 0; this is not a meaningful clinical reference and should not be interpreted alone.

## 7. Residual checks for the multiple regression

![Residuals vs Fitted](project12_residuals_vs_fitted.png)

A residuals-versus-fitted plot helps identify nonlinearity, unequal residual spread, unusual observations, and possible model misspecification. Breusch-Pagan p-value: **{as_p(float(bp_p))}**, suggesting **{resid_hetero}** at alpha = 0.05. Visual inspection is still needed.

![Residual Q-Q Plot](project12_qq_plot.png)

The Q-Q plot examines whether residuals approximately follow a Normal distribution. Jarque-Bera p-value: **{as_p(jb_p)}**; this provides **{resid_normality}** at alpha = 0.05. A test result alone does not establish perfect model assumptions.

## 8. Answers to analytical questions

1. **Age coefficients:** Simple model = {age_simple:.4f}; multiple model = {age_multiple:.4f}; change = {age_change:+.4f}.
2. **Why the change?** The multiple model adjusts for BMI, Pregnancies and BloodPressure. Correlations among predictors and outcome can shift the conditional Age coefficient; this alone does not prove confounding.
3. **BMI effect holding other variables constant:** +1 BMI unit corresponds to {multiple_coef['BMI']:.4f} predicted Glucose units with Age, Pregnancies and BloodPressure fixed.
4. **What is VIF?** A measure of variance inflation in an estimated coefficient caused by relationships among predictors.
5. **Severe multicollinearity?** Maximum VIF = {max_vif:.4f}. {vif_conclusion}
6. **Age x BMI interaction:** Coefficient = {interaction_coefficient:.6f}, p = {as_p(interaction_p)}. {interaction_conclusion} It tests whether the association of Age with Glucose changes with BMI; it does not imply a biological mechanism.
7. **Why not causation?** OLS on observational data may be affected by unmeasured confounding, selection bias, measurement problems, misspecified relationships and reverse causality.
8. **Which variables were adjusted for?** BMI, Pregnancies and BloodPressure were included as candidate confounders. Whether each is a true confounder depends on subject-matter and causal assumptions; statistical adjustment alone is not proof.

## 9. Clinical interpretation and limitations

The models describe **Glucose**, not the probability of diabetes or a clinical diagnosis. These estimates are associations in the observed sample. Raw zero values were retained because the assignment did not specify a data-cleaning rule; zero counts: Glucose = {int((data['Glucose'] == 0).sum())}, BMI = {int((data['BMI'] == 0).sum())}, BloodPressure = {int((data['BloodPressure'] == 0).sum())}. These entries may be clinically implausible and may affect results.

Residual assumptions should be checked, and VIF only evaluates linear dependencies among included predictors. No external validation, cross-validation, nonlinear Age modeling or causal identification strategy was conducted. The sample may not generalize to every population.

## 10. Conclusion

The analysis compares an Age-only regression with an adjusted model using Age, BMI, Pregnancies and BloodPressure. It reports age-coefficient changes, the R-squared of each model, VIF scores, an Age x BMI interaction, and residual diagnostics. Associations and statistical significance should not be interpreted as proof of causality.
"""

(BASE_DIR / "report12.md").write_text(report.strip() + "\n", encoding="utf-8")
print("\nSaved: project12_model_comparison.csv, project12_coefficients.csv,")
print("project12_vif.csv, 3 model summaries, 4 PNG figures, report12.md")
