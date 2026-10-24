"""Basic reproducibility and data-integrity checks for the RAPIS package."""
from pathlib import Path
import json
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
errors = []
checks = []

def check(condition, message):
    checks.append((bool(condition), message))
    if not condition:
        errors.append(message)

model_path = ROOT / "data/processed/rapis_model_data.csv"
district_path = ROOT / "outputs/district_summary.csv"
crop_path = ROOT / "outputs/crop_summary.csv"
metrics_path = ROOT / "data/processed/ml_validation_summary.json"
oof_path = ROOT / "data/processed/ml_oof_predictions.csv"

for path in [model_path, district_path, crop_path, metrics_path, oof_path]:
    check(path.exists(), f"Required file exists: {path.relative_to(ROOT)}")

if not errors:
    model = pd.read_csv(model_path)
    district = pd.read_csv(district_path)
    crop = pd.read_csv(crop_path)
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    oof = pd.read_csv(oof_path)

    required = {"District", "Crop", "Yield_kg_ha", "Production_MT"}
    check(required.issubset(model.columns), "Analytical dataset has required columns")
    check(not model[list(required)].isna().any().any(), "Required identifiers and outcomes have no missing values")
    check(not model.duplicated(["District", "Crop"]).any(), "No duplicate district-crop rows")
    check((model["Yield_kg_ha"] >= 0).all(), "Yield values are non-negative")
    check((model["Production_MT"] >= 0).all(), "Production values are non-negative")
    check(model["District"].nunique() == 30, "Analytical table has 30 districts (current package expectation)")
    check(model["Crop"].nunique() == 19, "Analytical table has 19 crop groups (current package expectation)")
    check(len(model) == 522, "Analytical table has 522 crop-district records (current package expectation)")
    check(set(model["District"]) == set(district["District"]), "District summary covers the same districts as analytical data")
    check(set(model["Crop"]) == set(crop["Crop"]), "Crop summary covers the same crop groups as analytical data")
    check(len(oof) == len(model), "Out-of-fold prediction file has one row per analytical observation")
    check(metrics.get("observations") == len(model), "Saved ML summary observation count matches analytical data")
    check(metrics.get("districts") == model["District"].nunique(), "Saved ML summary district count matches analytical data")
    check(metrics.get("crop_groups") == model["Crop"].nunique(), "Saved ML summary crop count matches analytical data")
    check(len(metrics.get("fold_mae_kg_ha", [])) == 5, "Saved ML summary contains five MAE fold results")
    check(len(metrics.get("fold_r2", [])) == 5, "Saved ML summary contains five R-squared fold results")

for ok, message in checks:
    print(f"{'PASS' if ok else 'FAIL'}  {message}")
print(f"\n{sum(ok for ok, _ in checks)}/{len(checks)} checks passed")
if errors:
    sys.exit(1)
