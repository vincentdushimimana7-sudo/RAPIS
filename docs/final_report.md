# RAPIS — Final Project Draft

## 1. Executive summary
RAPIS is a data-driven agricultural productivity intelligence prototype for Rwanda. It uses NISR Seasonal Agricultural Survey Season B 2026 tables to examine reported crop yields and agricultural practices across districts. The system is designed to evolve into a predictive decision-support platform after approved microdata and compatible external datasets are obtained.

## 2. Problem
Agricultural productivity differs across crops and locations. Decision-makers need structured evidence on productivity patterns and observable agricultural practices to support planning.

## 3. Objectives
- Measure reported productivity across crops and districts.
- Examine associations with irrigation, fertilizer use, erosion protection and agroforestry.
- Develop an exploratory predictive modelling pipeline.
- Present results in an interactive dashboard.
- Establish a roadmap for integrating climate, soil and satellite data.

## 4. Data
The workbook supplied for this project contains 33 Season B 2026 tables. Key tables used:
- Table 11: average yield by crop type and district.
- Table 13: crop production by crop type and district.
- Table 22: organic fertilizer use.
- Table 23: inorganic fertilizer use.
- Table 29: agricultural practices including irrigation and erosion protection.
- Table 33: degree of erosion by district.

## 5. Methods
The project reshapes crop-by-district yield and production tables into a long analytical dataset and merges district-level practice indicators. Descriptive statistics and visualization are followed by exploratory machine-learning modelling. Group-aware cross-validation is planned/used so that districts are not simultaneously treated as independent training and testing units.

## 6. Expected impact
Potential users include agricultural planners, government institutions, development partners, researchers and civil society organizations. The eventual system will support evidence-based identification of productivity patterns and intervention areas.

## 7. Limitations
- Current data are aggregated.
- Current analysis covers Season B 2026.
- District-level practice variables repeat across crops.
- Correlation does not imply causation.
- A single season cannot establish long-term trends.
- Climate and satellite variables have not yet been merged.

## 8. Next phase
Approved NISR microdata + rainfall + temperature + soil + elevation + satellite indicators -> validated predictive model -> geospatial map -> deployed decision-support application.

## 9. NISR 2026 competition alignment

RAPIS is designed for NISR's Track 1: Agricultural Productivity. The project directly addresses the track's stated areas of small-scale irrigation and soil conservation/fertility management, while documenting post-harvest, value-addition and export opportunities as future modules requiring approved data.

The application is structured around the five official 2026 evaluation criteria: problem understanding and relevance, data use and methodology, technology innovation, usability and design, and tangible impact.

The project also includes an explicit AI-assistance disclosure and submission-readiness checklist. Source: NISR 2026 Hackathon Competition, https://statistics.gov.rw/about/hackathon/2026-hackathon-competition
