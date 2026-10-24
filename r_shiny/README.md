# RAPIS — R/Shiny Competition Application

**Team WINNER | NISR 2026 Big Data Hackathon | Track 1**

## Run

From the project root:

```r
source("r_shiny/install.R")
shiny::runApp("r_shiny")
```

The application includes:
- Decision Center
- Productivity Explorer
- District-held-out validated ML benchmark
- Drivers & Practices
- District Profile
- Evidence-based Targeting Lab
- Rwanda Evidence Map (official NISR boundary-ready)
- Scenario Lab (model-based sensitivity analysis)
- NISR Season B 2026 benchmark panel
- Climate & Geospatial Readiness
- Methodology & Impact

## Validated ML

Run the benchmark from the project root:

```bash
python src/validated_ml.py
```

The model uses an Extra Trees regressor with crop type and agricultural practice indicators. Validation uses 5-fold `GroupKFold`, with entire districts held out from each fold. The generated files are:

- `data/processed/ml_validation_summary.json`
- `data/processed/ml_oof_predictions.csv`
- `data/processed/ml_feature_importance.csv`
- `data/processed/rapis_validated_ml.joblib`

The current one-season benchmark is approximately **R² 0.80** and **MAE 1,097 kg/ha**. This is a predictive benchmark, not a causal estimate, and should be revalidated across seasons before operational deployment.

## Next-generation data

External data are deliberately not fabricated. Use the schemas and connector instructions in `data/external/README.md` and `scripts/fetch_external_data.py` to add approved rainfall, soil, elevation, satellite and NISR boundary layers.
