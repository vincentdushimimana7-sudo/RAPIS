# RAPIS technical review and release notes

## What was improved in this package

- Reworked the Streamlit dashboard into a clearer six-section workflow: Overview, Productivity Explorer, District Profiles, Targeting Lab, Predictive Benchmark, and Data & Methodology.
- Added global crop and district filters, clearer units, more legible charts, evidence safeguards, downloadable CSV outputs, district profiles, and adjustable targeting weights.
- Added visible explanations distinguishing descriptive evidence, predictive performance, and causal claims.
- Added a simple project validation script and an explicit run sequence.
- Updated the root README and dependency ranges, and added a Streamlit theme and Git ignore rules.
- Retained the R/Shiny app as an alternative dashboard.

## Integrity checks run on the supplied package

- Processed analytical data: 522 rows, 30 districts, 19 crop groups.
- No duplicate district-crop pairs were detected.
- Required identifiers and outcome fields had no missing values.
- No negative yield or production values were detected.
- District and crop summary coverage matched the analytical dataset.
- Saved out-of-fold prediction and model summary row/count checks matched the analytical data.
- Python syntax compilation passed for the Streamlit app and the existing model scripts.

Run `python scripts/validate_project.py` from the project root to repeat the basic checks.

## Items not represented as completed

- No video was created as part of this redesign.
- No GitHub publication, public deployment, or submission action was performed.
- The supplied package does not demonstrate that the app has been tested on a public host.
- External climate, soil, elevation, satellite, and official district-boundary layers remain unconnected unless their real source files are added and documented.
- Exact NISR table identifiers, source-page citations, source permissions, and every transformation still require final verification by the team against the original source publication/portal.
- The ML benchmark should be rerun from the included code in the team's target environment before the reported metrics are used in final presentation materials.

## Responsible interpretation

The targeting score is a transparent, user-adjustable screening aid. It is not an official government ranking or a causal estimate of intervention impact. District-wide mean yields combine different crop groups; crop-specific comparisons are preferred when comparing like with like. The predictive model is based on one season of aggregated observations and is not a guarantee of future harvest performance.
