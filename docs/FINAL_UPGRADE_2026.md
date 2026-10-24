# RAPIS — Final NISR 2026 Competition Upgrade

## What was added

1. **Rwanda Evidence Map**
   - Uses official/approved NISR boundary GeoJSON when present.
   - Joins district evidence-priority scores to geography.
   - Does not fabricate coordinates or district polygons.
   - Shows observed yield, irrigation, severe erosion and evidence-priority score in map popups.

2. **Scenario Lab**
   - Lets the user vary irrigation, inorganic fertilizer, erosion protection and agroforestry levels.
   - Returns a model-based sensitivity estimate for the selected crop.
   - Explicitly distinguishes scenario analysis from causal impact estimation.

3. **Latest NISR benchmark panel**
   - Adds official Season B 2026 national agricultural indicators to the NISR Scorecard.
   - The source is linked in the app and documentation.

4. **Competition narrative**
   - Demo path is now: Decision Center → Evidence Map → Validated ML → Targeting Lab → Scenario Lab → NISR Scorecard.

## Why these changes matter

NISR's 2026 Track 1 asks for innovative data-driven solutions to real agricultural challenges and explicitly highlights irrigation, soil conservation/fertility, post-harvest storage, processing/value addition and export opportunities. NISR also evaluates problem relevance, data/methodology, technology innovation, usability/design and tangible impact at 20 points each.

RAPIS therefore emphasizes a simple chain:

**NISR evidence → spatial diagnosis → validated predictive signal → transparent targeting → scenario exploration → practical decision support**

## Important integrity rules

- Do not describe the targeting score as an official government ranking.
- Do not describe exploratory associations as causal effects.
- Do not present scenario outputs as guaranteed treatment impacts.
- Do not claim climate/soil/satellite analysis until the corresponding approved data are actually connected.
- Verify every statistic against the original NISR source before submission.

## Official current benchmark used in the app

NISR's Season B 2026 release reports coverage across all 30 districts and national rates including 20.9% improved-seed use, 81.3% organic-fertilizer use, 57.5% inorganic-fertilizer use, 39.1% pesticide use, 13.1% irrigation, 58% agroforestry and 1.8% mechanical-equipment use.

Source: https://statistics.gov.rw/statistical-publications/agriculture-environment/seasonal-agricultural-survey-season-b-2026
