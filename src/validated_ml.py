from pathlib import Path
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import GroupKFold, cross_validate, cross_val_predict
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import mean_absolute_error, r2_score

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'processed' / 'rapis_model_data.csv'
OUT = ROOT / 'data' / 'processed'
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA)
num = [
    'irrigation_pct','inorganic_fertilizer_farmers_pct',
    'organic_fertilizer_farmers_pct','erosion_protected_pct',
    'agroforestry_pct','mechanical_equipment_pct',
    'severe_erosion_pct','moderate_erosion_pct',
    'low_erosion_pct','very_low_erosion_pct'
]
cat = ['Crop']
features = num + cat
X = df[features]
y = df['Yield_kg_ha']
groups = df['District']

pre = ColumnTransformer([
    ('num', SimpleImputer(strategy='median'), num),
    ('cat', OneHotEncoder(handle_unknown='ignore'), cat)
])
model = ExtraTreesRegressor(
    n_estimators=600, min_samples_leaf=3, random_state=42, n_jobs=-1
)
pipe = Pipeline([('preprocess', pre), ('model', model)])
cv = GroupKFold(n_splits=5)

scores = cross_validate(
    pipe, X, y, cv=cv, groups=groups,
    scoring={'mae':'neg_mean_absolute_error','r2':'r2'},
    return_train_score=False
)
oof = cross_val_predict(pipe, X, y, cv=cv, groups=groups, method='predict')

metrics = {
    'model': 'ExtraTreesRegressor',
    'validation': '5-fold GroupKFold; district held out by group',
    'observations': int(len(df)),
    'districts': int(df.District.nunique()),
    'crop_groups': int(df.Crop.nunique()),
    'mae_kg_ha': float(-scores['test_mae'].mean()),
    'r2': float(scores['test_r2'].mean()),
    'fold_mae_kg_ha': [float(x) for x in -scores['test_mae']],
    'fold_r2': [float(x) for x in scores['test_r2']],
    'warning': 'One-season aggregated data; predictive performance should be revalidated on additional seasons and external covariates before operational deployment.'
}
(OUT / 'ml_validation_summary.json').write_text(json.dumps(metrics, indent=2))

pred = df[['District','Crop','Yield_kg_ha']].copy()
pred['OOF_Predicted_Yield_kg_ha'] = oof
pred['OOF_Absolute_Error_kg_ha'] = np.abs(pred['Yield_kg_ha'] - pred['OOF_Predicted_Yield_kg_ha'])
pred.to_csv(OUT / 'ml_oof_predictions.csv', index=False)

pipe.fit(X, y)
model_only = pipe.named_steps['model']
pre_fitted = pipe.named_steps['preprocess']
feature_names = list(pre_fitted.get_feature_names_out())
imp = pd.DataFrame({'Feature': feature_names, 'Importance': model_only.feature_importances_})
imp['Feature'] = imp['Feature'].str.replace('num__','',regex=False).str.replace('cat__Crop_','Crop: ',regex=False)
imp = imp.sort_values('Importance', ascending=False)
imp.to_csv(OUT / 'ml_feature_importance.csv', index=False)

try:
    import joblib
    joblib.dump({'pipeline': pipe, 'features': features, 'validation': metrics}, OUT / 'rapis_validated_ml.joblib')
except Exception:
    pass

print(json.dumps(metrics, indent=2))
