library(shiny)
library(dplyr)
library(ggplot2)
library(scales)
library(shinydashboard)
library(ggvis)
library(tidyr)


correlation <- round(cor(mtcars), 3)
nms <- names(mtcars)

loadData <- function() {
    result <- c()
    pfd <- read.csv('Goal1_PFD_1of3.csv.gz')
    pfd$CalendarYear <- pfd$CalendarYear + 2000
    result$pfd <- pfd
    
    candidates <- read.csv('Cands.csv.gz')
    candidates$Name <- sprintf("%s %s", candidates$Firstname, candidates$Lastname)
    result$candidates <- candidates
    return(result)
}
    
getHeatMapData <- function(d) {
    #Todo: avoid this two-step
    tmp <- d %>% group_by(CID, CalendarYear) %>% summarize(n=n()) %>% arrange(desc(n))
    x <- data.frame(CID = tmp$CID, Year=tmp$CalendarYear, n=tmp$n)
    x$Year <- sprintf('Year-%s', x$Year)
    y <- spread(x, Year, n)
    cids <- y$CID
    z <- y[,2:ncol(y)]
    rownames(z) <- cids
    m <- as.matrix(z)
    m[is.na(m)] <- 0
    return (t(m))
}

data <- {
    #load(file='all.Rdata')
    loadData()
}
    
# Define server logic required to draw a histogram
server <- function(input, output) {
    output$heat <- renderPlotly({
        v <- getHeatMapData(data$pfd)
        a <- attributes(v)[[2]]
        cids <- unlist(a[2])
        names <- data$candidates %>% 
            select(CID, Name) %>% 
            inner_join(data.frame(CID=cids), by='CID') %>% 
            select(Name)
        years <- unlist(a[1])
        m <- matrix(v, nrow=nrow(v))
        
        vals <- unique(scales::rescale(c(m)))
        o <- order(vals, decreasing = FALSE)
        cols <- scales::col_numeric("Reds", domain = NULL)(vals)
        colz <- setNames(data.frame(vals[o], cols[o]), NULL)
        
        plot_ly(x = cids, y = years, z = m, type = "heatmap", 
                colorscale = colz, source = "heatplot") %>%
            layout(xaxis = list(title = ""), yaxis = list(title = ""))
    })
    
    output$selected <- renderTable(
    { 
        s <- event_data("plotly_click", source = "heatplot")
        if (length(s)) {
            cid <- s[['x']]
            name <- data$candidates$Name[data$candidates$CID == cid]
            d <- data.frame(Property=c("CID", "Name", "Year", "Entries"), 
                            Value=c(cid, name, s[['y']], s[['z']]))
        } else {
            d <- data.frame()
        }
        return(d)
    })

    output$entries <- renderTable(
    { 
        s <- event_data("plotly_click", source = "heatplot")
        if (length(s)) {
            cid <- s[['x']]
            year <- gsub('Year-', '', s[['y']])
            d <- data$pfd %>% 
                filter(CID == cid, CalendarYear == year) %>%
                select(AssetSource, Asset4Date, TransactionType)
            
        } else {
            d <- data.frame()
        }
        return (d)
    })
    
}