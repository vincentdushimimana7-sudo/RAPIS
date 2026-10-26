# RAPIS alignment with NST2, Vision 2050 and PSTA5

## 1. Strategic rationale

RAPIS (Rwanda Agricultural Productivity Intelligence System) supports evidence-informed agricultural planning by helping users explore observed differences in crop productivity, review available agricultural-practice indicators and identify locations or crop groups that may warrant further investigation.

The policy connection is deliberate:

- **NST2 (2024–2029)** sets a national transformation agenda and includes a priority for climate-resilient, productive and modernized agri-food systems. Its agricultural agenda includes increasing productivity of priority food crops.
- **Vision 2050** sets Rwanda's longer-term development direction toward prosperity and improved quality of life; agriculture is recognized as a source of wealth creation.
- **PSTA5 (2024–2029)** provides the sector-specific agricultural transformation framework, emphasizing resilient and sustainable agri-food systems.

RAPIS should be presented as a prototype that can contribute analytical evidence to these priorities—not as an official government platform or proof that a policy target has been achieved.

## 2. Policy-to-dashboard connection

### A. Priority crop productivity

**Policy connection:** NST2 includes a target to raise productivity of priority food crops. The official NST2 document contains crop-specific baseline and end-period targets for crops such as maize, beans, rice, Irish potatoes, wheat, soybean and cassava.

**RAPIS contribution:** Display observed yield and production by crop and district, with clear units, season/year, data source and coverage. Where the available data use a compatible definition and period, compare observations with official targets.

**Required safeguards:**
- Never compare values with different units or definitions.
- Show the target's source and target year.
- Mark unavailable or non-comparable values as “Not available” rather than estimating them without a documented method.
- Distinguish observed results from official target values.

### B. Climate resilience and sustainable land management

**Policy connection:** NST2 and PSTA5 prioritize resilient and sustainable agri-food systems.

**RAPIS contribution:** Explore the available irrigation, erosion-protection and erosion-severity indicators alongside crop productivity. This can help users identify patterns that merit field verification or additional data collection.

**Required safeguards:** These associations are exploratory. Do not claim that irrigation or erosion indicators caused a yield difference without an appropriate causal design. Climate, rainfall, soil, elevation and satellite layers should only appear as integrated features when real, documented datasets are present.

### C. Evidence-based planning and targeting

**Policy connection:** NST2 implementation depends on monitoring progress and directing interventions toward development priorities. NISR's statistical strategy emphasizes timely, accessible statistics for evidence-based policymaking.

**RAPIS contribution:** Offer transparent filters, district and crop profiles, downloadable tables and a screening score that highlights evidence gaps or areas for further investigation.

**Required safeguards:** The score is a project-defined decision-support aid, not an official government ranking. Display its components, weights, missing-data treatment and limitations. It should support—not replace—expert review and consultation with local stakeholders.

### D. Agriculture, livelihoods and wealth creation

**Policy connection:** Vision 2050 positions agriculture within Rwanda's long-term wealth-creation ambitions; NST2 and PSTA5 aim to modernize the sector and strengthen resilience and productivity.

**RAPIS contribution:** Help analysts examine crop productivity patterns relevant to food availability, farm-sector performance and agricultural planning.

**Required safeguards:** Do not claim RAPIS has increased farmer incomes, reduced poverty, improved nutrition or created jobs unless a suitable impact evaluation or verified outcome data support that claim.

## 3. Recommended dashboard policy panel

Add a tab or section called **“Policy Alignment: NST2 & Vision 2050”** with:

1. **Policy context:** concise summaries of NST2, Vision 2050 and PSTA5.
2. **Priority crop indicators:** observed yield/production by crop, with source and unit.
3. **Official target comparison:** only where the observation and official target are definitionally comparable.
4. **Resilience indicators:** irrigation and erosion indicators available in the dataset.
5. **Evidence-priority screening:** score components, weights, and clear disclaimer that this is not an official ranking.
6. **Data coverage and limitations:** seasons, districts, crop groups, missing values, aggregation level and external data status.
7. **Download:** a CSV of the currently filtered observations and a policy-alignment matrix.

## 4. Suggested indicators and reporting rules

| Theme | Candidate indicator | Reporting rule |
|---|---|---|
| Crop productivity | Yield by crop and district | Report with unit, season/year, and source |
| Crop output | Production by crop and district | Report with unit and source |
| Irrigation | Available irrigation indicator | State denominator and definition if known |
| Land protection | Erosion protection / erosion severity | Explain category definitions and missingness |
| Priority screening | Productivity gap, irrigation gap, severe-erosion pressure | Show formula and weights; call it a screening score |
| Policy targets | Official NST2 crop target | Cite official source and target year; do not label it a RAPIS achievement |
| Data readiness | Coverage and completeness | Show records, districts, crop groups, period and missing data |

## 5. Suggested public-facing explanation

“RAPIS translates available agricultural statistics into an interactive evidence-exploration tool. It supports Rwanda's NST2 (2024–2029) and Vision 2050 direction by making crop- and district-level productivity patterns easier to examine, highlighting where additional evidence may be needed, and encouraging transparent, data-informed agricultural planning. Its outputs are exploratory and should be interpreted alongside official statistics, field knowledge and further-season validation.”

## 6. Limitations and responsible use

- The current prototype uses aggregated crop–district observations, not individual farm records.
- A single season or limited time coverage cannot establish long-term trends or causal impacts.
- Prediction results are benchmarks, not guaranteed future-harvest forecasts.
- The evidence-priority score is not an official district ranking.
- Do not claim external datasets are incorporated until they are sourced, documented and present in the repository.
- Before public release, verify original NISR table references, definitions, units, and the permitted use of source data.

## 7. Official references

- NST2 announcement by the Office of the Prime Minister: https://www.primature.gov.rw/news-detail/prime-minister-presented-to-parliament-governments-five-year-program-nst2
- Full NST2 document: https://minecofinnew.prod.risa.gov.rw/fileadmin/user_upload/Minecofin/Publications/REPORTS/National_Development_Planning_and_Research/NST2/NST2_2024-2029.pdf
- MINAGRI announcement on PSTA5: https://www.minagri.gov.rw/updates/news-details/rwanda-launches-5th-strategic-plan-for-agriculture-transformation
- NISR NSDS4: https://www.statistics.gov.rw/documents/strategies-and-policies/fourth-national-strategy-development-statistics-nsds4
