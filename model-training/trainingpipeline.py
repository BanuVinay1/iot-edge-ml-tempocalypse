import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

# -------- Load Spike-Rich Data --------
df = pd.read_parquet("data/tempocalypse_v2.parquet")

# -------- Label Generation --------
temps = df["temperature"].values
label = []
for i in range(len(temps)):
    future_temps = temps[i+1:i+6]
    label.append(1 if any(t > 50 for t in future_temps) else 0)

df = df.iloc[:-5]
df["will_cross_50_next_5min"] = label[:-5]

# -------- Feature Engineering --------
df["temp_delta"] = df["temperature"].diff().fillna(0)
df["rolling_mean_5"] = df["temperature"].rolling(5).mean().bfill()
df["rolling_std_5"] = df["temperature"].rolling(5).std().bfill()
df["rolling_max_5"] = df["temperature"].rolling(5).max().bfill()
df["temp_diff_3min"] = df["temperature"] - df["temperature"].shift(3).bfill()

# -------- Feature Set --------
X = df[[
    "temperature",
    "humidity",
    "temp_delta",
    "rolling_mean_5",
    "rolling_std_5",
    "rolling_max_5",
    "temp_diff_3min"
]]
y = df["will_cross_50_next_5min"]

# -------- Train/Test Split (Stratified & Balanced) --------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, random_state=42, stratify=y
)

# -------- Model Training --------
model = RandomForestClassifier(
    class_weight="balanced",
    n_estimators=150,
    max_depth=15,
    random_state=42
)
model.fit(X_train, y_train)

# -------- Threshold Tuning --------
probs = model.predict_proba(X_test)[:, 1]
y_pred = (probs > 0.4).astype(int)

# -------- Evaluation --------
print("🔍 Classification Report:\n", classification_report(y_test, y_pred))
print("📊 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# -------- Save Model --------
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/tempocalypse_model.pkl")
print("✅ RandomForest model saved as models/tempocalypse_model.pkl")
