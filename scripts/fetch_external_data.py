"""RAPIS external-data connector templates.

This script is intentionally conservative: it downloads only from documented public
endpoints and writes raw/derived files only when a connection succeeds. Review source,
license, date and spatial resolution before using any layer in a competition submission.

Install: pip install requests pandas numpy
"""
from pathlib import Path
import json
import time
import requests
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "external"
OUT.mkdir(parents=True, exist_ok=True)

# NISR public GIS service. The returned GeoJSON can be used by GIS software/R sf.
NISR_URL = ("https://gis-server.statistics.gov.rw/server/rest/services/Hosted/"
            "Cell_Boundary_2022__Open_Data_/FeatureServer/2/query")


def fetch_nisr_boundaries():
    params = {
        "where": "1=1",
        "outFields": "District,Sect_ID,Sector,Cell_ID,Cell",
        "returnGeometry": "true",
        "outSR": "4326",
        "f": "geojson",
    }
    r = requests.get(NISR_URL, params=params, timeout=60)
    r.raise_for_status()
    path = OUT / "rwanda_cells_nisr.geojson"
    path.write_bytes(r.content)
    return str(path)


def fetch_power_point(lat, lon, start="2025", end="2025"):
    url = "https://power.larc.nasa.gov/api/temporal/monthly/point"
    params = {
        "parameters": "PRECTOTCORR,T2M",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start,
        "end": end,
        "format": "JSON",
    }
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    return r.json()


def main():
    report = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "layers": {}}
    try:
        report["layers"]["nisr_boundary"] = {"status": "downloaded", "path": fetch_nisr_boundaries()}
    except Exception as exc:
        report["layers"]["nisr_boundary"] = {"status": "not_downloaded", "error": str(exc)}

    # NASA POWER requires district coordinates. Supply an approved centroid file first:
    # data/external/district_centroids.csv with District,latitude,longitude.
    centroids = OUT / "district_centroids.csv"
    if centroids.exists():
        c = pd.read_csv(centroids)
        rows = []
        for _, row in c.iterrows():
            try:
                payload = fetch_power_point(float(row.latitude), float(row.longitude))
                params = payload["properties"]["parameter"]
                for month in sorted(params["PRECTOTCORR"]):
                    rows.append({
                        "District": row.District,
                        "Year": 2025,
                        "Month": int(month),
                        "rainfall_mm": params["PRECTOTCORR"][month],
                        "temperature_c": params["T2M"][month],
                    })
                time.sleep(0.2)
            except Exception as exc:
                report.setdefault("errors", []).append({"District": row.District, "error": str(exc)})
        if rows:
            pd.DataFrame(rows).to_csv(OUT / "climate_monthly_district.csv", index=False)
            report["layers"]["nasa_power"] = {"status": "downloaded", "rows": len(rows)}
    else:
        report["layers"]["nasa_power"] = {"status": "waiting_for_district_centroids"}

    (OUT / "connector_report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
