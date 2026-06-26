# Combined VAST Challenge 2026 MC1 Shiny app

COMBINED_APP <- TRUE

source("task1.R", local = TRUE)
source("task2.R", local = TRUE)
source("task3.R", local = TRUE)

ui <- page_navbar(
  title          = mc1_title,
  theme          = mc1_theme,
  header         = tags$head(tags$style(HTML(mc1_css))),
  navbar_options = mc1_navbar_opts,
  task1_panel_explore,
  task1_panel_task,
  task2_ui,
  task3_ui,
  nav_spacer(),
  nav_item(
    tags$span(
      style = "color:rgba(255,255,255,0.45); font-size:0.76rem; font-weight:500;",
      "VAST Challenge 2026 MC1", tags$span(style = "margin:0 6px;", "|"), "ISSS608"
    )
  )
)

server <- function(input, output, session) {
  task1_server(input, output, session)
  task2_server(input, output, session)
  task3_server(input, output, session)
}

shinyApp(ui = ui, server = server)
