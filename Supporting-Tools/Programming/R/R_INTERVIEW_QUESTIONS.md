# 📊 R Programming Interview Questions & Answers

## 📋 Table of Contents
- [Basic Concepts](#basic-concepts)
- [Data Types & Structures](#data-types--structures)
- [Data Manipulation](#data-manipulation)
- [Statistical Analysis](#statistical-analysis)
- [Data Visualization](#data-visualization)
- [Advanced Programming](#advanced-programming)
- [Performance & Best Practices](#performance--best-practices)

---

## Basic Concepts

### 1. What is R and what are its key features?
**Answer:**
R is a programming language and environment for statistical computing and graphics.

**Key Features:**
- **Statistical computing**: Built-in statistical functions
- **Data visualization**: Powerful plotting capabilities
- **Open source**: Free and extensible
- **Package ecosystem**: CRAN with 18,000+ packages
- **Vectorized operations**: Efficient data processing
- **Cross-platform**: Runs on Windows, Mac, Linux

**Example:**
```r
# Basic R operations
x <- c(1, 2, 3, 4, 5)
mean(x)  # 3
sum(x)   # 15
plot(x)  # Simple plot
```

### 2. Explain R's assignment operators and their differences.
**Answer:**
**Assignment Operators:**
```r
# Left assignment
x <- 5        # Preferred
x = 5         # Also works
assign("x", 5) # Function-based

# Right assignment
5 -> y        # Less common

# Global assignment
x <<- 10      # Assigns to global environment

# Checking assignments
ls()          # List objects in environment
rm(x)         # Remove object
```

**Best Practices:**
- Use `<-` for assignment (R convention)
- Use `=` for function arguments
- Avoid `<<-` unless necessary for global scope

### 3. What are R's basic data types?
**Answer:**
**Atomic Data Types:**
```r
# Numeric (double)
x <- 3.14
class(x)      # "numeric"
typeof(x)     # "double"

# Integer
y <- 5L
class(y)      # "integer"

# Character
name <- "John"
class(name)   # "character"

# Logical
flag <- TRUE
class(flag)   # "logical"

# Complex
z <- 3 + 4i
class(z)      # "complex"

# Raw (bytes)
raw_data <- charToRaw("hello")
class(raw_data)  # "raw"
```

### 4. How do you handle missing values in R?
**Answer:**
**Missing Value Types:**
```r
# NA (Not Available)
x <- c(1, 2, NA, 4, 5)
is.na(x)           # Check for NA
sum(x)             # Returns NA
sum(x, na.rm = TRUE)  # 12 (removes NA)

# NULL (absence of value)
y <- NULL
is.null(y)         # TRUE
length(y)          # 0

# NaN (Not a Number)
z <- 0/0
is.nan(z)          # TRUE
is.na(z)           # TRUE (NaN is also NA)

# Inf (Infinity)
inf_val <- 1/0
is.infinite(inf_val)  # TRUE
is.finite(inf_val)    # FALSE
```

**Handling Missing Values:**
```r
# Remove missing values
complete_cases <- complete.cases(data)
clean_data <- data[complete_cases, ]

# Replace missing values
x[is.na(x)] <- mean(x, na.rm = TRUE)  # Replace with mean

# Using na.omit()
clean_data <- na.omit(data)
```

### 5. What are factors in R and when to use them?
**Answer:**
Factors represent categorical data with predefined levels.

**Creating Factors:**
```r
# Basic factor
colors <- factor(c("red", "blue", "red", "green", "blue"))
levels(colors)    # "blue" "green" "red" (alphabetical)
nlevels(colors)   # 3

# Ordered factor
sizes <- factor(c("small", "large", "medium", "small"), 
                levels = c("small", "medium", "large"),
                ordered = TRUE)

# Factor with labels
gender <- factor(c(1, 2, 1, 2), 
                levels = c(1, 2), 
                labels = c("Male", "Female"))
```

**Factor Operations:**
```r
# Add levels
levels(colors) <- c(levels(colors), "yellow")

# Reorder levels
colors <- factor(colors, levels = c("red", "blue", "green"))

# Convert to character
as.character(colors)

# Drop unused levels
droplevels(colors)
```

---

## Data Types & Structures

### 6. What are vectors and how do you work with them?
**Answer:**
**Vector Creation:**
```r
# Numeric vector
numbers <- c(1, 2, 3, 4, 5)
sequence <- 1:10
seq_by <- seq(from = 0, to = 10, by = 2)
repeated <- rep(1:3, times = 2)  # 1 2 3 1 2 3

# Character vector
names <- c("Alice", "Bob", "Charlie")

# Logical vector
flags <- c(TRUE, FALSE, TRUE)
```

**Vector Operations:**
```r
# Arithmetic operations (vectorized)
x <- c(1, 2, 3)
y <- c(4, 5, 6)
x + y        # c(5, 7, 9)
x * 2        # c(2, 4, 6)

# Indexing
numbers[1]           # First element (1-indexed)
numbers[c(1, 3, 5)]  # Multiple elements
numbers[-1]          # All except first
numbers[numbers > 3] # Conditional indexing

# Named vectors
ages <- c(Alice = 25, Bob = 30, Charlie = 35)
ages["Alice"]        # 25
```

### 7. How do you work with lists in R?
**Answer:**
Lists can contain different data types and structures.

**List Creation:**
```r
# Mixed data types
my_list <- list(
  numbers = 1:5,
  name = "John",
  matrix = matrix(1:6, nrow = 2),
  nested = list(a = 1, b = 2)
)

# Named list
person <- list(
  name = "Alice",
  age = 30,
  married = TRUE,
  children = c("Bob", "Carol")
)
```

**List Operations:**
```r
# Accessing elements
my_list[[1]]         # First element (returns vector)
my_list[1]           # First element (returns list)
my_list$numbers      # By name
my_list[["numbers"]] # By name (alternative)

# Adding elements
my_list$new_item <- "added"

# Removing elements
my_list$numbers <- NULL

# List functions
length(my_list)      # Number of elements
names(my_list)       # Element names
str(my_list)         # Structure
```

### 8. What are matrices and arrays in R?
**Answer:**
**Matrices (2D):**
```r
# Creating matrices
m1 <- matrix(1:12, nrow = 3, ncol = 4)
m2 <- matrix(1:12, nrow = 3, byrow = TRUE)

# Matrix operations
dim(m1)              # Dimensions
nrow(m1)             # Number of rows
ncol(m1)             # Number of columns

# Indexing
m1[1, 2]             # Element at row 1, column 2
m1[1, ]              # First row
m1[, 2]              # Second column
m1[1:2, 2:3]         # Submatrix

# Matrix arithmetic
m3 <- m1 + m2        # Element-wise addition
m4 <- m1 %*% t(m2)   # Matrix multiplication
```

**Arrays (Multi-dimensional):**
```r
# 3D array
arr <- array(1:24, dim = c(3, 4, 2))

# Accessing elements
arr[1, 2, 1]         # Specific element
arr[, , 1]           # First "slice"

# Array functions
dim(arr)             # c(3, 4, 2)
dimnames(arr) <- list(
  rows = c("R1", "R2", "R3"),
  cols = c("C1", "C2", "C3", "C4"),
  layers = c("L1", "L2")
)
```

### 9. How do data frames work in R?
**Answer:**
Data frames are the most common data structure for datasets.

**Creating Data Frames:**
```r
# Basic data frame
df <- data.frame(
  name = c("Alice", "Bob", "Charlie"),
  age = c(25, 30, 35),
  married = c(TRUE, FALSE, TRUE),
  stringsAsFactors = FALSE
)

# From vectors
names <- c("Alice", "Bob", "Charlie")
ages <- c(25, 30, 35)
df2 <- data.frame(names, ages)
```

**Data Frame Operations:**
```r
# Viewing data
head(df)             # First 6 rows
tail(df)             # Last 6 rows
str(df)              # Structure
summary(df)          # Summary statistics

# Dimensions
nrow(df)             # Number of rows
ncol(df)             # Number of columns
dim(df)              # Both dimensions

# Accessing data
df$name              # Column by name
df[["name"]]         # Alternative syntax
df[, "name"]         # Column by name (returns vector)
df[, c("name", "age")] # Multiple columns
df[1, ]              # First row
df[df$age > 25, ]    # Conditional selection
```

### 10. What are tibbles and how do they differ from data frames?
**Answer:**
Tibbles are a modern take on data frames (from tidyverse).

**Creating Tibbles:**
```r
library(tibble)

# Create tibble
tbl <- tibble(
  name = c("Alice", "Bob", "Charlie"),
  age = c(25, 30, 35),
  married = c(TRUE, FALSE, TRUE)
)

# Convert data frame to tibble
tbl2 <- as_tibble(df)
```

**Key Differences:**
```r
# Printing (tibbles show more info)
print(tbl)           # Shows data types, dimensions

# Subsetting (tibbles are stricter)
tbl$nam              # NULL (no partial matching)
df$nam               # Returns name column (partial matching)

# Never converts strings to factors
tbl3 <- tibble(x = c("a", "b", "c"))  # Stays character

# Can have complex columns
tbl4 <- tibble(
  x = 1:3,
  y = list(1:2, 1:3, 1:4)  # List column
)
```

---

## Data Manipulation

### 11. How do you use dplyr for data manipulation?
**Answer:**
**Core dplyr Verbs:**
```r
library(dplyr)

# Sample data
df <- data.frame(
  name = c("Alice", "Bob", "Charlie", "Diana"),
  age = c(25, 30, 35, 28),
  salary = c(50000, 60000, 70000, 55000),
  department = c("IT", "HR", "IT", "Finance")
)

# filter() - select rows
young_employees <- df %>% 
  filter(age < 30)

# select() - select columns
names_ages <- df %>% 
  select(name, age)

# mutate() - create new columns
df_with_bonus <- df %>% 
  mutate(
    bonus = salary * 0.1,
    age_group = ifelse(age < 30, "Young", "Senior")
  )

# arrange() - sort rows
sorted_df <- df %>% 
  arrange(desc(salary))

# summarise() - aggregate data
summary_stats <- df %>% 
  summarise(
    avg_age = mean(age),
    avg_salary = mean(salary),
    count = n()
  )

# group_by() - group operations
dept_summary <- df %>% 
  group_by(department) %>% 
  summarise(
    avg_salary = mean(salary),
    count = n()
  )
```

### 12. How do you reshape data with tidyr?
**Answer:**
**Pivoting Data:**
```r
library(tidyr)

# Wide to long (pivot_longer)
wide_data <- data.frame(
  name = c("Alice", "Bob"),
  math = c(90, 85),
  science = c(88, 92),
  english = c(85, 88)
)

long_data <- wide_data %>% 
  pivot_longer(
    cols = c(math, science, english),
    names_to = "subject",
    values_to = "score"
  )

# Long to wide (pivot_wider)
wide_again <- long_data %>% 
  pivot_wider(
    names_from = subject,
    values_from = score
  )

# Separate columns
df_separate <- data.frame(
  name_age = c("Alice_25", "Bob_30")
) %>% 
  separate(name_age, into = c("name", "age"), sep = "_")

# Unite columns
df_unite <- df_separate %>% 
  unite("name_age", name, age, sep = "_")
```

### 13. How do you handle string manipulation in R?
**Answer:**
**Base R String Functions:**
```r
# Basic string operations
text <- "Hello World"
nchar(text)          # 11 (character count)
toupper(text)        # "HELLO WORLD"
tolower(text)        # "hello world"

# Substring
substr(text, 1, 5)   # "Hello"
substring(text, c(1, 7), c(5, 11))  # c("Hello", "World")

# String concatenation
paste("Hello", "World")              # "Hello World"
paste0("Hello", "World")             # "HelloWorld"
paste(c("A", "B"), 1:2, sep = "-")  # c("A-1", "B-2")

# Pattern matching
grep("World", c("Hello", "World", "R"))  # 2 (position)
grepl("World", c("Hello", "World", "R")) # c(FALSE, TRUE, FALSE)
```

**stringr Package:**
```r
library(stringr)

# String detection
str_detect(c("apple", "banana", "cherry"), "a")  # c(TRUE, TRUE, FALSE)

# String extraction
str_extract("Phone: 123-456-7890", "\\d{3}-\\d{3}-\\d{4}")  # "123-456-7890"

# String replacement
str_replace("Hello World", "World", "R")  # "Hello R"
str_replace_all("banana", "a", "o")       # "bonono"

# String splitting
str_split("apple,banana,cherry", ",")     # List with vector

# String length and trimming
str_length("  hello  ")                   # 9
str_trim("  hello  ")                     # "hello"
```

### 14. How do you work with dates and times in R?
**Answer:**
**Base R Date/Time:**
```r
# Current date and time
Sys.Date()           # Current date
Sys.time()           # Current date and time

# Creating dates
date1 <- as.Date("2024-03-15")
date2 <- as.Date("15/03/2024", format = "%d/%m/%Y")

# Date arithmetic
date1 + 30           # Add 30 days
date2 - date1        # Difference in days

# Date components
format(date1, "%Y")  # Year: "2024"
format(date1, "%m")  # Month: "03"
format(date1, "%d")  # Day: "15"
format(date1, "%A")  # Weekday: "Friday"
```

**lubridate Package:**
```r
library(lubridate)

# Parsing dates
ymd("2024-03-15")    # 2024-03-15
mdy("03/15/2024")    # 2024-03-15
dmy("15-03-2024")    # 2024-03-15

# Date-time parsing
ymd_hms("2024-03-15 14:30:00")

# Extracting components
date <- ymd("2024-03-15")
year(date)           # 2024
month(date)          # 3
day(date)            # 15
wday(date, label = TRUE)  # Fri

# Date arithmetic
date + days(30)      # Add 30 days
date + months(2)     # Add 2 months
date + years(1)      # Add 1 year

# Time intervals
interval(ymd("2024-01-01"), ymd("2024-12-31"))
duration(days = 365)
period(months = 12)
```

### 15. How do you join data frames in R?
**Answer:**
**Base R Joins:**
```r
# Sample data
df1 <- data.frame(
  id = c(1, 2, 3),
  name = c("Alice", "Bob", "Charlie")
)

df2 <- data.frame(
  id = c(1, 2, 4),
  salary = c(50000, 60000, 70000)
)

# merge() function
inner_join <- merge(df1, df2, by = "id")              # Inner join
left_join <- merge(df1, df2, by = "id", all.x = TRUE) # Left join
right_join <- merge(df1, df2, by = "id", all.y = TRUE) # Right join
full_join <- merge(df1, df2, by = "id", all = TRUE)   # Full join
```

**dplyr Joins:**
```r
library(dplyr)

# Join functions
inner <- df1 %>% inner_join(df2, by = "id")
left <- df1 %>% left_join(df2, by = "id")
right <- df1 %>% right_join(df2, by = "id")
full <- df1 %>% full_join(df2, by = "id")

# Anti and semi joins
anti <- df1 %>% anti_join(df2, by = "id")   # Rows in df1 not in df2
semi <- df1 %>% semi_join(df2, by = "id")   # Rows in df1 that have match in df2

# Join by multiple columns
df3 <- data.frame(
  first_name = c("Alice", "Bob"),
  last_name = c("Smith", "Jones"),
  age = c(25, 30)
)

df4 <- data.frame(
  first_name = c("Alice", "Bob"),
  last_name = c("Smith", "Jones"),
  salary = c(50000, 60000)
)

joined <- df3 %>% 
  inner_join(df4, by = c("first_name", "last_name"))
```

---

## Statistical Analysis

### 16. How do you perform descriptive statistics in R?
**Answer:**
**Basic Statistics:**
```r
# Sample data
data <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

# Central tendency
mean(data)           # 5.5
median(data)         # 5.5
mode <- function(x) {
  ux <- unique(x)
  ux[which.max(tabulate(match(x, ux)))]
}

# Variability
var(data)            # Variance
sd(data)             # Standard deviation
range(data)          # Min and max
IQR(data)            # Interquartile range

# Quantiles
quantile(data)       # 0%, 25%, 50%, 75%, 100%
quantile(data, probs = c(0.1, 0.9))  # 10th and 90th percentiles

# Summary statistics
summary(data)        # Min, 1st Qu., Median, Mean, 3rd Qu., Max
```

**For Data Frames:**
```r
# Built-in dataset
data(mtcars)

# Summary for all columns
summary(mtcars)

# Specific statistics
sapply(mtcars, mean)  # Mean for each column
sapply(mtcars, sd)    # Standard deviation for each column

# Using dplyr
library(dplyr)
mtcars %>% 
  summarise(
    mean_mpg = mean(mpg),
    sd_mpg = sd(mpg),
    median_hp = median(hp),
    count = n()
  )

# Group statistics
mtcars %>% 
  group_by(cyl) %>% 
  summarise(
    mean_mpg = mean(mpg),
    mean_hp = mean(hp),
    count = n()
  )
```

### 17. How do you perform hypothesis testing in R?
**Answer:**
**t-tests:**
```r
# One-sample t-test
data <- rnorm(30, mean = 10, sd = 2)
t.test(data, mu = 10)  # Test if mean equals 10

# Two-sample t-test
group1 <- rnorm(30, mean = 10, sd = 2)
group2 <- rnorm(30, mean = 12, sd = 2)
t.test(group1, group2)  # Independent samples
t.test(group1, group2, paired = TRUE)  # Paired samples

# Welch's t-test (unequal variances)
t.test(group1, group2, var.equal = FALSE)
```

**Other Tests:**
```r
# Chi-square test
observed <- c(20, 30, 25, 25)
expected <- c(25, 25, 25, 25)
chisq.test(observed, p = expected/sum(expected))

# ANOVA
data(mtcars)
anova_result <- aov(mpg ~ factor(cyl), data = mtcars)
summary(anova_result)

# Correlation test
cor.test(mtcars$mpg, mtcars$hp)

# Shapiro-Wilk normality test
shapiro.test(mtcars$mpg)

# Wilcoxon test (non-parametric)
wilcox.test(group1, group2)
```

### 18. How do you perform regression analysis in R?
**Answer:**
**Linear Regression:**
```r
# Simple linear regression
model <- lm(mpg ~ hp, data = mtcars)
summary(model)

# Multiple regression
model2 <- lm(mpg ~ hp + wt + cyl, data = mtcars)
summary(model2)

# Model diagnostics
plot(model2)         # Diagnostic plots
residuals(model2)    # Residuals
fitted(model2)       # Fitted values
```

**Advanced Regression:**
```r
# Polynomial regression
model_poly <- lm(mpg ~ poly(hp, 2), data = mtcars)

# Interaction terms
model_interact <- lm(mpg ~ hp * wt, data = mtcars)

# Stepwise regression
library(MASS)
full_model <- lm(mpg ~ ., data = mtcars)
step_model <- stepAIC(full_model, direction = "both")

# Logistic regression
# Convert to binary outcome
mtcars$high_mpg <- ifelse(mtcars$mpg > median(mtcars$mpg), 1, 0)
logit_model <- glm(high_mpg ~ hp + wt, data = mtcars, family = binomial)
summary(logit_model)
```

### 19. How do you work with probability distributions in R?
**Answer:**
**Distribution Functions:**
```r
# Normal distribution
dnorm(0)             # Density at x=0
pnorm(0)             # Cumulative probability P(X <= 0)
qnorm(0.5)           # Quantile (inverse CDF)
rnorm(10)            # Random samples

# Other distributions
# Binomial
dbinom(5, size = 10, prob = 0.5)  # P(X = 5)
pbinom(5, size = 10, prob = 0.5)  # P(X <= 5)
rbinom(100, size = 10, prob = 0.5) # Random samples

# Poisson
dpois(3, lambda = 2)
ppois(3, lambda = 2)
rpois(100, lambda = 2)

# Chi-square
dchisq(5, df = 3)
pchisq(5, df = 3)
rchisq(100, df = 3)
```

**Custom Distributions:**
```r
# Simulate from custom distribution
simulate_mixture <- function(n) {
  # Mixture of two normals
  component <- rbinom(n, 1, 0.3)
  ifelse(component == 1, 
         rnorm(n, mean = -2, sd = 1),
         rnorm(n, mean = 3, sd = 1.5))
}

samples <- simulate_mixture(1000)
hist(samples, breaks = 30)
```

### 20. How do you perform time series analysis in R?
**Answer:**
**Time Series Objects:**
```r
# Create time series
ts_data <- ts(1:24, start = c(2020, 1), frequency = 12)  # Monthly data
plot(ts_data)

# Built-in time series
data(AirPassengers)
plot(AirPassengers)

# Decomposition
decomp <- decompose(AirPassengers)
plot(decomp)

# Seasonal decomposition
library(forecast)
stl_decomp <- stl(AirPassengers, s.window = "periodic")
plot(stl_decomp)
```

**Forecasting:**
```r
library(forecast)

# ARIMA modeling
auto_arima <- auto.arima(AirPassengers)
summary(auto_arima)

# Forecasting
forecast_result <- forecast(auto_arima, h = 12)  # 12 periods ahead
plot(forecast_result)

# Exponential smoothing
ets_model <- ets(AirPassengers)
ets_forecast <- forecast(ets_model, h = 12)

# Model accuracy
accuracy(forecast_result)
```

---

## Data Visualization

### 21. How do you create basic plots in R?
**Answer:**
**Base R Plotting:**
```r
# Scatter plot
plot(mtcars$hp, mtcars$mpg, 
     xlab = "Horsepower", 
     ylab = "Miles per Gallon",
     main = "MPG vs Horsepower")

# Line plot
x <- 1:10
y <- x^2
plot(x, y, type = "l", col = "blue", lwd = 2)

# Histogram
hist(mtcars$mpg, 
     breaks = 10, 
     col = "lightblue",
     main = "Distribution of MPG")

# Box plot
boxplot(mpg ~ cyl, data = mtcars,
        xlab = "Cylinders",
        ylab = "MPG",
        col = c("red", "green", "blue"))

# Bar plot
counts <- table(mtcars$cyl)
barplot(counts, 
        main = "Number of Cars by Cylinder",
        xlab = "Cylinders",
        col = rainbow(length(counts)))
```

### 22. How do you use ggplot2 for advanced visualization?
**Answer:**
**ggplot2 Basics:**
```r
library(ggplot2)

# Basic scatter plot
ggplot(mtcars, aes(x = hp, y = mpg)) +
  geom_point() +
  labs(title = "MPG vs Horsepower",
       x = "Horsepower",
       y = "Miles per Gallon")

# Adding aesthetics
ggplot(mtcars, aes(x = hp, y = mpg, color = factor(cyl))) +
  geom_point(size = 3) +
  geom_smooth(method = "lm", se = FALSE) +
  scale_color_manual(values = c("red", "green", "blue")) +
  theme_minimal()

# Faceting
ggplot(mtcars, aes(x = hp, y = mpg)) +
  geom_point() +
  facet_wrap(~ cyl) +
  theme_bw()
```

**Advanced ggplot2:**
```r
# Multiple geometries
ggplot(mtcars, aes(x = factor(cyl), y = mpg)) +
  geom_boxplot(alpha = 0.7) +
  geom_jitter(width = 0.2, alpha = 0.5) +
  stat_summary(fun = mean, geom = "point", 
               shape = 18, size = 3, color = "red")

# Custom themes
my_theme <- theme_minimal() +
  theme(
    plot.title = element_text(size = 16, face = "bold"),
    axis.text = element_text(size = 12),
    legend.position = "bottom"
  )

ggplot(mtcars, aes(x = hp, y = mpg, color = factor(cyl))) +
  geom_point(size = 3) +
  my_theme +
  labs(title = "Custom Themed Plot")
```

### 23. How do you create interactive visualizations?
**Answer:**
**plotly:**
```r
library(plotly)

# Convert ggplot to interactive
p <- ggplot(mtcars, aes(x = hp, y = mpg, color = factor(cyl))) +
  geom_point(size = 3) +
  labs(title = "Interactive Scatter Plot")

ggplotly(p)

# Direct plotly
plot_ly(mtcars, x = ~hp, y = ~mpg, color = ~factor(cyl),
        type = "scatter", mode = "markers") %>%
  layout(title = "Interactive Plot with plotly")
```

**shiny for Web Apps:**
```r
library(shiny)

ui <- fluidPage(
  titlePanel("Interactive Data Explorer"),
  
  sidebarLayout(
    sidebarPanel(
      selectInput("x_var", "X Variable:",
                  choices = names(mtcars),
                  selected = "hp"),
      selectInput("y_var", "Y Variable:",
                  choices = names(mtcars),
                  selected = "mpg")
    ),
    
    mainPanel(
      plotOutput("scatter_plot")
    )
  )
)

server <- function(input, output) {
  output$scatter_plot <- renderPlot({
    ggplot(mtcars, aes_string(x = input$x_var, y = input$y_var)) +
      geom_point(size = 3) +
      theme_minimal()
  })
}

shinyApp(ui = ui, server = server)
```

### 24. How do you customize plots and themes?
**Answer:**
**Base R Customization:**
```r
# Custom colors and styling
plot(mtcars$hp, mtcars$mpg,
     col = rainbow(nrow(mtcars)),
     pch = 19,  # Point type
     cex = 1.5, # Point size
     main = "Customized Scatter Plot",
     sub = "Data from mtcars dataset",
     xlab = "Horsepower",
     ylab = "Miles per Gallon",
     xlim = c(50, 350),
     ylim = c(10, 35))

# Add legend
legend("topright", 
       legend = c("4 cyl", "6 cyl", "8 cyl"),
       col = c("red", "green", "blue"),
       pch = 19)

# Add grid
grid()

# Add text annotations
text(300, 30, "High HP\nLow MPG", cex = 0.8)
```

**ggplot2 Customization:**
```r
# Custom color palettes
library(RColorBrewer)

ggplot(mtcars, aes(x = hp, y = mpg, color = factor(cyl))) +
  geom_point(size = 3) +
  scale_color_brewer(type = "qual", palette = "Set1") +
  theme_classic() +
  theme(
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
    axis.title = element_text(size = 14),
    legend.title = element_text(size = 12),
    legend.position = c(0.8, 0.8),
    panel.grid.major = element_line(color = "gray90", size = 0.5)
  ) +
  labs(
    title = "Fuel Efficiency vs Engine Power",
    subtitle = "Data from 1974 Motor Trend magazine",
    x = "Gross Horsepower",
    y = "Miles per US Gallon",
    color = "Cylinders",
    caption = "Source: Henderson and Velleman (1981)"
  )
```

### 25. How do you save and export plots?
**Answer:**
**Base R Export:**
```r
# PNG
png("my_plot.png", width = 800, height = 600, res = 300)
plot(mtcars$hp, mtcars$mpg)
dev.off()

# PDF
pdf("my_plot.pdf", width = 8, height = 6)
plot(mtcars$hp, mtcars$mpg)
dev.off()

# JPEG
jpeg("my_plot.jpg", width = 800, height = 600, quality = 95)
plot(mtcars$hp, mtcars$mpg)
dev.off()
```

**ggplot2 Export:**
```r
# Create plot
p <- ggplot(mtcars, aes(x = hp, y = mpg)) +
  geom_point() +
  theme_minimal()

# Save with ggsave
ggsave("ggplot.png", plot = p, width = 8, height = 6, dpi = 300)
ggsave("ggplot.pdf", plot = p, width = 8, height = 6)

# Multiple formats
formats <- c("png", "pdf", "svg")
for (fmt in formats) {
  ggsave(paste0("plot.", fmt), plot = p, width = 8, height = 6)
}
```

---

## Advanced Programming

### 26. How do you write functions in R?
**Answer:**
**Basic Functions:**
```r
# Simple function
square <- function(x) {
  return(x^2)
}

# Function with multiple parameters
calculate_bmi <- function(weight, height, units = "metric") {
  if (units == "metric") {
    bmi <- weight / (height^2)
  } else {
    bmi <- (weight / (height^2)) * 703
  }
  return(bmi)
}

# Function with default arguments
greet <- function(name, greeting = "Hello") {
  paste(greeting, name, "!")
}

# Vectorized function
normalize <- function(x) {
  (x - min(x)) / (max(x) - min(x))
}
```

**Advanced Functions:**
```r
# Function with variable arguments
my_summary <- function(..., na.rm = TRUE) {
  data <- c(...)
  list(
    mean = mean(data, na.rm = na.rm),
    median = median(data, na.rm = na.rm),
    sd = sd(data, na.rm = na.rm),
    length = length(data)
  )
}

# Higher-order functions
apply_function <- function(data, func) {
  func(data)
}

# Closure (function that returns function)
make_multiplier <- function(n) {
  function(x) x * n
}

double <- make_multiplier(2)
triple <- make_multiplier(3)
```

### 27. How do you handle errors and debugging in R?
**Answer:**
**Error Handling:**
```r
# try() for error handling
result <- try({
  x <- 1 / 0
  print("This won't print")
}, silent = TRUE)

if (inherits(result, "try-error")) {
  print("An error occurred")
}

# tryCatch() for more control
safe_divide <- function(a, b) {
  tryCatch({
    result <- a / b
    return(result)
  }, 
  error = function(e) {
    message("Error: ", e$message)
    return(NA)
  },
  warning = function(w) {
    message("Warning: ", w$message)
    return(a / b)
  })
}

# Custom error messages
validate_input <- function(x) {
  if (!is.numeric(x)) {
    stop("Input must be numeric")
  }
  if (any(x < 0)) {
    warning("Negative values detected")
  }
  return(x)
}
```

**Debugging:**
```r
# Debug function
debug(my_function)    # Enter debug mode
undebug(my_function)  # Exit debug mode

# Browser for interactive debugging
my_function <- function(x) {
  y <- x * 2
  browser()  # Pause execution here
  z <- y + 1
  return(z)
}

# Trace function calls
trace(lm)             # Trace lm function
untrace(lm)           # Stop tracing

# Print debugging
debug_function <- function(x) {
  cat("Input:", x, "\n")
  result <- x^2
  cat("Result:", result, "\n")
  return(result)
}
```

### 28. How do you work with environments and scoping?
**Answer:**
**Environment Basics:**
```r
# Global environment
x <- 10
ls()                  # List objects in current environment
environment()         # Current environment

# Function environments
my_function <- function() {
  y <- 20             # Local variable
  print(environment()) # Function environment
  return(y)
}

# Lexical scoping
outer_function <- function(x) {
  inner_function <- function(y) {
    x + y             # x from outer function scope
  }
  return(inner_function)
}

add_five <- outer_function(5)
add_five(3)           # Returns 8
```

**Environment Manipulation:**
```r
# Create new environment
my_env <- new.env()
my_env$a <- 1
my_env$b <- 2

# List objects in environment
ls(envir = my_env)

# Parent environment
parent.env(my_env)

# Search path
search()              # List of environments in search path

# Assign to specific environment
assign("z", 100, envir = .GlobalEnv)
get("z", envir = .GlobalEnv)
```

### 29. How do you create and use S3 classes?
**Answer:**
**S3 Class System:**
```r
# Create S3 object
person <- function(name, age) {
  obj <- list(name = name, age = age)
  class(obj) <- "person"
  return(obj)
}

# Create instances
john <- person("John", 30)
jane <- person("Jane", 25)

# Generic methods
print.person <- function(x, ...) {
  cat("Person:", x$name, "Age:", x$age, "\n")
}

summary.person <- function(object, ...) {
  cat("Summary for", object$name, "\n")
  cat("Age:", object$age, "years old\n")
  if (object$age >= 18) {
    cat("Status: Adult\n")
  } else {
    cat("Status: Minor\n")
  }
}

# Method dispatch
print(john)           # Calls print.person
summary(jane)         # Calls summary.person

# Check class
class(john)           # "person"
inherits(john, "person")  # TRUE
```

**Method Creation:**
```r
# Generic function
greet <- function(x) {
  UseMethod("greet")
}

# Default method
greet.default <- function(x) {
  cat("Hello!\n")
}

# Specific method for person class
greet.person <- function(x) {
  cat("Hello", x$name, "!\n")
}

# Usage
greet(john)           # "Hello John !"
greet("anything")     # "Hello!"
```

### 30. How do you work with packages and namespaces?
**Answer:**
**Package Management:**
```r
# Install packages
install.packages("dplyr")
install.packages(c("ggplot2", "tidyr", "readr"))

# Load packages
library(dplyr)
require(ggplot2)      # Alternative, returns TRUE/FALSE

# Check if package is installed
if (!require(pacman)) {
  install.packages("pacman")
  library(pacman)
}

# Load multiple packages
pacman::p_load(dplyr, ggplot2, tidyr)

# Unload package
detach("package:dplyr", unload = TRUE)
```

**Namespace Usage:**
```r
# Use function without loading package
dplyr::filter(mtcars, mpg > 20)

# Avoid namespace conflicts
stats::filter()       # Base R filter
dplyr::filter()       # dplyr filter

# Import specific functions
importFrom <- function() {
  # In package NAMESPACE file:
  # importFrom(dplyr, filter, select, mutate)
}

# Check loaded packages
search()              # Search path
loadedNamespaces()    # Loaded namespaces
sessionInfo()         # Session information
```

---

## Performance & Best Practices

### 31. How do you optimize R code for performance?
**Answer:**
**Vectorization:**
```r
# Slow: Loop
slow_sum <- function(x) {
  result <- 0
  for (i in 1:length(x)) {
    result <- result + x[i]
  }
  return(result)
}

# Fast: Vectorized
fast_sum <- function(x) {
  sum(x)
}

# Benchmark
library(microbenchmark)
x <- 1:10000
microbenchmark(
  slow = slow_sum(x),
  fast = fast_sum(x),
  times = 100
)
```

**Memory Management:**
```r
# Pre-allocate vectors
# Slow: Growing vector
slow_growth <- function(n) {
  result <- c()
  for (i in 1:n) {
    result <- c(result, i^2)
  }
  return(result)
}

# Fast: Pre-allocated
fast_growth <- function(n) {
  result <- numeric(n)
  for (i in 1:n) {
    result[i] <- i^2
  }
  return(result)
}

# Even faster: Vectorized
fastest_growth <- function(n) {
  (1:n)^2
}
```

**Efficient Data Structures:**
```r
# Use appropriate data structures
# data.table for large datasets
library(data.table)
dt <- data.table(mtcars)
dt[mpg > 20, .(mean_hp = mean(hp)), by = cyl]

# Matrix operations instead of data frames for numeric data
mat <- as.matrix(mtcars[, c("mpg", "hp", "wt")])
cor(mat)  # Faster than cor(mtcars[, c("mpg", "hp", "wt")])
```

### 32. How do you profile and benchmark R code?
**Answer:**
**Profiling:**
```r
# Rprof for profiling
Rprof("profile.out")
# Your code here
result <- lm(mpg ~ ., data = mtcars)
Rprof(NULL)

# View profiling results
summaryRprof("profile.out")

# profvis for interactive profiling
library(profvis)
profvis({
  data <- data.frame(
    x = rnorm(10000),
    y = rnorm(10000)
  )
  model <- lm(y ~ x, data = data)
  summary(model)
})
```

**Benchmarking:**
```r
library(microbenchmark)

# Compare different approaches
x <- 1:1000
microbenchmark(
  loop = {
    result <- 0
    for (i in x) result <- result + i
  },
  vectorized = sum(x),
  times = 1000
)

# System timing
system.time({
  large_data <- matrix(rnorm(1000000), nrow = 1000)
  result <- apply(large_data, 1, mean)
})
```

### 33. What are R coding best practices?
**Answer:**
**Code Style:**
```r
# Good naming conventions
calculate_mean_age <- function(ages) {  # snake_case for functions
  mean(ages, na.rm = TRUE)
}

user_data <- data.frame(...)           # snake_case for variables
MAX_ITERATIONS <- 1000                 # UPPER_CASE for constants

# Proper spacing and indentation
if (condition) {
  do_something()
} else {
  do_something_else()
}

# Function documentation
#' Calculate BMI
#' 
#' @param weight Numeric vector of weights in kg
#' @param height Numeric vector of heights in meters
#' @return Numeric vector of BMI values
#' @examples
#' calculate_bmi(70, 1.75)
calculate_bmi <- function(weight, height) {
  weight / (height^2)
}
```

**Code Organization:**
```r
# Use projects and proper file structure
# project/
#   ├── R/
#   │   ├── functions.R
#   │   └── analysis.R
#   ├── data/
#   ├── output/
#   └── README.md

# Load packages at the top
library(dplyr)
library(ggplot2)

# Source functions
source("R/functions.R")

# Use here package for file paths
library(here)
data <- read.csv(here("data", "input.csv"))
```

### 34. How do you handle large datasets in R?
**Answer:**
**Memory-Efficient Approaches:**
```r
# data.table for large datasets
library(data.table)
large_dt <- fread("large_file.csv")  # Fast reading
large_dt[, mean_value := mean(value), by = group]  # Efficient operations

# Read in chunks
read_in_chunks <- function(file, chunk_size = 10000) {
  con <- file(file, "r")
  on.exit(close(con))
  
  results <- list()
  chunk_num <- 1
  
  while (length(lines <- readLines(con, n = chunk_size)) > 0) {
    # Process chunk
    chunk_data <- process_chunk(lines)
    results[[chunk_num]] <- chunk_data
    chunk_num <- chunk_num + 1
  }
  
  return(do.call(rbind, results))
}

# Use databases
library(DBI)
library(RSQLite)

con <- dbConnect(SQLite(), "large_database.db")
result <- dbGetQuery(con, "SELECT * FROM table WHERE condition")
dbDisconnect(con)
```

**Parallel Processing:**
```r
library(parallel)

# Detect cores
num_cores <- detectCores() - 1

# Parallel apply
cl <- makeCluster(num_cores)
clusterEvalQ(cl, library(dplyr))
results <- parLapply(cl, data_list, process_function)
stopCluster(cl)

# foreach for parallel loops
library(foreach)
library(doParallel)

registerDoParallel(cores = num_cores)
results <- foreach(i = 1:1000, .combine = rbind) %dopar% {
  # Parallel computation
  process_data(i)
}
```

### 35. How do you create reproducible research with R?
**Answer:**
**Reproducible Workflow:**
```r
# Use renv for package management
renv::init()          # Initialize project
renv::snapshot()      # Save package versions
renv::restore()       # Restore packages

# Set seed for reproducibility
set.seed(123)
random_data <- rnorm(100)

# Use R Markdown for reports
# ```{r setup, include=FALSE}
# knitr::opts_chunk$set(echo = TRUE, warning = FALSE, message = FALSE)
# library(dplyr)
# library(ggplot2)
# ```

# Version control with Git
# .gitignore should include:
# .Rproj.user
# .Rhistory
# .RData
# .Ruserdata
```

**Project Structure:**
```r
# Recommended project structure
# project_name/
#   ├── project_name.Rproj
#   ├── README.md
#   ├── renv.lock
#   ├── R/
#   │   ├── 01_data_cleaning.R
#   │   ├── 02_analysis.R
#   │   └── functions.R
#   ├── data/
#   │   ├── raw/
#   │   └── processed/
#   ├── output/
#   │   ├── figures/
#   │   └── tables/
#   ├── reports/
#   │   └── analysis_report.Rmd
#   └── tests/

# Use here package for paths
library(here)
data_path <- here("data", "raw", "input.csv")
output_path <- here("output", "figures", "plot.png")
```

**Documentation:**
```r
# Document functions with roxygen2
#' @title Calculate Summary Statistics
#' @description This function calculates basic summary statistics
#' @param x A numeric vector
#' @param na.rm Logical, should NA values be removed?
#' @return A named list of summary statistics
#' @export
#' @examples
#' summary_stats(c(1, 2, 3, 4, 5))
summary_stats <- function(x, na.rm = TRUE) {
  list(
    mean = mean(x, na.rm = na.rm),
    median = median(x, na.rm = na.rm),
    sd = sd(x, na.rm = na.rm)
  )
}

# Create package documentation
# devtools::document()
# devtools::check()
```

---

*This comprehensive guide covers 35+ essential R programming interview questions with detailed answers and practical examples for data science and statistical analysis interviews.*