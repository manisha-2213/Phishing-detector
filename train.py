"""Train the phishing URL model.

Usage:
    python train.py                      # uses the small sample_data.csv (demo only)
    python train.py path/to/dataset.csv  # CSV with columns: url,label  (label: 1 = phishing, 0 = safe)
"""
import sys

import joblib
import matplotlib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score,
                             classification_report)
from sklearn.model_selection import train_test_split

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from features import FEATURE_NAMES, extract_features

data_path = sys.argv[1] if len(sys.argv) > 1 else "sample_data.csv"
df = pd.read_csv(data_path)
df = df.dropna(subset=["url", "label"]).drop_duplicates(subset="url")
print(f"Loaded {len(df)} URLs from {data_path}")

X = pd.DataFrame([extract_features(u) for u in df["url"]])[FEATURE_NAMES]
y = df["label"].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

pred = model.predict(X_test)
print(f"\nAccuracy: {accuracy_score(y_test, pred):.2%}")
print(classification_report(y_test, pred, target_names=["safe", "phishing"]))

ConfusionMatrixDisplay.from_predictions(
    y_test, pred, display_labels=["safe", "phishing"], cmap="Blues"
)
plt.title("Confusion matrix")
plt.savefig("confusion_matrix.png", dpi=150, bbox_inches="tight")

joblib.dump(model, "model.joblib")
print("Saved model.joblib and confusion_matrix.png")
