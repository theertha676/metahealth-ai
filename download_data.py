# download_data.py - Get real diabetes dataset
import pandas as pd
import urllib.request
import os

print("📥 Downloading PIMA Indian Diabetes Dataset...")

# URL for the dataset
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"

# Column names
columns = ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 
           'insulin', 'bmi', 'diabetes_pedigree', 'age', 'outcome']

# Download and save
urllib.request.urlretrieve(url, "pima-diabetes.csv")

# Load and verify
df = pd.read_csv("pima-diabetes.csv", names=columns)
print(f"✅ Dataset downloaded! Shape: {df.shape}")
print(f"📊 Samples: {len(df)} patients")
print(f"🎯 Diabetic: {df['outcome'].sum()} patients")
print(f"✅ Non-diabetic: {len(df) - df['outcome'].sum()} patients")
print("\nFirst 5 rows:")
print(df.head())

# Save with headers for clarity
df.to_csv("pima-diabetes.csv", index=False)
print("\n💾 Saved as 'pima-diabetes.csv'")