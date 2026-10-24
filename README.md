# RAPIS — Rwanda Agricultural Productivity Intelligence System

**Team:** WINNER  
**Competition:** NISR 2026 Big Data Hackathon  
**Track:** Agricultural Productivity  
**Primary dashboard:** Streamlit (`app/streamlit_app.py`)  
**Alternative dashboard:** R Shiny (`r_shiny/`)

## Project question

How can NISR agricultural data and complementary public data be used to identify factors associated with differences in agricultural productivity across Rwanda and support evidence-based agricultural planning?

## What RAPIS provides

- An interactive overview of crop-by-district productivity evidence.
- Crop-specific comparisons of reported yield and production.
- District profiles combining observed crop outcomes with available agricultural-practice indicators.
- A transparent evidence-priority score using productivity gaps, irrigation indicators and severe-erosion indicators.
- An Extra Trees predictive benchmark evaluated with five-fold GroupKFold, holding out entire districts in each fold.
- Downloadable CSV tables for further analysis.
- Clear statements of data coverage, methods and limitations.

## Run locally

Use Python 3.10 or newer.

```bash
python -m venv .venv
```

Activate the environment, then run:

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

To reproduce the saved machine-learning validation outputs:

```bash
python src/validated_ml.py
python scripts/validate_project.py
```

The dashboard reads the processed files under `data/processed/` and summary files under `outputs/`. Run commands from this project root.

## Main folders

```text
rapis_work/
├── app/
│   └── streamlit_app.py
├── data/
│   ├── raw/                 # supplied source workbook
│   ├── processed/           # crop-district data and ML outputs
│   └── external/            # source notes and optional external layers
├── docs/                    # methodology, governance, alignment and project notes
├── outputs/                 # district/crop summaries and charts
├── r_shiny/                 # alternative R Shiny dashboard
├── scripts/                 # optional external-data helpers
├── src/
│   ├── model.py
│   └── validated_ml.py
├── requirements.txt
└── README.md
```

## Data provenance and interpretation

The current prototype uses the supplied workbook named `NISR_SAS_2026_Season_B_tables.xlsx` and processed crop-by-district data included in this package. Before public release, the team should verify the exact table references, definitions, units, transformations and permission/terms for every source against the original NISR publication or portal. Do not claim that the external climate, soil, satellite or boundary layers are integrated unless their actual data files and sources are present.

The processed analytical table contains 522 crop-by-district records, 30 districts and 19 crop groups. The unit of analysis is aggregated, not individual-farm microdata.

## Predictive model

The saved benchmark reports an Extra Trees regressor evaluated with five-fold GroupKFold by district. The reported values are stored in `data/processed/ml_validation_summary.json` and visualized in the dashboard. They must be interpreted as a single-season, aggregated-data benchmark—not as future harvest accuracy, causal evidence, or a guarantee of generalization to later seasons. Reproduce the results from `src/validated_ml.py` before quoting them in a presentation.

## Evidence-priority score

The dashboard's default score uses three transparent components:

- 45% productivity gap;
- 30% irrigation gap;
- 25% severe-erosion pressure.

The app lets users adjust these weights. The weights are project-defined assumptions, normalized to sum to one; the score is a screening aid for further investigation, not an official government ranking or a validated intervention-impact estimate.

## Important limitations

- One season of aggregated observations cannot establish causal effects.
- District mean yields combine different crop groups and should not be used as a crop-neutral measure of overall productivity without further justification.
- Relationships between practice indicators and yield are exploratory.
- External climate, soil, elevation, satellite and administrative-boundary layers are not invented. The app shows the current data status and requires approved, documented files before those features can be used.
- Predictions should be evaluated on additional seasons and compared with a baseline before operational use.

## Technical integrity check

Run `python scripts/validate_project.py` to check required files, data row counts, district/crop coverage, duplicate keys, non-negative outcomes and consistency of the saved validation artifacts. The check is a package-integrity test; it does not independently verify the original NISR source tables. See `docs/TECHNICAL_REVIEW.md`.

## Documentation

See `docs/` for competition alignment, strategy, data governance, methodology, disclosure and project notes. The R/Shiny alternative has separate instructions in `r_shiny/README.md`.
