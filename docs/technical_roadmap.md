# RAPIS Next-Generation Technical Roadmap

## Implemented in this release

1. Professional R/Shiny decision-support interface.
2. District-held-out Extra Trees benchmark.
3. Out-of-fold predictions and feature importance.
4. Transparent intervention-targeting score.
5. External-data contract for climate, soil, terrain, satellite and official geography.
6. Connector template for NISR GIS and NASA POWER.

## Phase 2 — multi-season forecasting

Add at least several seasons/years of crop-district observations and use time-aware validation. Candidate models:

- Extra Trees / Random Forest baseline
- Gradient boosting
- Regularised regression
- Hierarchical models for district/crop effects

Validation should include both held-out districts and held-out seasons where sample size permits.

## Phase 3 — climate-smart geospatial intelligence

Join crop outcomes with:

- rainfall totals and anomalies
- temperature and heat stress
- dry-spell indicators
- soil properties
- elevation/slope
- satellite vegetation indices
- official NISR administrative boundaries

The final unit can move from district to sector/cell if compatible NISR agricultural observations are available.

## Phase 4 — operational decision support

Produce:

- district/sector evidence briefs
- intervention scenario comparisons
- uncertainty intervals
- data-quality flags
- source/provenance panel
- model monitoring across new seasons
- reproducible refresh pipeline

## Non-negotiable safeguards

RAPIS must not claim that an observational association is a causal treatment effect. Every external layer must carry source, date, spatial resolution, processing and licensing metadata.
