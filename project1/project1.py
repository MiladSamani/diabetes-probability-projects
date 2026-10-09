import pandas as pd
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"

columns = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
    "Outcome"
]

df = pd.read_csv(url, names=columns)

print(df.head())

print(df.shape)

print(df["Outcome"].value_counts())

total = len(df)

diabetic = (df["Outcome"] == 1).sum()

non_diabetic = (df["Outcome"] == 0).sum()

p_diabetic = diabetic / total

p_non_diabetic = non_diabetic / total

print("P(Diabetes):", p_diabetic)
print("P(No Diabetes):", p_non_diabetic)

print("Sum:", p_diabetic + p_non_diabetic)

p_classical_diabetes = 0.5

print("Classical P(Diabetes):", p_classical_diabetes)
print("Empirical P(Diabetes):", p_diabetic)


plt.bar(
    ["No Diabetes", "Diabetes"],
    [non_diabetic, diabetic]
)

plt.title("Diabetes Outcome Distribution")
plt.xlabel("Outcome")
plt.ylabel("Number of Patients")

plt.savefig("outcome_distribution.png")
plt.show()
