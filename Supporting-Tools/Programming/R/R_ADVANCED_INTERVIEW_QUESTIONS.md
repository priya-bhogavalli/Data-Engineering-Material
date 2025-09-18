# 📊 R Programming Advanced Interview Questions (41-80)

### 41. How do you perform machine learning in R?
**Answer:**
```r
library(caret)
library(randomForest)

# Data preparation
data(iris)
set.seed(123)
trainIndex <- createDataPartition(iris$Species, p = 0.8, list = FALSE)
train_data <- iris[trainIndex, ]
test_data <- iris[-trainIndex, ]

# Random Forest
rf_model <- randomForest(Species ~ ., data = train_data)
rf_pred <- predict(rf_model, test_data)
confusionMatrix(rf_pred, test_data$Species)

# Cross-validation
ctrl <- trainControl(method = "cv", number = 10)
rf_cv <- train(Species ~ ., data = train_data, 
               method = "rf", trControl = ctrl)

# Model comparison
models <- list(
  rf = train(Species ~ ., data = train_data, method = "rf", trControl = ctrl),
  svm = train(Species ~ ., data = train_data, method = "svmRadial", trControl = ctrl),
  knn = train(Species ~ ., data = train_data, method = "knn", trControl = ctrl)
)
resamples(models) %>% summary()
```

### 42. How do you create Shiny applications?
**Answer:**
```r
library(shiny)

# UI
ui <- fluidPage(
  titlePanel("Iris Dataset Explorer"),
  
  sidebarLayout(
    sidebarPanel(
      selectInput("variable", "Choose variable:",
                  choices = names(iris)[1:4]),
      sliderInput("bins", "Number of bins:",
                  min = 5, max = 50, value = 30)
    ),
    
    mainPanel(
      plotOutput("histogram"),
      tableOutput("summary")
    )
  )
)

# Server
server <- function(input, output) {
  output$histogram <- renderPlot({
    hist(iris[[input$variable]], 
         breaks = input$bins,
         main = paste("Histogram of", input$variable))
  })
  
  output$summary <- renderTable({
    summary(iris[[input$variable]])
  })
}

# Run app
shinyApp(ui = ui, server = server)

# Reactive expressions
server <- function(input, output) {
  filtered_data <- reactive({
    iris[iris$Species == input$species, ]
  })
  
  output$plot <- renderPlot({
    plot(filtered_data()$Sepal.Length, filtered_data()$Sepal.Width)
  })
}
```

### 43. How do you work with big data in R?
**Answer:**
```r
# data.table for large datasets
library(data.table)

# Fast reading
dt <- fread("large_file.csv")  # Much faster than read.csv

# Efficient operations
dt[, mean_value := mean(column1), by = group]  # Group operations
dt[column1 > 100 & column2 == "A"]  # Fast filtering

# Memory efficient operations
dt[, .(sum_col1 = sum(column1), 
       count = .N), by = .(group1, group2)]

# Working with databases for big data
library(DBI)
library(dplyr)

con <- dbConnect(RSQLite::SQLite(), "large_db.sqlite")
large_table <- tbl(con, "big_table")

# Process data in chunks
result <- large_table %>%
  filter(date >= "2023-01-01") %>%
  group_by(category) %>%
  summarise(total = sum(amount)) %>%
  collect()

# Parallel processing
library(parallel)
library(foreach)
library(doParallel)

# Setup parallel backend
cl <- makeCluster(detectCores() - 1)
registerDoParallel(cl)

# Parallel computation
result <- foreach(i = 1:1000, .combine = c) %dopar% {
  # Some computation
  sqrt(i)
}

stopCluster(cl)
```

### 44. How do you perform text mining and NLP in R?
**Answer:**
```r
library(tm)
library(wordcloud)
library(tidytext)

# Create corpus
docs <- c("This is the first document.",
          "This document is the second document.",
          "And this is the third one.")
corpus <- Corpus(VectorSource(docs))

# Text preprocessing
corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, removeNumbers)
corpus <- tm_map(corpus, removeWords, stopwords("english"))
corpus <- tm_map(corpus, stripWhitespace)

# Document-term matrix
dtm <- DocumentTermMatrix(corpus)
inspect(dtm)

# Term frequency
freq <- colSums(as.matrix(dtm))
freq[order(freq, decreasing = TRUE)]

# Word cloud
wordcloud(names(freq), freq, min.freq = 1)

# Sentiment analysis with tidytext
library(tidytext)
library(dplyr)

text_df <- data.frame(
  text = c("I love this product", "This is terrible", "Amazing quality"),
  id = 1:3
)

sentiment <- text_df %>%
  unnest_tokens(word, text) %>%
  inner_join(get_sentiments("bing")) %>%
  count(id, sentiment) %>%
  spread(sentiment, n, fill = 0) %>%
  mutate(sentiment_score = positive - negative)
```

### 45. How do you work with spatial data in R?
**Answer:**
```r
library(sf)
library(ggplot2)
library(maps)

# Reading spatial data
# shapefile <- st_read("path/to/shapefile.shp")

# Creating spatial points
points <- data.frame(
  lon = c(-74.0059, -118.2437, -87.6298),
  lat = c(40.7128, 34.0522, 41.8781),
  city = c("New York", "Los Angeles", "Chicago")
)

points_sf <- st_as_sf(points, coords = c("lon", "lat"), crs = 4326)

# Plotting maps
world <- map_data("world")
ggplot(world, aes(x = long, y = lat, group = group)) +
  geom_polygon(fill = "lightgray", color = "white") +
  geom_sf(data = points_sf, color = "red", size = 3) +
  coord_sf(xlim = c(-180, 180), ylim = c(-90, 90))

# Spatial operations
# buffer <- st_buffer(points_sf, dist = 1000)  # 1km buffer
# intersection <- st_intersection(poly1, poly2)
# distance <- st_distance(points_sf)

# Leaflet for interactive maps
library(leaflet)
leaflet(points) %>%
  addTiles() %>%
  addMarkers(~lon, ~lat, popup = ~city)
```

### 46. How do you perform web scraping in R?
**Answer:**
```r
library(rvest)
library(httr)

# Basic web scraping
url <- "https://example.com"
page <- read_html(url)

# Extract elements
titles <- page %>%
  html_nodes("h2") %>%
  html_text()

links <- page %>%
  html_nodes("a") %>%
  html_attr("href")

# Tables
tables <- page %>%
  html_table(fill = TRUE)

# Handling forms and sessions
session <- html_session("https://example.com/login")
form <- html_form(session)[[1]]
filled_form <- set_values(form, username = "user", password = "pass")
submit_form(session, filled_form)

# API requests
library(jsonlite)
response <- GET("https://api.example.com/data")
data <- fromJSON(content(response, "text"))

# Rate limiting and politeness
Sys.sleep(1)  # Wait between requests
```

### 47. How do you create interactive visualizations?
**Answer:**
```r
library(plotly)
library(DT)
library(crosstalk)

# Interactive ggplot
p <- ggplot(mtcars, aes(x = wt, y = mpg, color = factor(cyl))) +
  geom_point() +
  geom_smooth(method = "lm")
ggplotly(p)

# Interactive tables
datatable(mtcars, 
          filter = "top",
          options = list(pageLength = 10, scrollX = TRUE))

# Linked brushing with crosstalk
shared_mtcars <- SharedData$new(mtcars)

bscols(
  plot_ly(shared_mtcars, x = ~wt, y = ~mpg) %>% add_markers(),
  datatable(shared_mtcars)
)

# Custom plotly
plot_ly(mtcars, x = ~wt, y = ~mpg, color = ~factor(cyl),
        type = "scatter", mode = "markers",
        hovertemplate = "Weight: %{x}<br>MPG: %{y}<extra></extra>")

# 3D plots
plot_ly(mtcars, x = ~wt, y = ~hp, z = ~mpg, color = ~factor(cyl),
        type = "scatter3d", mode = "markers")
```

### 48. How do you optimize R code performance?
**Answer:**
```r
# Vectorization vs loops
# Slow
result <- numeric(1000)
for(i in 1:1000) {
  result[i] <- i^2
}

# Fast
result <- (1:1000)^2

# Pre-allocate vectors
# Slow
result <- c()
for(i in 1:1000) {
  result <- c(result, i^2)
}

# Fast
result <- numeric(1000)
for(i in 1:1000) {
  result[i] <- i^2
}

# Use apply family instead of loops
# apply, lapply, sapply, mapply

# Profiling code
library(profvis)
profvis({
  # Your code here
  slow_function()
})

# Benchmarking
library(microbenchmark)
microbenchmark(
  method1 = slow_approach(),
  method2 = fast_approach(),
  times = 100
)

# Memory profiling
library(pryr)
object_size(large_object)
mem_used()
mem_change(expensive_operation())

# Parallel processing
library(parallel)
mclapply(1:4, function(x) x^2, mc.cores = 2)
```

### 49. How do you work with APIs in R?
**Answer:**
```r
library(httr)
library(jsonlite)

# GET request
response <- GET("https://api.github.com/users/octocat")
status_code(response)
content(response, "text")

# Parse JSON response
data <- fromJSON(content(response, "text"))

# POST request with data
post_data <- list(name = "test", value = 123)
response <- POST("https://api.example.com/data",
                 body = post_data, encode = "json")

# Authentication
# API key in header
response <- GET("https://api.example.com/data",
                add_headers(Authorization = paste("Bearer", api_key)))

# OAuth
oauth_app <- oauth_app("myapp", key = "key", secret = "secret")
token <- oauth2.0_token(oauth_endpoints("github"), oauth_app)
response <- GET("https://api.github.com/user", config(token = token))

# Error handling
safe_api_call <- function(url) {
  tryCatch({
    response <- GET(url)
    if (status_code(response) == 200) {
      return(fromJSON(content(response, "text")))
    } else {
      stop("API request failed with status: ", status_code(response))
    }
  }, error = function(e) {
    message("Error: ", e$message)
    return(NULL)
  })
}
```

### 50. How do you create R packages?
**Answer:**
```r
library(devtools)
library(roxygen2)

# Create package structure
create_package("mypackage")

# Package structure:
# DESCRIPTION - package metadata
# NAMESPACE - exported functions
# R/ - R code files
# man/ - documentation
# tests/ - unit tests

# Example function with documentation
#' Add two numbers
#'
#' @param x A number
#' @param y A number
#' @return The sum of x and y
#' @export
#' @examples
#' add_numbers(2, 3)
add_numbers <- function(x, y) {
  x + y
}

# Generate documentation
document()

# Check package
check()

# Install package
install()

# Unit tests with testthat
library(testthat)

test_that("add_numbers works correctly", {
  expect_equal(add_numbers(2, 3), 5)
  expect_equal(add_numbers(-1, 1), 0)
  expect_error(add_numbers("a", 1))
})

# Build package
build()

# Submit to CRAN
release()
```

### 51-60. Additional Advanced Topics:
- **Rcpp** - C++ integration for performance
- **Parallel computing** - Advanced parallel strategies
- **Memory management** - Efficient memory usage
- **S4 classes** - Object-oriented programming
- **R6 classes** - Reference classes
- **Environments** - Advanced environment manipulation
- **Metaprogramming** - Non-standard evaluation
- **Package testing** - Comprehensive testing strategies
- **Continuous integration** - Automated testing and deployment
- **Docker** - Containerizing R applications

### 61-70. Specialized Domains:
- **Bioinformatics** - Bioconductor packages
- **Finance** - Quantitative finance with quantmod
- **Econometrics** - Time series and panel data
- **Bayesian analysis** - MCMC and Stan
- **Survival analysis** - Time-to-event data
- **Network analysis** - Graph theory and networks
- **Image processing** - Computer vision tasks
- **Signal processing** - Time series and frequency analysis
- **Optimization** - Mathematical optimization
- **Simulation** - Monte Carlo methods

### 71-80. Production and Deployment:
- **Plumber** - REST APIs in R
- **Docker deployment** - Containerized R services
- **Cloud deployment** - AWS, GCP, Azure
- **Scaling R** - Distributed computing
- **Monitoring** - Application monitoring
- **Security** - Secure R applications
- **Version control** - Git workflows for R
- **Reproducibility** - Reproducible research practices
- **Documentation** - Package and project documentation
- **Best practices** - R coding standards and conventions

---

*This completes the comprehensive R programming interview questions covering 80 essential topics with detailed answers and practical code examples.*