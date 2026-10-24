# RAPIS — NISR 2026 Hackathon Alignment & Action Plan

## Official competition basis

RAPIS is entered under **Track 1: Agricultural Productivity** of the NISR 2026 Big Data Hackathon.

NISR states that Track 1 solutions should address real agricultural challenges in Rwanda and may focus on:
- small-scale irrigation;
- soil conservation and fertility management;
- post-harvest collection and storage;
- agricultural productivity, processing and value addition;
- export market opportunities for Rwandan agricultural products.

NISR also requires the solution to be informed by NISR data, with optional open/public agricultural, food-security or climate data, and encourages tangible practical impact for farmers, agricultural planners or policymakers.

Official source: https://statistics.gov.rw/about/hackathon/2026-hackathon-competition

## The five NISR judging criteria

| Criterion | Weight | What RAPIS must demonstrate | Current implementation | Final action |
|---|---:|---|---|---|
| Problem Understanding & Relevance | 20 | Clear agricultural problem + NST2/Vision 2050 relevance | Agricultural productivity gap and intervention evidence | Lead presentation with one concrete decision question |
| Data Use & Methodology | 20 | NISR data, sound preprocessing, appropriate analytical/AI methods | SAS Season B 2026 + district practice indicators + district-held-out ML | Add data dictionary, provenance and validation explanation |
| Tech Innovation | 20 | Relevant technology and creative approach | R/Shiny + ML + targeting + external-data architecture | Add map, scenario analysis and alert prototype |
| Usability & Design | 20 | Intuitive tool and clear visualisation | Professional Shiny workflow and interactive charts | Keep demo focused on one user journey |
| Tangible Impact | 20 | Potential real-world use | District evidence-priority workflow | Define measurable implementation KPIs and user actions |

## Recommended competition positioning

### One-sentence value proposition

**RAPIS turns NISR agricultural statistics into a transparent district decision-support workflow for identifying productivity gaps, examining observable constraints, validating predictive signals and targeting further agricultural analysis.**

### The decision question

> **Where are agricultural productivity gaps concentrated, what observable agricultural conditions are associated with those gaps, and where should planners investigate or target additional intervention analysis?**

This is intentionally narrower than claiming that RAPIS proves causal intervention effects.

## Track 1 coverage matrix

### 1. Small-scale irrigation

**Current:** irrigation coverage is included in the district evidence and targeting score.

**Upgrade:** add a map showing irrigation coverage against observed productivity and allow users to identify districts with low irrigation and low observed productivity.

**Responsible claim:** association/evidence priority, not causal impact.

### 2. Soil conservation and fertility

**Current:** erosion protection and severe-erosion indicators are included.

**Upgrade:** connect approved soil variables when available: soil organic carbon, pH, texture and relevant nutrient indicators.

### 3. Post-harvest collection and storage

**Current gap:** not sufficiently represented in the present dataset.

**Recommendation:** do not fabricate this layer. Add a clearly labelled future module and connect an approved NISR/open dataset if available.

### 4. Processing and value addition

**Current gap:** not sufficiently represented.

**Recommendation:** add a future module using approved data on crop processing, agro-processing facilities, value-chain participation or production-to-market pathways.

### 5. Export market opportunities

**Current gap:** not currently modelled.

**Recommendation:** add a future export-opportunity module using public trade/export data, linking priority crops to production capacity and external-market demand.

## NISR-required submission readiness

NISR's 2026 announcement says submissions are expected to include:
1. a **public GitHub link**;
2. a **deployed application link**;
3. **documentation**.

Before submission, the team should verify all three are publicly accessible and tested from a clean browser/device.

## Data integrity and AI disclosure

NISR explicitly states that AI tools may be used as assistants, but participants remain responsible for the submitted work and must disclose AI use. The team should therefore include an **AI Assistance Disclosure** in the repository and documentation.

Recommended wording:

> AI-assisted tools were used during software development, documentation refinement and code-review support. The team reviewed, tested and remains responsible for all submitted code, data processing, statistical interpretation, visualisations and claims. Source data and external references are acknowledged in the repository.

Do not claim that AI generated or verified statistical findings independently.

## What judges should see in the first 90 seconds

1. **Problem:** a specific Rwanda agricultural productivity decision problem.
2. **NISR evidence:** one clear district/crop finding.
3. **Innovation:** validated district-held-out ML benchmark.
4. **Decision support:** transparent evidence-priority targeting.
5. **Impact:** what a planner can do next with the output.

## Recommended final demo sequence

**Decision Center → Rwanda/District map → Validated ML → Targeting Lab → Scenario → Impact/Policy**

Avoid spending presentation time on technical setup or every dashboard page.

## Claims that must not be made

Do not say:
- irrigation causes a specific yield increase based on the current cross-sectional data;
- the ML model forecasts future harvests without multi-season validation;
- RAPIS is an official government priority ranking;
- climate risk is measured before climate data are connected;
- external datasets were used if they are only planned connectors.

## Evidence language to use

Prefer:
- “observed productivity”;
- “district-held-out predictive benchmark”;
- “exploratory association”;
- “evidence-priority score”;
- “decision-support prototype”;
- “candidate intervention area for further assessment.”

## 30-day technical roadmap

### Phase 1 — submission hardening
- freeze data version;
- document all source tables;
- verify reproducibility;
- test Shiny app from a clean installation;
- publish GitHub repository;
- deploy application;
- add AI disclosure;
- prepare 90-second demo.

### Phase 2 — geospatial upgrade
- connect official NISR administrative boundaries;
- add district map;
- add sector/cell granularity if permitted data are available;
- show productivity and irrigation layers.

### Phase 3 — climate/soil/satellite upgrade
- rainfall and dry-spell indicators;
- soil properties;
- elevation/slope;
- Sentinel-2 vegetation/crop-condition indicators;
- multi-season validation.

### Phase 4 — Track 1 expansion
- post-harvest/storage module;
- value-addition module;
- export-opportunity module.

## Source

NISR. 2026 Hackathon Competition. National Institute of Statistics of Rwanda.
https://statistics.gov.rw/about/hackathon/2026-hackathon-competition
