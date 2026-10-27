# RAPIS — Rwanda Agricultural Productivity Intelligence System

**Team:** WINNER  
**Competition:** NISR 2026 Big Data Hackathon  
**Track:** Agricultural Productivity  
**Live dashboard:** https://mdcpg6hvhrmnsb4mbd2fm2.streamlit.app/  
**GitHub repository:** https://github.com/vincentdushimimana7-sudo/RAPIS
**Video link:**https://drive.google.com/file/d/1cdpqJxRDVaXgH5TGg6dwfaaOXoSz5dEQ/view?usp=sharing
## Project purpose

RAPIS is an agricultural decision-support prototype that uses available NISR agricultural survey data to explore crop productivity differences across districts and identify evidence-based priorities for further investigation.

**Research question:** How can NISR agricultural data and complementary public data be used to identify factors associated with differences in agricultural productivity across Rwanda and support evidence-based agricultural planning?

## Strategic alignment

RAPIS is designed to support the direction of Rwanda's:
- **NST2 (2024–2029):** climate-resilient, productive and modernized agri-food systems, including increased productivity of priority food crops.
- **Vision 2050:** the long-term ambition for prosperity and quality of life, including agriculture as a source of wealth creation.
- **PSTA5 (2024–2029):** transformation toward resilient and sustainable agri-food systems.

The dashboard is an analytical prototype. It does not determine official government priorities, prove causal impacts, or replace official monitoring systems.

## Current prototype and data boundaries

The repository's project documentation describes a processed analytical table with 522 crop-by-district records, 30 districts and 19 crop groups. Confirm the exact original NISR publication, table references, definitions, units and use conditions before external publication.

The current analysis is aggregated at crop–district level. It is not individual-farm microdata. External climate, soil, elevation, satellite and boundary data must only be described as integrated when the actual sourced files and processing steps are present.

## What the prototype is intended to provide

- Crop and district productivity exploration.
- Comparisons of reported yield and production.
- District profiles using available agricultural-practice indicators.
- A transparent evidence-priority score using productivity gaps, irrigation indicators and severe-erosion indicators.
- A predictive benchmark with district-held-out validation, interpreted cautiously.
- Downloadable analytical tables and clear methodology notes.
- Policy-alignment information explaining how observed indicators relate to NST2, Vision 2050 and PSTA5.

## Run locally

Use Python 3.10 or newer:

```bash
python -m venv .venv
```

Activate the environment, then run:

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

To reproduce and check the analytical outputs:

```bash
python src/validated_ml.py
python scripts/validate_project.py
```

Run commands from the repository root.

## Important interpretation safeguards

1. A one-season aggregated dataset cannot establish causal effects.
2. Crop yields should be compared within comparable crop groups; a simple average across different crops may be misleading.
3. The evidence-priority score is a project-defined screening tool, not an official government ranking or validated intervention-impact estimate.
4. Predictive performance on held-out districts does not establish performance in future seasons. Validate with additional seasons before operational use.
5. Do not present policy targets as RAPIS results. Show the source, baseline year, target year, unit and status for every target.
6. Do not invent external data, geographic coverage, model performance, or impacts.

## Policy alignment files

- `docs/NST2_VISION2050_ALIGNMENT.md` — detailed policy alignment and recommended use.
- `docs/POLICY_ALIGNMENT_MATRIX.csv` — policy-to-indicator matrix for dashboard design.
- `app/policy_alignment_section.py` — optional Streamlit section that can be integrated into the main dashboard.

## Official references

- Rwanda National Strategy for Transformation 2 (NST2), 2024–2029: https://www.primature.gov.rw/news-detail/prime-minister-presented-to-parliament-governments-five-year-program-nst2
- Official NST2 document (PDF): https://minecofinnew.prod.risa.gov.rw/fileadmin/user_upload/Minecofin/Publications/REPORTS/National_Development_Planning_and_Research/NST2/NST2_2024-2029.pdf
- Ministry of Agriculture and Animal Resources announcement on PSTA5: https://www.minagri.gov.rw/updates/news-details/rwanda-launches-5th-strategic-plan-for-agriculture-transformation
- NISR Fourth National Strategy for the Development of Statistics (NSDS4): https://www.statistics.gov.rw/documents/strategies-and-policies/fourth-national-strategy-development-statistics-nsds4
- ## Video Demonstration

Watch our presentation of the Rwanda Agricultural Productivity Intelligence System (RAPIS), developed by Team Winner for the NISR 2026 Big Data Hackathon.

**Project Video:** [Watch the RAPIS Presentation](https://drive.google.com/file/d/1cdpqJxRDVaXgH5TGg6dwfaaOXoSz5dEQ/view?usp=sharing)

The video presents the agricultural productivity challenge, our data and methodology, the interactive dashboard, and the potential contribution of RAPIS to evidence-based agricultural planning in Rwanda, aligned with NST2 and Vision 2050.

