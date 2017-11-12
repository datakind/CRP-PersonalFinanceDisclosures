#

library(shiny)

source('ui.R')
#source('server.R')

print(getwd())
# Run the application 
shinyApp(ui = ui, server = server)

