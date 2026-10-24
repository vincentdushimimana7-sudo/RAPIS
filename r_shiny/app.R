# RAPIS — Rwanda Agricultural Productivity Intelligence System
# NISR 2026 Big Data Hackathon | Track 1 | Team WINNER

required <- c("shiny","bslib","plotly","DT","dplyr","tidyr","readr","ggplot2","scales","htmltools","jsonlite","leaflet","sf")
missing <- required[!vapply(required, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing)) stop("Install required packages: ", paste(missing, collapse = ", "))

library(shiny); library(bslib); library(plotly); library(DT); library(dplyr)
library(tidyr); library(readr); library(ggplot2); library(scales); library(htmltools); library(jsonlite)
if (requireNamespace("leaflet", quietly=TRUE)) library(leaflet)
if (requireNamespace("sf", quietly=TRUE)) library(sf)

BASE <- normalizePath(file.path(getwd(), ".."), mustWork = FALSE)
if (!file.exists(file.path(BASE, "data", "processed", "rapis_model_data.csv"))) BASE <- normalizePath(".", mustWork = FALSE)

model <- read_csv(file.path(BASE, "data/processed/rapis_model_data.csv"), show_col_types = FALSE)
district <- read_csv(file.path(BASE, "outputs/district_summary.csv"), show_col_types = FALSE)
crop <- read_csv(file.path(BASE, "outputs/crop_summary.csv"), show_col_types = FALSE)

ml_metrics_file <- file.path(BASE, "data/processed/ml_validation_summary.json")
ml_metrics <- if (file.exists(ml_metrics_file)) fromJSON(ml_metrics_file) else NULL
imp_file <- file.path(BASE, "data/processed/ml_feature_importance.csv")
importance <- if (file.exists(imp_file)) read_csv(imp_file, show_col_types = FALSE) else tibble(Feature=character(), Importance=double())

evidence_files <- c(
  climate = file.path(BASE, "data/external/climate_district.csv"),
  soil = file.path(BASE, "data/external/soil_district.csv"),
  elevation = file.path(BASE, "data/external/elevation_district.csv"),
  satellite = file.path(BASE, "data/external/satellite_district.csv"),
  boundary = file.path(BASE, "data/external/rwanda_districts.geojson")
)
external_status <- tibble(
  Layer = c("Rainfall / climate", "Soil properties", "Elevation / terrain", "Satellite indicators", "NISR administrative boundaries"),
  File = basename(evidence_files),
  Status = ifelse(file.exists(evidence_files), "CONNECTED", "READY TO CONNECT"),
  Source = c("NASA POWER / approved climate source", "ISRIC SoilGrids", "Approved DEM source", "Copernicus Sentinel-2 / approved source", "NISR GIS Open Data")
)
nisr_latest <- tibble(
  Indicator = c("Improved seeds", "Organic fertilizer", "Inorganic fertilizer", "Pesticides", "Irrigation", "Agroforestry", "Mechanical equipment"),
  Season_B_2026 = c(20.9,81.3,57.5,39.1,13.1,58.0,1.8),
  Unit = rep("% of farmers",7),
  Source = rep("NISR Seasonal Agricultural Survey — Season B 2026",7)
)

fmt <- function(x, digits=0) format(round(x,digits), big.mark=",", nsmall=digits, trim=TRUE)
metric_card <- function(title, value, subtitle="", tone="") div(class=paste("metric-card", tone), div(class="metric-title",title), div(class="metric-value",value), div(class="metric-sub",subtitle))

features <- c("irrigation_pct","inorganic_fertilizer_farmers_pct","organic_fertilizer_farmers_pct","erosion_protected_pct","agroforestry_pct","mechanical_equipment_pct")
fit <- lm(log1p(Yield_kg_ha) ~ irrigation_pct + inorganic_fertilizer_farmers_pct + organic_fertilizer_farmers_pct + erosion_protected_pct + agroforestry_pct + mechanical_equipment_pct + Crop, data=model)
model_r2 <- summary(fit)$r.squared

# Transparent targeting score: descriptive prioritisation, not causal impact.
targeting <- district |> mutate(
  productivity_gap = 1 - percent_rank(mean_yield_kg_ha),
  irrigation_gap = 1 - percent_rank(mean_irrigation_pct),
  erosion_pressure = percent_rank(severe_erosion_pct),
  targeting_score = 100 * (0.45*productivity_gap + 0.30*irrigation_gap + 0.25*erosion_pressure),
  decision_band = case_when(targeting_score >= 66 ~ "High evidence priority", targeting_score >= 33 ~ "Medium evidence priority", TRUE ~ "Lower evidence priority")
) |> arrange(desc(targeting_score))

ui <- page_navbar(
  title=div(class="brand", span(class="brand-main","RAPIS"), span(class="brand-sub","Rwanda Agricultural Productivity Intelligence System")),
  theme=bs_theme(version=5, bootswatch="flatly", primary="#087f5b", secondary="#16324f", success="#2f9e44") |> bs_add_rules("$enable-shadows: true;"),
  header=tagList(tags$link(rel="stylesheet",type="text/css",href="custom.css"), nav_spacer(), span(class="season-pill","NISR SAS • Season B 2026")),

  nav_panel("Decision Center",
    layout_sidebar(sidebar=sidebar(
      h5("Decision filters"),
      selectInput("crop","Crop group",c("All crops",sort(unique(model$Crop)))),
      selectInput("district","District",c("All districts",sort(unique(model$District)))),
      checkboxInput("show_note","Show evidence safeguards",TRUE),
      hr(), div(class="sidebar-note",strong("RAPIS objective"),p("Turn official agricultural statistics into transparent evidence for productivity planning, climate resilience and intervention design."))
    ),
    div(class="hero",h1("From agricultural statistics to actionable intelligence"),p("A competition-ready decision-support prototype linking NISR productivity evidence with validated machine learning, intervention targeting and a roadmap for climate/geospatial integration."),div(class="hero-tags",span("NISR EVIDENCE"),span("VALIDATED ML"),span("TARGETING"),span("CLIMATE-READY"))),
    uiOutput("kpis"),
    layout_columns(card(card_header("Observed productivity by district"),plotlyOutput("district_plot",height="430px")),card(card_header("Crop productivity profile"),plotlyOutput("crop_plot",height="430px")),col_widths=c(7,5)),
    conditionalPanel("input.show_note",div(class="method-note",strong("Evidence safeguard: "),"Current results are descriptive Season B 2026 aggregated observations. They do not establish causal effects."))
    )
  ),

  nav_panel("Productivity Explorer",
    layout_sidebar(sidebar=sidebar(selectInput("explore_crop","Crop",c("All crops",sort(unique(model$Crop)))),radioButtons("metric","Measure",c("Yield (kg/ha)"="Yield_kg_ha","Production (MT)"="Production_MT")),sliderInput("topn","Show districts",5,30,15,1),hr(),p(class="small-muted","Compare observed outcomes without interpreting the display as a causal or official ranking.")),
    card(card_header("District comparison"),plotlyOutput("explore_plot",height="620px")),card(card_header("Selected evidence"),DTOutput("explore_table"))
  ),

  nav_panel("Validated ML",
    div(class="section-intro",h2("District-held-out predictive benchmark"),p("RAPIS uses group-aware cross-validation: entire districts are held out from each test fold. This is stricter than randomly splitting individual observations when district-level generalisation matters.")),
    uiOutput("ml_kpis"),
    layout_columns(card(card_header("Observed vs out-of-fold prediction"),plotlyOutput("ml_scatter",height="450px")),card(card_header("Feature importance"),plotlyOutput("importance_plot",height="450px")),col_widths=c(7,5)),
    card(card_header("Validation folds"),DTOutput("ml_table")),
    div(class="method-note",strong("Interpretation: "),"The model is predictive, not causal. It is trained on one aggregated season, so its performance must be revalidated on additional seasons and external climate/soil/satellite covariates before operational use.")
  ),

  nav_panel("Drivers & Practices",
    layout_sidebar(sidebar=sidebar(selectInput("driver","Indicator",c("Irrigation"="irrigation_pct","Inorganic fertilizer"="inorganic_fertilizer_farmers_pct","Organic fertilizer"="organic_fertilizer_farmers_pct","Erosion protection"="erosion_protected_pct","Agroforestry"="agroforestry_pct","Mechanical equipment"="mechanical_equipment_pct")),checkboxInput("trend","Show exploratory trend",TRUE),hr(),p(class="small-muted","Associations are exploratory; fitted lines do not identify causal effects."))),
    card(card_header("Observed relationship with yield"),plotlyOutput("driver_plot",height="570px")),card(card_header("Correlation evidence"),DTOutput("corr_table"))
  ),

  nav_panel("District Profile",
    layout_sidebar(sidebar=sidebar(selectInput("profile_district","District",sort(unique(model$District)))),uiOutput("profile_header"),layout_columns(card(card_header("Crop profile"),plotlyOutput("profile_crop_plot",height="430px")),card(card_header("Practice profile"),plotlyOutput("profile_practice_plot",height="430px")),col_widths=c(7,5)),card(card_header("Evidence table"),DTOutput("profile_table")),downloadButton("download_profile","Download district evidence"))
  ),

  nav_panel("Targeting Lab",
    div(class="section-intro",h2("Evidence-based intervention targeting"),p("This transparent score combines lower observed productivity, lower irrigation coverage and higher severe-erosion pressure. It is a planning aid—not a causal impact estimate or official government prioritisation.")),
    layout_columns(card(card_header("District evidence-priority matrix"),plotlyOutput("target_plot",height="540px")),card(card_header("Targeting logic"),uiOutput("target_logic"),br(),downloadButton("download_targeting","Download targeting table")),col_widths=c(8,4)),
    card(card_header("District targeting table"),DTOutput("target_table"))
  ),

  nav_panel("Rwanda Evidence Map",
    div(class="section-intro",h2("District evidence map"),p("A spatial decision layer for RAPIS. When the official NISR boundary GeoJSON is connected, district evidence can be mapped directly without using invented coordinates.")),
    uiOutput("map_status"),
    conditionalPanel("output.map_ready", leafletOutput("evidence_map",height="650px")),
    conditionalPanel("!output.map_ready", card(card_header("Official boundary connection"),div(class="map-placeholder",h3("NISR GIS layer ready to connect"),p("RAPIS is configured to consume official NISR administrative geography. The current package does not fabricate district polygons or coordinates. Run scripts/fetch_external_data.py after reviewing the source and saving the approved boundary layer under data/external/."),tags$ul(tags$li("Source: NISR GIS Open Data"),tags$li("Spatial reference target: WGS 84 / EPSG:4326"),tags$li("Map joins on district name / official identifiers")))),
    card(card_header("How the map supports decisions"),div(class="prose",tags$ol(tags$li(strong("Locate")," — identify districts with lower observed productivity."),tags$li(strong("Diagnose")," — inspect irrigation, erosion and input indicators."),tags$li(strong("Prioritise further analysis")," — use the transparent evidence-priority score."),tags$li(strong("Verify")," — overlay approved climate, soil or satellite evidence before operational use."))))
  ),

  nav_panel("Scenario Lab",
    div(class="section-intro",h2("What-if productivity scenario"),p("Explore how changing observed practice indicators changes the model-based productivity estimate. This is a sensitivity/scenario tool, not a causal impact calculator.")),
    layout_sidebar(sidebar=sidebar(
      selectInput("scenario_crop","Crop group",sort(unique(model$Crop))),
      sliderInput("scenario_irrigation","Irrigation coverage (%)",0,100,25,1),
      sliderInput("scenario_inorganic","Inorganic fertilizer users (%)",0,100,55,1),
      sliderInput("scenario_erosion","Erosion-protected plots (%)",0,100,70,1),
      sliderInput("scenario_agro","Agroforestry (%)",0,100,58,1),
      hr(),p(class="small-muted","The scenario is evaluated against the fitted model used for exploratory sensitivity analysis. It does not claim that changing one practice will causally produce the displayed yield.")),
    uiOutput("scenario_kpis"),
    layout_columns(card(card_header("Scenario sensitivity"),plotlyOutput("scenario_plot",height="470px")),card(card_header("Decision interpretation"),uiOutput("scenario_interpretation")),col_widths=c(8,4)),
    card(card_header("Scenario assumptions"),DTOutput("scenario_table"))
  ),

  nav_panel("NISR 2026 Scorecard",
    div(class="section-intro",h2("Built around the NISR 2026 judging criteria"),p("NISR evaluates Problem Understanding & Relevance, Data Use & Methodology, Tech Innovation, Usability & Design, and Tangible Impact — 20 points each. RAPIS maps each criterion to visible evidence in the application.")),
    layout_columns(
      card(card_header("Five criteria × 20 points"),
        div(class="score-grid",
          div(class="score-item",strong("20"),span("Problem & relevance"),p("Track 1 agricultural productivity + NST2/Vision 2050")),
          div(class="score-item",strong("20"),span("Data & methodology"),p("NISR evidence + preprocessing + district-held-out validation")),
          div(class="score-item",strong("20"),span("Tech innovation"),p("R/Shiny + ML + transparent targeting + geospatial roadmap")),
          div(class="score-item",strong("20"),span("Usability & design"),p("Decision Center + filters + interactive evidence")),
          div(class="score-item",strong("20"),span("Tangible impact"),p("Planner-facing targeting and decision workflow"))
        )
      ),
      card(card_header("Track 1 coverage"),
        tags$ul(
          tags$li(strong("Small-scale irrigation: "),"current district evidence and targeting"),
          tags$li(strong("Soil conservation/fertility: "),"erosion evidence; soil connector ready"),
          tags$li(strong("Post-harvest/storage: "),"planned module pending approved data"),
          tags$li(strong("Processing/value addition: "),"planned module pending approved data"),
          tags$li(strong("Export opportunities: "),"planned module pending approved trade data")
        ),
        div(class="method-note",strong("Integrity rule: "),"planned modules are labelled as planned; RAPIS does not fabricate missing observations."))
    ),
    card(card_header("Latest official NISR agriculture benchmark"),div(class="method-note",p("NISR reports that Season B 2026 covered all 30 districts. The national benchmark includes 13.1% irrigation adoption, 20.9% improved-seed use, 57.5% inorganic-fertilizer use and 81.3% organic-fertilizer use."),p(a(href="https://statistics.gov.rw/statistical-publications/agriculture-environment/seasonal-agricultural-survey-season-b-2026",target="_blank","Verify against NISR Season B 2026 release before final submission."))),DTOutput("nisr_latest_table")),
    card(card_header("Submission readiness"),DTOutput("nisr_readiness_table")),
    div(class="method-note",strong("Source: "),a(href="https://statistics.gov.rw/about/hackathon/2026-hackathon-competition",target="_blank","NISR 2026 Hackathon Competition"),". The project documentation contains the full alignment and action plan.")
  ),

  nav_panel("Climate & Geospatial Readiness",
    div(class="section-intro",h2("Next-generation data layer"),p("RAPIS is structured to add rainfall, soil, terrain, satellite and official administrative geography without fabricating missing observations.")),
    card(card_header("Data connection status"),DTOutput("external_table")),
    layout_columns(card(card_header("What the new layer enables"),div(class="prose",tags$ul(tags$li(strong("Climate stress:")," rainfall totals, anomalies and dry-spell indicators."),tags$li(strong("Soil constraints:")," pH, organic carbon, texture and nutrient indicators."),tags$li(strong("Terrain:")," elevation and slope to improve spatial targeting."),tags$li(strong("Satellite signals:")," vegetation and crop-condition indicators such as NDVI."),tags$li(strong("Geospatial targeting:")," district/sector/cell evidence linked to official NISR boundaries.")))),card(card_header("Current connectors"),div(class="prose",p(strong("NISR GIS:")," official administrative boundary service."),p(strong("NASA POWER:")," climate data connector template."),p(strong("ISRIC SoilGrids:")," soil-data connector template; its REST API is currently subject to availability constraints."),p(strong("Copernicus Sentinel-2:")," satellite connector template requiring appropriate access credentials/data service.")))),col_widths=c(7,5)),
    card(card_header("External-data contract"),div(class="prose",p("Place approved district-level files in data/external/ using the schemas documented in data/external/README.md. RAPIS automatically detects connected layers.")),downloadButton("download_external_template","Download external-data status"))
  ),

  nav_panel("Methodology & Impact",
    layout_columns(card(card_header("Current evidence"),div(class="prose",tags$ul(tags$li("NISR Seasonal Agricultural Survey — Season B 2026 tables"),tags$li("522 crop × district observations"),tags$li("30 districts and 19 crop groups"),tags$li("Agricultural practice indicators covering irrigation, fertilizer, erosion, agroforestry and mechanisation")))),card(card_header("Analytical safeguards"),div(class="prose",tags$ul(tags$li("District-held-out validation for the predictive benchmark."),tags$li("Observed, predictive and causal claims are explicitly separated."),tags$li("Crop composition is accounted for in the ML benchmark."),tags$li("External layers are marked unavailable until actually connected."),tags$li("Future models should be revalidated across seasons and time.")))),col_widths=c(6,6)),
    card(card_header("National development relevance"),div(class="prose",p(strong("NST2 2024–2029: "),"Rwanda's agriculture strategy emphasises higher productivity, climate resilience, modernisation, irrigation and improved inputs."),p(strong("PSTA 5 / climate-smart agriculture: "),"RAPIS can help connect production evidence to resource and resilience planning."),p(strong("Vision 2050: "),"the platform supports data-driven, technology-enabled and productive agriculture."))),
    card(card_header("Competition pitch"),div(class="pitch-box",h3("The problem"),p("Agricultural statistics are valuable, but decision-makers need a faster way to identify where productivity is low, which observed practices differ, and where additional climate and spatial evidence should be integrated."),h3("The RAPIS solution"),p("A transparent analytics layer that starts with official NISR evidence, adds district-held-out predictive modelling, exposes uncertainty and creates a practical pathway to climate-smart geospatial targeting."),h3("The innovation"),p("RAPIS does not stop at a dashboard: it creates a reproducible evidence pipeline that can evolve from descriptive statistics to validated multi-source decision support.")))
  ),
  footer=div(class="footer-note","RAPIS • Team WINNER • NISR 2026 Big Data Hackathon • Track 1 • Prototype based on Season B 2026 aggregated evidence")
)

server <- function(input, output, session) {
  filtered_main <- reactive({x<-model;if(input$crop!="All crops")x<-filter(x,Crop==input$crop);if(input$district!="All districts")x<-filter(x,District==input$district);x})
  output$kpis <- renderUI({x<-filtered_main();tagList(div(class="metric-grid",metric_card("Observations",fmt(nrow(x)),"crop × district records"),metric_card("Districts",fmt(n_distinct(x$District)),"represented"),metric_card("Crop groups",fmt(n_distinct(x$Crop)),"represented"),metric_card("Median yield",paste0(fmt(median(x$Yield_kg_ha,na.rm=TRUE))," kg/ha"),"observed median")))})
  output$district_plot <- renderPlotly({x<-filtered_main()|>group_by(District)|>summarise(Yield=mean(Yield_kg_ha,na.rm=TRUE),.groups="drop")|>arrange(Yield);plot_ly(x,x=~Yield,y=~reorder(District,Yield),type="bar",orientation="h",hovertemplate="%{y}<br>Mean yield: %{x:,.0f} kg/ha<extra></extra>")|>layout(xaxis=list(title="Mean observed yield (kg/ha)"),yaxis=list(title=""),margin=list(l=110))})
  output$crop_plot <- renderPlotly({x<-filtered_main()|>group_by(Crop)|>summarise(Yield=mean(Yield_kg_ha,na.rm=TRUE),.groups="drop")|>arrange(desc(Yield))|>slice_head(n=10);plot_ly(x,x=~Yield,y=~reorder(Crop,Yield),type="bar",orientation="h",hovertemplate="%{y}<br>%{x:,.0f} kg/ha<extra></extra>")|>layout(xaxis=list(title="Mean observed yield (kg/ha)"),yaxis=list(title=""),margin=list(l=125))})
  explore_data <- reactive({x<-model;if(input$explore_crop!="All crops")x<-filter(x,Crop==input$explore_crop);x|>group_by(District)|>summarise(Value=mean(.data[[input$metric]],na.rm=TRUE),Records=n(),.groups="drop")|>arrange(desc(Value))|>slice_head(n=input$topn)})
  output$explore_plot <- renderPlotly({x<-explore_data();label<-if(input$metric=="Yield_kg_ha")"Mean yield (kg/ha)" else "Mean production (MT)";plot_ly(x,x=~Value,y=~reorder(District,Value),type="bar",orientation="h",hovertemplate="%{y}<br>%{x:,.1f}<extra></extra>")|>layout(xaxis=list(title=label),yaxis=list(title=""),margin=list(l=110))})
  output$explore_table <- renderDT({datatable(explore_data(),rownames=FALSE,options=list(pageLength=15,dom='tip'))|>formatRound("Value",1)})

  output$ml_kpis <- renderUI({if(is.null(ml_metrics)) return(div(class="method-note","Validated ML artifact not found. Run src/validated_ml.py."));div(class="metric-grid",metric_card("5-fold R²",sprintf("%.3f",ml_metrics$r2),"district-held-out mean", "accent"),metric_card("MAE",paste0(fmt(ml_metrics$mae_kg_ha)," kg/ha"),"out-of-fold mean"),metric_card("Districts",fmt(ml_metrics$districts),"held out by group"),metric_card("Observations",fmt(ml_metrics$observations),"training evidence"))})
  oof_file <- file.path(BASE,"data/processed/ml_oof_predictions.csv")
  output$ml_scatter <- renderPlotly({req(file.exists(oof_file));x<-read_csv(oof_file,show_col_types=FALSE);p<-ggplot(x,aes(x=Yield_kg_ha,y=OOF_Predicted_Yield_kg_ha,text=paste0("District: ",District,"<br>Crop: ",Crop)))+geom_point(alpha=.55)+geom_abline(slope=1,intercept=0,linetype=2)+labs(x="Observed yield (kg/ha)",y="Out-of-fold predicted yield (kg/ha)")+theme_minimal(base_size=12);ggplotly(p,tooltip="text")})
  output$importance_plot <- renderPlotly({req(nrow(importance)>0);x<-importance|>slice_head(n=12)|>arrange(Importance);plot_ly(x,x=~Importance,y=~reorder(Feature,Importance),type="bar",orientation="h",hovertemplate="%{y}<br>Importance: %{x:.3f}<extra></extra>")|>layout(xaxis=list(title="Model feature importance"),yaxis=list(title=""),margin=list(l=150))})
  output$ml_table <- renderDT({req(!is.null(ml_metrics));datatable(tibble(Fold=1:5,`MAE (kg/ha)`=ml_metrics$fold_mae_kg_ha,`R²`=ml_metrics$fold_r2),rownames=FALSE,options=list(dom='tip'))|>formatRound(c("MAE (kg/ha)","R²"),3)})

  output$driver_plot <- renderPlotly({x<-model;p<-ggplot(x,aes(x=.data[[input$driver]],y=Yield_kg_ha,text=paste0("District: ",District,"<br>Crop: ",Crop)))+geom_point(alpha=.45)+labs(x="Indicator (%)",y="Yield (kg/ha)")+theme_minimal(base_size=12);if(input$trend)p<-p+geom_smooth(method="lm",se=TRUE);ggplotly(p,tooltip="text")})
  output$corr_table <- renderDT({vals<-model|>select(all_of(features),Yield_kg_ha)|>summarise(across(all_of(features),~cor(.x,Yield_kg_ha,use="complete.obs")))|>pivot_longer(everything(),names_to="Indicator",values_to="Correlation")|>arrange(desc(abs(Correlation)));datatable(vals,rownames=FALSE,options=list(dom='tip'))|>formatRound("Correlation",3)})

  profile <- reactive({district|>filter(District==input$profile_district)})
  output$profile_header <- renderUI({p<-profile();div(class="profile-hero",h2(input$profile_district),p(class="profile-sub",paste0("Observed evidence across ",p$crops_observed," crop groups")),div(class="profile-stats",span(paste0("Mean yield: ",fmt(p$mean_yield_kg_ha)," kg/ha")),span(paste0("Irrigation: ",fmt(p$mean_irrigation_pct,1),"%")),span(paste0("Severe erosion: ",fmt(p$severe_erosion_pct,1),"%"))))})
  output$profile_crop_plot <- renderPlotly({x<-model|>filter(District==input$profile_district)|>arrange(desc(Yield_kg_ha));plot_ly(x,x=~Yield_kg_ha,y=~reorder(Crop,Yield_kg_ha),type="bar",orientation="h",hovertemplate="%{y}<br>%{x:,.0f} kg/ha<extra></extra>")|>layout(xaxis=list(title="Observed yield (kg/ha)"),yaxis=list(title=""),margin=list(l=125))})
  output$profile_practice_plot <- renderPlotly({p<-profile();x<-tibble(Indicator=c("Irrigation","Inorganic fertilizer","Organic fertilizer","Erosion protected"),Value=c(p$mean_irrigation_pct,p$mean_inorganic_fertilizer_pct,p$mean_organic_fertilizer_pct,p$severe_erosion_pct));plot_ly(x,x=~Value,y=~reorder(Indicator,Value),type="bar",orientation="h",hovertemplate="%{y}<br>%{x:.1f}%<extra></extra>")|>layout(xaxis=list(title="Indicator (%)"),yaxis=list(title=""),margin=list(l=150))})
  output$profile_table <- renderDT({model|>filter(District==input$profile_district)|>select(District,Crop,Yield_kg_ha,Production_MT,irrigation_pct,inorganic_fertilizer_farmers_pct,organic_fertilizer_farmers_pct,erosion_protected_pct)|>arrange(desc(Yield_kg_ha))|>datatable(rownames=FALSE,options=list(pageLength=15))|>formatRound(c("Yield_kg_ha","Production_MT"),1)|>formatRound(c("irrigation_pct","inorganic_fertilizer_farmers_pct","organic_fertilizer_farmers_pct","erosion_protected_pct"),1)})
  output$download_profile <- downloadHandler(filename=function()paste0(gsub(" ","_",input$profile_district),"_RAPIS_evidence.csv"),content=function(file)write.csv(model|>filter(District==input$profile_district),file,row.names=FALSE))

  output$target_plot <- renderPlotly({p<-ggplot(targeting,aes(x=mean_irrigation_pct,y=mean_yield_kg_ha,size=severe_erosion_pct,text=paste0("District: ",District,"<br>Evidence priority score: ",round(targeting_score,1),"<br>Severe erosion: ",round(severe_erosion_pct,1),"%")))+geom_point(alpha=.7)+labs(x="Mean irrigation coverage (%)",y="Mean observed yield (kg/ha)",size="Severe erosion (%)")+theme_minimal(base_size=12);ggplotly(p,tooltip="text")})
  output$target_logic <- renderUI({div(class="prose",h4("Score components"),tags$ul(tags$li("45%: productivity gap"),tags$li("30%: irrigation gap"),tags$li("25%: severe-erosion pressure")),p("Each component is percentile-scaled across the 30 districts. The score is intended to make assumptions visible and testable, not to represent an official allocation decision."))})
  output$target_table <- renderDT({datatable(targeting|>select(District,mean_yield_kg_ha,mean_irrigation_pct,severe_erosion_pct,targeting_score,decision_band),rownames=FALSE,options=list(pageLength=15))|>formatRound(c("mean_yield_kg_ha","targeting_score"),1)|>formatRound(c("mean_irrigation_pct","severe_erosion_pct"),1)})
  output$download_targeting <- downloadHandler(filename="RAPIS_evidence_targeting.csv",content=function(file)write.csv(targeting,file,row.names=FALSE))

  output$map_status <- renderUI({
    ready <- file.exists(evidence_files[5]) && requireNamespace("sf",quietly=TRUE) && requireNamespace("leaflet",quietly=TRUE)
    if (ready) div(class="method-note success-note",strong("Map connected: "),"official/approved GeoJSON detected. District evidence is joined before rendering.") else div(class="method-note",strong("Map status: "),"READY TO CONNECT — no fabricated geography is used in the current package.")
  })
  outputOptions(output,"map_status",suspendWhenHidden=FALSE)
  output$map_ready <- reactive({file.exists(evidence_files[5]) && requireNamespace("sf",quietly=TRUE) && requireNamespace("leaflet",quietly=TRUE)})
  outputOptions(output,"map_ready",suspendWhenHidden=FALSE)
  output$evidence_map <- renderLeaflet({
    req(file.exists(evidence_files[5]),requireNamespace("sf",quietly=TRUE),requireNamespace("leaflet",quietly=TRUE))
    g <- sf::st_read(evidence_files[5],quiet=TRUE)
    nm <- names(g); district_col <- nm[grepl("district",tolower(nm))][1]
    req(!is.na(district_col))
    g <- g |> dplyr::left_join(targeting |> select(District,targeting_score,mean_yield_kg_ha,mean_irrigation_pct,severe_erosion_pct), by=c(district_col="District"))
    leaflet(g) |> addProviderTiles("CartoDB.Positron") |> addPolygons(weight=1,fillOpacity=.65,
      label=~paste0(District,": priority ",round(targeting_score,1)),
      popup=~paste0("<b>",District,"</b><br>Mean yield: ",round(mean_yield_kg_ha)," kg/ha<br>Irrigation: ",round(mean_irrigation_pct,1),"%<br>Severe erosion: ",round(severe_erosion_pct,1),"%<br>Evidence priority: ",round(targeting_score,1)))
  })

  scenario_pred <- reactive({
    nd <- tibble(
      irrigation_pct=input$scenario_irrigation,
      inorganic_fertilizer_farmers_pct=input$scenario_inorganic,
      organic_fertilizer_farmers_pct=median(model$organic_fertilizer_farmers_pct,na.rm=TRUE),
      erosion_protected_pct=input$scenario_erosion,
      agroforestry_pct=input$scenario_agro,
      mechanical_equipment_pct=median(model$mechanical_equipment_pct,na.rm=TRUE),
      Crop=input$scenario_crop
    )
    expm1(predict(fit,newdata=nd))
  })
  output$scenario_kpis <- renderUI({
    base <- median(model$Yield_kg_ha[model$Crop==input$scenario_crop],na.rm=TRUE)
    pred <- scenario_pred()
    tagList(div(class="metric-grid",metric_card("Scenario estimate",paste0(fmt(pred)," kg/ha"),"model-based sensitivity estimate","accent"),metric_card("Crop benchmark",paste0(fmt(base)," kg/ha"),"observed crop median"),metric_card("Difference",paste0(fmt(pred-base)," kg/ha"),"scenario minus crop median")))
  })
  output$scenario_plot <- renderPlotly({
    vals <- tibble(Indicator=c("Irrigation","Inorganic fertilizer","Erosion protection","Agroforestry"),Value=c(input$scenario_irrigation,input$scenario_inorganic,input$scenario_erosion,input$scenario_agro))
    plot_ly(vals,x=~Value,y=~reorder(Indicator,Value),type="bar",orientation="h",hovertemplate="%{y}: %{x:.1f}%<extra></extra>") |> layout(xaxis=list(title="Scenario level (%)"),yaxis=list(title=""),margin=list(l=150))
  })
  output$scenario_interpretation <- renderUI({
    p <- scenario_pred(); base <- median(model$Yield_kg_ha[model$Crop==input$scenario_crop],na.rm=TRUE);
    div(class="prose",h4("What this means"),p(paste0("Under the selected inputs, the fitted exploratory model returns an estimated yield of ",fmt(p)," kg/ha for ",input$scenario_crop,". The observed crop median is ",fmt(base)," kg/ha.")),p(strong("Use: "),"compare scenarios and identify questions for further field or programme evaluation."),p(strong("Do not use as: "),"a guaranteed treatment effect, causal estimate, or official policy target.")))
  })
  output$scenario_table <- renderDT({
    datatable(tibble(Variable=c("Crop","Irrigation","Inorganic fertilizer","Erosion protection","Agroforestry","Organic fertilizer (held at median)","Mechanical equipment (held at median)"),Value=c(input$scenario_crop,input$scenario_irrigation,input$scenario_inorganic,input$scenario_erosion,input$scenario_agro,round(median(model$organic_fertilizer_farmers_pct,na.rm=TRUE),1),round(median(model$mechanical_equipment_pct,na.rm=TRUE),1))),rownames=FALSE,options=list(dom='tip'))
  })

  output$nisr_latest_table <- renderDT({datatable(nisr_latest,rownames=FALSE,options=list(dom='tip',pageLength=10)) |> formatRound("Season_B_2026",1)})

  output$nisr_readiness_table <- renderDT({
    x <- tibble(
      Requirement=c("Public GitHub repository","Deployed application","Documentation","NISR data acknowledgement","AI assistance disclosure","Originality / source declaration","Clean-install reproducibility"),
      Status=c("READY","READY TO DEPLOY","READY","READY","READY","REQUIRED BEFORE SUBMISSION","TEST BEFORE SUBMISSION"),
      RAPIS_evidence=c("Repository package structure","Shiny app + deployment checklist","docs/ folder","Data-source documentation","docs/AI_ASSISTANCE_DISCLOSURE.md","Submission checklist","r_shiny/install.R + run_app.R")
    )
    datatable(x,rownames=FALSE,options=list(dom='tip',pageLength=10))
  })

  output$external_table <- renderDT({datatable(external_status,rownames=FALSE,options=list(dom='tip',pageLength=10))})
  output$download_external_template <- downloadHandler(filename="RAPIS_external_data_status.csv",content=function(file)write.csv(external_status,file,row.names=FALSE))
}
shinyApp(ui,server)
