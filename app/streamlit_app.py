from pathlib import Path
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
OUT = ROOT / "outputs"

st.set_page_config(
    page_title="RAPIS | Agricultural Productivity Intelligence",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Lightweight, responsive styling: visual clarity takes priority over decoration.
st.markdown("""
<style>
:root { --rapis-green: #146c43; --rapis-ink: #172b25; --rapis-muted: #61736b; }
.block-container {padding-top: 1.4rem; padding-bottom: 2.5rem; max-width: 1500px;}
.rapis-kicker {text-transform: uppercase; letter-spacing: .12em; font-size: .76rem; font-weight: 750; color: #146c43;}
.rapis-title {font-size: clamp(2rem, 3.5vw, 3.1rem); line-height: 1.08; font-weight: 800; color: #172b25; margin: .25rem 0 .6rem 0;}
.rapis-subtitle {font-size: 1.05rem; line-height: 1.6; color: #53665d; max-width: 950px;}
.rapis-banner {padding: 1.35rem 1.5rem; border: 1px solid #dce9e1; border-radius: 16px; background: linear-gradient(115deg,#f0f8f2 0%,#ffffff 78%); margin-bottom: 1.2rem;}
.rapis-note {padding: .85rem 1rem; background: #f5f8f6; border-left: 4px solid #146c43; border-radius: 6px; color: #34483e; font-size: .93rem;}
[data-testid="stMetric"] {border: 1px solid #e2eae5; padding: .9rem 1rem; border-radius: 12px; background: #fff;}
[data-testid="stMetricLabel"] {color: #61736b;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

@st.cache_data

def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)

@st.cache_data

def load_json(path: Path):
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as f:
        return json.load(f)

model = load_csv(DATA / "rapis_model_data.csv")
district_summary = load_csv(OUT / "district_summary.csv")
crop_summary = load_csv(OUT / "crop_summary.csv")
oof = load_csv(DATA / "ml_oof_predictions.csv")
importance = load_csv(DATA / "ml_feature_importance.csv")
metrics = load_json(DATA / "ml_validation_summary.json")

if model.empty or district_summary.empty or crop_summary.empty:
    st.error("RAPIS could not find one or more required processed data files. Check the project folder and README setup instructions.")
    st.stop()

required_cols = {"District", "Crop", "Yield_kg_ha", "Production_MT"}
missing_cols = required_cols - set(model.columns)
if missing_cols:
    st.error("The analytical dataset is missing required columns: " + ", ".join(sorted(missing_cols)))
    st.stop()

# Main header
st.markdown("""
<div class="rapis-banner">
  <div class="rapis-kicker">Team WINNER · NISR 2026 Big Data Hackathon · Track 1</div>
  <div class="rapis-title">Rwanda Agricultural Productivity<br>Intelligence System</div>
  <div class="rapis-subtitle">Explore observed crop productivity, compare agricultural practice indicators, inspect a district-held-out predictive benchmark, and transparently identify locations for further investigation.</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## RAPIS controls")
    st.caption("Use filters to explore the available crop-by-district evidence.")
    crops = sorted(model["Crop"].dropna().astype(str).unique())
    districts = sorted(model["District"].dropna().astype(str).unique())
    selected_crop = st.selectbox("Crop group", ["All crops"] + crops)
    selected_district = st.selectbox("District", ["All districts"] + districts)
    st.divider()
    st.markdown("**Evidence coverage**")
    st.write("Season B 2026 · aggregated tables")
    st.write(f"{model['District'].nunique()} districts · {model['Crop'].nunique()} crop groups")
    st.caption("This is a research prototype, not an official district ranking or a causal-impact model.")

filtered = model.copy()
if selected_crop != "All crops":
    filtered = filtered[filtered["Crop"].astype(str) == selected_crop]
if selected_district != "All districts":
    filtered = filtered[filtered["District"].astype(str) == selected_district]

# Small helper functions

def metric_or_na(value, suffix="", digits=0):
    try:
        if pd.isna(value):
            return "Not available"
        return f"{value:,.{digits}f}{suffix}"
    except (TypeError, ValueError):
        return "Not available"


def clean_chart(fig, height=430):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=55, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", color="#263b31"),
        title=dict(x=0.01, xanchor="left", font=dict(size=17)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#e8eee9", zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig


def district_targeting(data: pd.DataFrame, w_productivity=0.45, w_irrigation=0.30, w_erosion=0.25):
    x = data.copy()
    # Ensure weights are non-negative and sum to one before applying them.
    weights = [max(0.0, float(w_productivity)), max(0.0, float(w_irrigation)), max(0.0, float(w_erosion))]
    total = sum(weights)
    if total == 0:
        weights = [0.45, 0.30, 0.25]
        total = 1.0
    weights = [w / total for w in weights]
    x["productivity_gap"] = 1 - x["mean_yield_kg_ha"].rank(pct=True, method="average")
    x["irrigation_gap"] = 1 - x["mean_irrigation_pct"].rank(pct=True, method="average")
    x["erosion_pressure"] = x["severe_erosion_pct"].rank(pct=True, method="average")
    x["evidence_priority_score"] = 100 * (
        weights[0] * x["productivity_gap"] +
        weights[1] * x["irrigation_gap"] +
        weights[2] * x["erosion_pressure"]
    )
    x["priority_band"] = pd.cut(
        x["evidence_priority_score"], bins=[-0.01, 33.333, 66.667, 100.01],
        labels=["Lower evidence priority", "Medium evidence priority", "Higher evidence priority"]
    ).astype(str)
    return x.sort_values("evidence_priority_score", ascending=False), weights


tab_overview, tab_explore, tab_district, tab_target, tab_ml, tab_method = st.tabs([
    "Overview", "Productivity Explorer", "District Profiles", "Targeting Lab", "Predictive Benchmark", "Data & Methodology"
])

with tab_overview:
    st.markdown("### Decision overview")
    st.caption("The indicators below update with the crop and district filters in the sidebar.")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Crop × district records", f"{len(filtered):,}")
    k2.metric("Districts represented", f"{filtered['District'].nunique():,}")
    k3.metric("Crop groups represented", f"{filtered['Crop'].nunique():,}")
    k4.metric("Median observed yield", metric_or_na(filtered["Yield_kg_ha"].median(), " kg/ha"))

    left, right = st.columns([1.35, 1])
    with left:
        by_district = (filtered.groupby("District", as_index=False)
                       .agg(mean_yield_kg_ha=("Yield_kg_ha", "mean"), records=("Crop", "count"))
                       .sort_values("mean_yield_kg_ha", ascending=True))
        fig = px.bar(by_district, x="mean_yield_kg_ha", y="District", orientation="h",
                     color="mean_yield_kg_ha", color_continuous_scale="Greens",
                     hover_data={"mean_yield_kg_ha": ":,.1f", "records": True},
                     title="Mean observed yield by district",
                     labels={"mean_yield_kg_ha": "Mean yield (kg/ha)", "District": "District"})
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(clean_chart(fig, max(400, min(700, 24 * len(by_district) + 100))), use_container_width=True)
    with right:
        by_crop = (filtered.groupby("Crop", as_index=False)
                   .agg(mean_yield_kg_ha=("Yield_kg_ha", "mean"), districts=("District", "nunique"))
                   .sort_values("mean_yield_kg_ha", ascending=True).tail(12))
        fig = px.bar(by_crop, x="mean_yield_kg_ha", y="Crop", orientation="h",
                     color="mean_yield_kg_ha", color_continuous_scale="Greens",
                     hover_data={"mean_yield_kg_ha": ":,.1f", "districts": True},
                     title="Crop groups with higher observed yields",
                     labels={"mean_yield_kg_ha": "Mean yield (kg/ha)", "Crop": "Crop group"})
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(clean_chart(fig, 430), use_container_width=True)

    if selected_district != "All districts":
        drow = district_summary[district_summary["District"] == selected_district]
        if not drow.empty:
            r = drow.iloc[0]
            selected_rows = filtered[filtered["District"] == selected_district]
            selected_yield = selected_rows["Yield_kg_ha"].mean() if not selected_rows.empty else float("nan")
            st.markdown(f"#### Selected district: {selected_district}")
            a, b, c, d = st.columns(4)
            a.metric("Mean yield (current filters)", metric_or_na(selected_yield, " kg/ha"))
            b.metric("Irrigation indicator", metric_or_na(r["mean_irrigation_pct"], "%", 1))
            c.metric("Severe erosion indicator", metric_or_na(r["severe_erosion_pct"], "%", 2))
            d.metric("Crop groups in current view", metric_or_na(selected_rows["Crop"].nunique()))

    st.markdown("<div class='rapis-note'><b>How to interpret this page:</b> district means combine the crop groups available for each district. Since crops have different typical yields, compare districts within the same crop when making crop-specific conclusions. These are descriptive observations, not evidence that a practice caused a yield difference.</div>", unsafe_allow_html=True)

with tab_explore:
    st.markdown("### Compare observed agricultural outcomes")
    col1, col2, col3 = st.columns([1.2, 1, 1])
    with col1:
        exp_crop = st.selectbox("Crop group for comparison", ["All crops"] + crops, index=(crops.index(selected_crop) + 1 if selected_crop in crops else 0), key="exp_crop")
    with col2:
        measure = st.selectbox("Outcome measure", ["Yield (kg/ha)", "Production (MT)"], key="measure")
    with col3:
        top_n = st.slider("Number of districts", min_value=5, max_value=max(5, len(districts)), value=min(15, len(districts)), key="top_n")
    exp = model.copy()
    if exp_crop != "All crops":
        exp = exp[exp["Crop"] == exp_crop]
    metric_col = "Yield_kg_ha" if measure == "Yield (kg/ha)" else "Production_MT"
    metric_label = "Mean yield (kg/ha)" if metric_col == "Yield_kg_ha" else "Mean production (MT)"
    exp_summary = (exp.groupby("District", as_index=False)
                   .agg(Value=(metric_col, "mean"), Crop_records=("Crop", "count"))
                   .sort_values("Value", ascending=False).head(top_n).sort_values("Value", ascending=True))
    fig = px.bar(exp_summary, x="Value", y="District", orientation="h", color="Value",
                 color_continuous_scale="Greens", hover_data={"Value": ":,.2f", "Crop_records": True},
                 title=f"{metric_label} by district — {exp_crop}", labels={"Value": metric_label})
    fig.update_coloraxes(showscale=False)
    st.plotly_chart(clean_chart(fig, max(400, 24 * len(exp_summary) + 100)), use_container_width=True)
    st.dataframe(exp_summary.rename(columns={"Value": metric_label, "Crop_records": "Crop × district records"}), use_container_width=True, hide_index=True)
    st.download_button("Download comparison table (CSV)", exp_summary.to_csv(index=False).encode("utf-8"),
                       file_name="rapis_productivity_comparison.csv", mime="text/csv")

with tab_district:
    st.markdown("### District evidence profiles")
    profile_district = st.selectbox("Choose a district", districts,
                                    index=(districts.index(selected_district) if selected_district in districts else 0), key="profile_district")
    d = district_summary[district_summary["District"] == profile_district]
    crop_rows = model[model["District"] == profile_district].sort_values("Yield_kg_ha", ascending=False)
    if not d.empty:
        r = d.iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Mean yield across observed crops", metric_or_na(r["mean_yield_kg_ha"], " kg/ha"))
        c2.metric("Irrigation indicator", metric_or_na(r["mean_irrigation_pct"], "%", 1))
        c3.metric("Inorganic fertilizer indicator", metric_or_na(r["mean_inorganic_fertilizer_pct"], "%", 1))
        c4.metric("Organic fertilizer indicator", metric_or_na(r["mean_organic_fertilizer_pct"], "%", 1))
    left, right = st.columns([1.2, 1])
    with left:
        fig = px.bar(crop_rows.sort_values("Yield_kg_ha", ascending=True), x="Yield_kg_ha", y="Crop", orientation="h",
                     title=f"Observed yield by crop — {profile_district}", color="Yield_kg_ha", color_continuous_scale="Greens",
                     labels={"Yield_kg_ha": "Yield (kg/ha)", "Crop": "Crop group"})
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(clean_chart(fig, max(400, 25 * len(crop_rows) + 100)), use_container_width=True)
    with right:
        practice_cols = {
            "Irrigation": "mean_irrigation_pct",
            "Inorganic fertilizer": "mean_inorganic_fertilizer_pct",
            "Organic fertilizer": "mean_organic_fertilizer_pct",
            "Severe erosion": "severe_erosion_pct",
        }
        vals = pd.DataFrame({"Indicator": list(practice_cols), "Value (%)": [float(r[col]) for col in practice_cols.values()]})
        fig = px.bar(vals.sort_values("Value (%)"), x="Value (%)", y="Indicator", orientation="h",
                     title="Agricultural practice / erosion indicators", color="Value (%)", color_continuous_scale="Greens",
                     labels={"Value (%)": "Indicator value (%)"})
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(clean_chart(fig, 430), use_container_width=True)
    st.markdown("#### Crop-level evidence")
    display_cols = [c for c in ["District", "Crop", "Yield_kg_ha", "Production_MT", "irrigation_pct", "inorganic_fertilizer_farmers_pct", "organic_fertilizer_farmers_pct", "erosion_protected_pct"] if c in crop_rows.columns]
    st.dataframe(crop_rows[display_cols].rename(columns={
        "Yield_kg_ha": "Yield (kg/ha)", "Production_MT": "Production (MT)",
        "irrigation_pct": "Irrigation indicator (%)", "inorganic_fertilizer_farmers_pct": "Inorganic fertilizer indicator (%)",
        "organic_fertilizer_farmers_pct": "Organic fertilizer indicator (%)", "erosion_protected_pct": "Erosion protection indicator (%)"
    }).round(2), use_container_width=True, hide_index=True)
    st.download_button("Download district evidence (CSV)", crop_rows.to_csv(index=False).encode("utf-8"),
                       file_name=f"rapis_{profile_district.lower().replace(' ', '_')}_evidence.csv", mime="text/csv")

with tab_target:
    st.markdown("### Transparent evidence-priority explorer")
    st.write("This tool identifies districts for further investigation using lower observed yield, lower irrigation indicators and higher severe-erosion indicators. It is not an official allocation rule or a validated estimate of intervention impact.")
    with st.expander("Adjust score weights", expanded=True):
        w1, w2, w3 = st.columns(3)
        wp = w1.slider("Productivity gap weight", 0, 100, 45, 5)
        wi = w2.slider("Irrigation gap weight", 0, 100, 30, 5)
        we = w3.slider("Severe erosion weight", 0, 100, 25, 5)
        if wp + wi + we == 0:
            st.warning("At least one weight must be greater than zero. Default weights will be used until then.")
    target, norm_weights = district_targeting(district_summary, wp, wi, we)
    st.caption(f"Normalized weights used: productivity {norm_weights[0]:.0%} · irrigation {norm_weights[1]:.0%} · severe erosion {norm_weights[2]:.0%}.")
    high = int((target["priority_band"] == "Higher evidence priority").sum())
    mid = int((target["priority_band"] == "Medium evidence priority").sum())
    low = int((target["priority_band"] == "Lower evidence priority").sum())
    a, b, c = st.columns(3)
    a.metric("Higher evidence-priority districts", high)
    b.metric("Medium evidence-priority districts", mid)
    c.metric("Lower evidence-priority districts", low)
    left, right = st.columns([1.2, 1])
    with left:
        fig = px.scatter(target, x="mean_irrigation_pct", y="mean_yield_kg_ha", size="severe_erosion_pct",
                         color="priority_band", hover_name="District", hover_data={"evidence_priority_score": ":.1f"},
                         title="District evidence landscape",
                         labels={"mean_irrigation_pct": "Irrigation indicator (%)", "mean_yield_kg_ha": "Mean yield across observed crops (kg/ha)", "priority_band": "Evidence band"},
                         color_discrete_map={"Higher evidence priority": "#b45309", "Medium evidence priority": "#3977a8", "Lower evidence priority": "#16845b"})
        st.plotly_chart(clean_chart(fig, 480), use_container_width=True)
    with right:
        fig = px.bar(target.head(12).sort_values("evidence_priority_score"), x="evidence_priority_score", y="District", orientation="h",
                     color="evidence_priority_score", color_continuous_scale="Oranges", title="12 highest evidence-priority scores",
                     labels={"evidence_priority_score": "Evidence-priority score (0–100)"})
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(clean_chart(fig, 480), use_container_width=True)
    st.dataframe(target[["District", "mean_yield_kg_ha", "mean_irrigation_pct", "severe_erosion_pct", "evidence_priority_score", "priority_band"]].round(2), use_container_width=True, hide_index=True)
    st.download_button("Download evidence-priority table (CSV)", target.to_csv(index=False).encode("utf-8"),
                       file_name="rapis_evidence_priority.csv", mime="text/csv")
    st.markdown("<div class='rapis-note'><b>Interpretation safeguard:</b> score weights are transparent design assumptions. A high score means the district meets the selected descriptive criteria; it does not prove that an intervention will have the greatest impact there.</div>", unsafe_allow_html=True)

with tab_ml:
    st.markdown("### District-held-out predictive benchmark")
    st.write("RAPIS includes an Extra Trees regression benchmark. Grouped cross-validation holds out entire districts during evaluation, reducing leakage from observations belonging to the same district across train and test folds.")
    if metrics:
        a, b, c, d = st.columns(4)
        a.metric("Mean cross-validation R²", metric_or_na(metrics.get("r2"), digits=3))
        b.metric("Mean absolute error", metric_or_na(metrics.get("mae_kg_ha"), " kg/ha"))
        c.metric("Observations", metric_or_na(metrics.get("observations")))
        d.metric("Districts held out by group", metric_or_na(metrics.get("districts")))
        if not oof.empty:
            left, right = st.columns([1.15, 1])
            with left:
                fig = px.scatter(oof, x="Yield_kg_ha", y="OOF_Predicted_Yield_kg_ha", color="Crop",
                                 hover_data=["District", "OOF_Absolute_Error_kg_ha"], opacity=.72,
                                 title="Observed vs out-of-fold predicted yield",
                                 labels={"Yield_kg_ha": "Observed yield (kg/ha)", "OOF_Predicted_Yield_kg_ha": "Out-of-fold prediction (kg/ha)"})
                lo = float(min(oof["Yield_kg_ha"].min(), oof["OOF_Predicted_Yield_kg_ha"].min()))
                hi = float(max(oof["Yield_kg_ha"].max(), oof["OOF_Predicted_Yield_kg_ha"].max()))
                fig.add_trace(go.Scatter(x=[lo, hi], y=[lo, hi], mode="lines", name="Ideal prediction", line=dict(dash="dash", color="#53665d")))
                st.plotly_chart(clean_chart(fig, 470), use_container_width=True)
            with right:
                if not importance.empty:
                    imp = importance.head(12).sort_values("Importance", ascending=True)
                    fig = px.bar(imp, x="Importance", y="Feature", orientation="h", color="Importance", color_continuous_scale="Greens",
                                 title="Top model feature-importance values", labels={"Importance": "Model importance", "Feature": "Feature"})
                    fig.update_coloraxes(showscale=False)
                    st.plotly_chart(clean_chart(fig, 470), use_container_width=True)
            if "fold_mae_kg_ha" in metrics and "fold_r2" in metrics:
                fold = pd.DataFrame({"Fold": range(1, len(metrics["fold_mae_kg_ha"]) + 1), "MAE (kg/ha)": metrics["fold_mae_kg_ha"], "R²": metrics["fold_r2"]})
                st.markdown("#### Fold-level performance")
                st.dataframe(fold.round(3), use_container_width=True, hide_index=True)
        st.markdown("<div class='rapis-note'><b>Limitations:</b> this benchmark uses aggregated data from one season. It is a predictive exercise, not a causal model or a guarantee of future harvest performance. Validate on additional seasons and compare against a simple baseline before operational use.</div>", unsafe_allow_html=True)
    else:
        st.warning("Validation summary not found. Run `python src/validated_ml.py` from the project root to regenerate it.")

with tab_method:
    st.markdown("### Data, definitions and responsible use")
    st.markdown("#### Data coverage")
    coverage = pd.DataFrame([
        {"Item": "Primary source", "Current status": "Workbook supplied with project; source tables and citations must be checked against the original NISR publication."},
        {"Item": "Analytical unit", "Current status": "Crop-by-district aggregated observations."},
        {"Item": "Coverage", "Current status": f"{model['District'].nunique()} districts, {model['Crop'].nunique()} crop groups, {len(model):,} records in the processed table."},
        {"Item": "External climate / soil / satellite data", "Current status": "Not represented as connected observations unless the relevant source file is present and documented."},
        {"Item": "Administrative boundary map", "Current status": "Not rendered unless an approved district boundary GeoJSON is added."},
    ])
    st.dataframe(coverage, use_container_width=True, hide_index=True)
    st.markdown("#### Interpretation rules")
    st.markdown("""
- Yield is displayed in kilograms per hectare (kg/ha); production is displayed in metric tonnes (MT).
- District-wide mean yield combines the crop groups available for that district. Use crop-specific comparisons when the goal is to compare like with like.
- Agricultural practice indicators are exploratory contextual variables. Their relationships with yield are not causal estimates.
- The evidence-priority score is a transparent project-defined screening tool, not an official government ranking or a budget allocation formula.
- Machine-learning performance comes from grouped cross-validation on one season of aggregated data and should be tested on additional seasons.
- RAPIS does not fabricate climate, soil, satellite or district-boundary data. Missing layers must be connected from approved sources and documented before use.
""")
    st.markdown("#### Downloads")
    d1, d2, d3 = st.columns(3)
    d1.download_button("Processed crop × district data", model.to_csv(index=False).encode("utf-8"), file_name="rapis_model_data.csv", mime="text/csv")
    d2.download_button("District summary", district_summary.to_csv(index=False).encode("utf-8"), file_name="rapis_district_summary.csv", mime="text/csv")
    d3.download_button("Crop summary", crop_summary.to_csv(index=False).encode("utf-8"), file_name="rapis_crop_summary.csv", mime="text/csv")
    st.markdown("#### Reproducibility")
    st.code("pip install -r requirements.txt\npython src/validated_ml.py\nstreamlit run app/streamlit_app.py", language="bash")
    st.caption("The R/Shiny version is retained in r_shiny/. This Streamlit app is the recommended single entry point for a simple public deployment.")

st.divider()
st.caption("RAPIS · Team WINNER · NISR 2026 Big Data Hackathon · Track 1: Agricultural Productivity · Analytical prototype")
