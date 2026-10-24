packages <- c("shiny","bslib","plotly","DT","dplyr","tidyr","readr","ggplot2","scales","htmltools","jsonlite","leaflet","sf")
new <- packages[!vapply(packages, requireNamespace, logical(1), quietly=TRUE)]
if(length(new)) install.packages(new, repos="https://cloud.r-project.org")
message("RAPIS dependencies are ready. Run shiny::runApp('r_shiny').")
