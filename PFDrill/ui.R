library(shiny)
library(plotly)

# Define UI for application that draws a histogram
ui <- fluidPage(
    
    # Application title
    titlePanel("Personal Financial Disclosure Heatmap"),
    mainPanel(
        h2('Heatmap'),
        plotlyOutput("heat"),
        tableOutput('selected'),
        tableOutput('entries')
    )
    #,verbatimTextOutput("selection")
    
)

