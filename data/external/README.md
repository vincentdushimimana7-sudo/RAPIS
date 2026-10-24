# RAPIS External Data Contract

RAPIS does **not** invent climate, soil, terrain, satellite or spatial observations. External layers become active only when the corresponding approved file is supplied.

## Required district-level files

| File | Minimum columns | Example source |
|---|---|---|
| `climate_district.csv` | `District`, `rainfall_mm`, `rainfall_anomaly_pct`, `dry_spell_days` | NASA POWER / approved meteorological source |
| `soil_district.csv` | `District`, `soil_ph`, `soil_organic_carbon`, `soil_clay_pct`, `soil_nitrogen` | ISRIC SoilGrids |
| `elevation_district.csv` | `District`, `elevation_m`, `slope_pct` | Approved DEM |
| `satellite_district.csv` | `District`, `ndvi_mean`, `ndvi_anomaly_pct`, `vegetation_stress_pct` | Copernicus Sentinel-2 / approved service |
| `rwanda_districts.geojson` | official district geometry + `District` field | NISR GIS Open Data |

## Important

- Preserve source, date, spatial resolution and processing method in a companion metadata file.
- Do not mix seasons without explicitly adding a `Season` or `Year` field.
- Do not interpret external associations as causal effects without an appropriate identification strategy.
- For operational use, prefer official/approved sources and document licenses and access dates.

## Official data pathways used by the project

NISR provides an open GIS service for Rwanda administrative boundaries. The NISR GIS service documents WGS84 coordinates and GeoJSON query support.

SoilGrids provides global soil information through ISRIC; its REST API is beta/subject to availability, so the project recommends stable downloadable/WebDAV or WCS pathways where appropriate.

NASA POWER can provide climate time series suitable for an analytical prototype. Sentinel-2 data can supply vegetation indicators after appropriate preprocessing.
