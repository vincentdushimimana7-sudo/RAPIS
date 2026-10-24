# RAPIS Complete Project Package

Team: WINNER  
Competition: NISR 2026 Big Data Hackathon  
Track: Agricultural Productivity

## Start the dashboard on Windows
1. Install Python 3.10 or newer.
2. Double-click `run_rapis_windows.bat`.
3. Wait for dependencies and checks to complete.
4. Open the local URL printed by Streamlit.

Alternatively, from this `rapis_work` directory run:

```bash
pip install -r requirements.txt
python scripts/validate_project.py
streamlit run app/streamlit_app.py
```

## Included folders
- `app/`: primary Streamlit dashboard.
- `r_shiny/`: alternative R Shiny dashboard and setup instructions.
- `data/raw/`: supplied source workbook.
- `data/processed/`: processed analysis data and saved model outputs.
- `data/external/`: notes on external data sources and integration status.
- `outputs/`: crop/district summaries and chart images.
- `src/`: model and validation code.
- `scripts/`: validation and optional external-data helper scripts.
- `docs/`: methodology, data governance, NISR alignment, technical review, and validation report.

## Important scope notes
This package contains the project code and data files available to the team. The dashboard must still be run and checked on the team's computer. Verify the original NISR table references and source-data permissions before public release. Climate, soil, satellite, and boundary layers are not represented as fully integrated unless corresponding data files and working code are present.

The demonstration video and the public GitHub/deployment/submission process are intentionally excluded, as requested.
