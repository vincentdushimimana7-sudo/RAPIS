from pathlib import Path
import pandas as pd
from sklearn.model_selection import GroupKFold, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np
import joblib

df = pd.read_csv("data/processed/rapis_model_data.csv")
features = ["irrigation_pct","inorganic_fertilizer_farmers_pct",
            "organic_fertilizer_farmers_pct","erosion_protected_pct",
            "agroforestry_pct","severe_erosion_pct","moderate_erosion_pct"]
X = df[features]
y = df["Yield_kg_ha"]
groups = df["District"]

pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("model", RandomForestRegressor(n_estimators=300, random_state=42, min_samples_leaf=3))
])

cv = GroupKFold(n_splits=5)
mae = -cross_val_score(pipe, X, y, cv=cv, groups=groups,
                       scoring="neg_mean_absolute_error").mean()
r2 = cross_val_score(pipe, X, y, cv=cv, groups=groups,
                     scoring="r2").mean()
print("Grouped 5-fold CV MAE:", mae)
print("Grouped 5-fold CV R2:", r2)

pipe.fit(X,y)
Path("data/processed").mkdir(exist_ok=True)
joblib.dump({"pipeline":pipe,"features":features}, "data/processed/rapis_model.joblib")
