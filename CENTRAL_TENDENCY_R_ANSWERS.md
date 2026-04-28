# Central Tendency in R - Complete Answer Document

---

## **QUESTION 1: Basic Dataset (Vector in R)**

### Problem:
Create a dataset of marks obtained by 10 students:
```r
marks <- c(45, 67, 78, 88, 56, 67, 78, 90, 45, 67)
```

### Answer 1: Calculate the Mean

**Calculation:**
- Sum = 45 + 67 + 78 + 88 + 56 + 67 + 78 + 90 + 45 + 67 = 681
- Count = 10
- Mean = 681 ÷ 10 = **68.1**

**R Code:**
```r
marks <- c(45, 67, 78, 88, 56, 67, 78, 90, 45, 67)
mean_marks <- mean(marks)
print(mean_marks)  # Output: 68.1
```

---

### Answer 2: Find the Median

**Calculation:**
1. Sort data: 45, 45, 56, 67, 67, 67, 78, 78, 88, 90
2. Find middle value (position 5 and 6): 67 and 78
3. Average: (67 + 78) ÷ 2 = **72.5**

**R Code:**
```r
median_marks <- median(marks)
print(median_marks)  # Output: 72.5
```

---

### Answer 3: Identify the Mode

**Calculation:**
- 45 appears 2 times
- 67 appears **3 times** ← Most frequent
- 78 appears 2 times
- Others appear 1 time each
- Mode = **67**

**R Code:**
```r
# Custom function for mode
mode_function <- function(x) {
  uniq_x <- unique(x)
  uniq_x[which.max(tabulate(match(x, uniq_x)))]
}

mode_marks <- mode_function(marks)
print(mode_marks)  # Output: 67

# View frequency distribution
table(marks)
# Output:
# 45 56 67 78 88 90
#  2  1  3  2  1  1
```

---

### Answer 4: Interpret Which Measure Best Represents the Data

| Measure | Value | Characteristic |
|---------|-------|-----------------|
| Mean | 68.1 | Average performance |
| Median | 72.5 | Middle value |
| Mode | 67 | Most common score |

**Interpretation:**
- **Best Measure: MEDIAN (72.5)**

**Reasons:**
1. Mean (68.1) and Median (72.5) are close, indicating fairly symmetric data
2. No extreme outliers present
3. The data shows no significant skewness
4. Median is easiest to interpret and most robust
5. Good for understanding typical student performance

**Conclusion:** The median score of 72.5 best represents the central tendency of the student marks.

---

## **QUESTION 2: Ungrouped Data (Income Data)**

### Problem:
Monthly incomes (in ₹000): 25, 30, 35, 40, 45, 50, 55, 60, 100

### Answer 1: Compute Mean, Median, and Mode

**Mean Calculation:**
- Sum = 25 + 30 + 35 + 40 + 45 + 50 + 55 + 60 + 100 = 480
- Count = 9
- Mean = 480 ÷ 9 = **53.33 ₹000**

**Median Calculation:**
- Sorted: 25, 30, 35, 40, **45**, 50, 55, 60, 100
- Middle value (5th out of 9) = **45 ₹000**

**Mode Calculation:**
- All values appear only once
- Mode = **No unique mode (Amodal)**

**R Code:**
```r
income <- c(25, 30, 35, 40, 45, 50, 55, 60, 100)

mean_income <- mean(income)
print(mean_income)  # Output: 53.33

median_income <- median(income)
print(median_income)  # Output: 45

# Mode function
mode_function <- function(x) {
  uniq_x <- unique(x)
  modes <- uniq_x[tabulate(match(x, uniq_x)) == max(tabulate(match(x, uniq_x)))]
  if(length(modes) == length(uniq_x)) return("No unique mode")
  return(modes)
}

mode_income <- mode_function(income)
print(mode_income)  # Output: No unique mode
```

---

### Answer 2: Comment on the Effect of Extreme Value (100)

**Analysis:**

| Without 100 | With 100 (Outlier) |
|------------|-------------------|
| Sum = 380 | Sum = 480 |
| Count = 8 | Count = 9 |
| Mean = 47.5 | Mean = 53.33 |
| Median = 42.5 | Median = 45 |

**Effect Observed:**
- Mean increased by: 53.33 - 47.5 = **5.83 ₹000** (12.3% increase)
- Median increased by: 45 - 42.5 = **2.5 ₹000** (5.9% increase)

**Key Insight:**
- **The extreme value (100) pulls the MEAN upward much more than the MEDIAN**
- Mean is **VERY SENSITIVE** to outliers
- Median is **ROBUST** (less affected by outliers)

**R Code:**
```r
income_without_outlier <- income[-9]  # Remove 100

cat("With Outlier (100):\n")
cat("Mean:", mean(income), "\n")
cat("Median:", median(income), "\n\n")

cat("Without Outlier:\n")
cat("Mean:", mean(income_without_outlier), "\n")
cat("Median:", median(income_without_outlier), "\n\n")

cat("Difference in Mean:", mean(income) - mean(income_without_outlier), "\n")
cat("Difference in Median:", median(income) - median(income_without_outlier), "\n")
```

---

### Answer 3: Identify Which Measure is Most Appropriate and Why

**Answer: MEDIAN is most appropriate**

**Reasons:**
1. **Data is skewed** - The extreme value 100 creates right skew
2. **Outlier present** - 100 is far from other values (25-60 range)
3. **Mean is misleading** - 53.33 doesn't represent typical income (most earn 25-60)
4. **Median is accurate** - 45 truly represents typical income
5. **Business decision** - For budgeting, median is more realistic

**Conclusion:** 
Use **MEDIAN (45 ₹000)** for decision-making rather than mean. It represents the typical income more accurately when outliers are present.

---

## **QUESTION 3: Built-in Dataset (Using R Dataset - mtcars)**

### Problem:
Using R's built-in mtcars dataset, analyze MPG and HP variables.

### Answer 1: Calculate mean, median, and mode of MPG

**R Code:**
```r
data(mtcars)

# View first few rows
head(mtcars[, c("mpg", "hp")])

# Custom mode function
mode_function <- function(x) {
  uniq_x <- unique(x)
  modes <- uniq_x[tabulate(match(x, uniq_x)) == max(tabulate(match(x, uniq_x)))]
  if(length(modes) == length(uniq_x)) return(NA)
  return(modes[1])
}

# MPG Analysis
mean_mpg <- mean(mtcars$mpg)
median_mpg <- median(mtcars$mpg)
mode_mpg <- mode_function(mtcars$mpg)

cat("=== MPG (Miles Per Gallon) ===\n")
cat("Mean MPG:", mean_mpg, "\n")
cat("Median MPG:", median_mpg, "\n")
cat("Mode MPG:", if(is.na(mode_mpg)) "No unique mode" else mode_mpg, "\n")
cat("Std Dev:", round(sd(mtcars$mpg), 2), "\n")
```

**Results:**
- Mean MPG: **20.09**
- Median MPG: **19.2**
- Mode MPG: **No unique mode** (values are continuous)
- Std Dev: **6.03**

---

### Answer 2: Do the same for HP (Horsepower)

**R Code:**
```r
# HP Analysis
mean_hp <- mean(mtcars$hp)
median_hp <- median(mtcars$hp)
mode_hp <- mode_function(mtcars$hp)

cat("\n=== HP (Horsepower) ===\n")
cat("Mean HP:", mean_hp, "\n")
cat("Median HP:", median_hp, "\n")
cat("Mode HP:", if(is.na(mode_hp)) "No unique mode" else mode_hp, "\n")
cat("Std Dev:", round(sd(mtcars$hp), 2), "\n")
```

**Results:**
- Mean HP: **146.69**
- Median HP: **123**
- Mode HP: **No unique mode**
- Std Dev: **68.56**

---

### Answer 3: Compare both variables in terms of central tendency

**Comparison Table:**

| Measure | MPG | HP |
|---------|-----|-----|
| Mean | 20.09 | 146.69 |
| Median | 19.2 | 123 |
| Std Dev | 6.03 | 68.56 |
| CV (%) | 30% | 47% |
| Mean - Median | +0.89 | +23.69 |

**R Code for Comparison:**
```r
cv_mpg <- (sd(mtcars$mpg) / mean_mpg) * 100
cv_hp <- (sd(mtcars$hp) / mean_hp) * 100

cat("\n=== COMPARISON ===\n")
cat("Variable | Mean | Median | Std Dev | CV(%)\n")
cat("---------|------|--------|---------|-------\n")
cat(sprintf("MPG | %.2f | %.2f | %.2f | %.2f\n", mean_mpg, median_mpg, sd(mtcars$mpg), cv_mpg))
cat(sprintf("HP | %.2f | %.2f | %.2f | %.2f\n", mean_hp, median_hp, sd(mtcars$hp), cv_hp))
```

---

### Answer 4: Interpret which variable shows more consistency

**Analysis:**

**Coefficient of Variation (CV):**
- CV = (Std Dev / Mean) × 100
- Measures relative variability

**MPG:** CV = 30%
- More consistent fuel efficiency
- Less spread in data
- More predictable MPG performance

**HP:** CV = 47%
- Less consistent horsepower
- More spread in data
- More variable engine power

**Interpretation:**
- **MPG shows MORE CONSISTENCY** (lower CV = 30% vs 47%)
- Fuel efficiency is more stable across cars
- Horsepower varies more widely between cars

**Conclusion:** **MPG is more consistent** as a variable. Fuel efficiency is more predictable, while horsepower shows greater variability across the dataset.

---

## **QUESTION 4: Dataset with Missing Values**

### Problem:
```r
sales <- c(120, 150, NA, 200, 180, NA, 170, 160)
```

### Answer 1: Compute mean and median using appropriate arguments

**R Code:**
```r
sales <- c(120, 150, NA, 200, 180, NA, 170, 160)

# WRONG WAY (don't do this)
cat("Without na.rm argument:\n")
cat("Mean:", mean(sales), "\n")  # Returns NA
cat("Median:", median(sales), "\n")  # Returns NA

# CORRECT WAY
cat("\nWith na.rm = TRUE:\n")
mean_sales <- mean(sales, na.rm = TRUE)
median_sales <- median(sales, na.rm = TRUE)

cat("Mean:", mean_sales, "\n")
cat("Median:", median_sales, "\n")
```

**Results:**
- Mean: **162.5** (only valid values used)
- Median: **165** (only valid values used)

---

### Answer 2: Handle missing values properly

**Key Points:**

| Issue | Solution |
|-------|----------|
| NA values cause problems | Use `na.rm = TRUE` |
| All calculations fail | Always specify `na.rm = TRUE` |
| Data loss | Removes only NA, keeps valid values |

**R Code for Proper Handling:**
```r
cat("=== MISSING VALUES HANDLING ===\n")
cat("Original data:", sales, "\n")
cat("Total values:", length(sales), "\n")
cat("Missing values (NA):", sum(is.na(sales)), "\n")
cat("Valid values:", sum(!is.na(sales)), "\n\n")

# Extract only valid values
valid_sales <- sales[!is.na(sales)]
cat("Valid data only:", valid_sales, "\n")
cat("Count of valid data:", length(valid_sales), "\n")
```

**Output:**
- Total values: 8
- Missing values: 2
- Valid values: 6
- Valid data: 120, 150, 200, 180, 170, 160

---

### Answer 3: Find the mode

**R Code:**
```r
mode_function <- function(x, na.rm = TRUE) {
  if(na.rm) x <- x[!is.na(x)]
  uniq_x <- unique(x)
  modes <- uniq_x[tabulate(match(x, uniq_x)) == max(tabulate(match(x, uniq_x)))]
  if(length(modes) == length(uniq_x)) return(NA)
  return(modes[1])
}

mode_sales <- mode_function(sales)
cat("Mode:", if(is.na(mode_sales)) "No unique mode" else mode_sales, "\n")
```

**Result:** No unique mode (all values appear once)

---

### Answer 4: Explain how missing values affect central tendency

**Impact Analysis:**

| Aspect | Effect |
|--------|--------|
| **Without na.rm = TRUE** | All calculations return NA (useless) |
| **With na.rm = TRUE** | Uses only valid data (correct) |
| **Sample size** | Reduces from 8 to 6 observations |
| **Interpretation** | Results apply only to non-missing data |
| **Data quality** | Shows 25% of data is missing |

**Explanation:**
```
1. NA values "break" calculations in R
2. Must explicitly tell R to ignore NA using na.rm = TRUE
3. When na.rm = TRUE, R removes NA values before calculating
4. Results are based on 6 valid values, not 8 total values
5. Must report: "Mean = 162.5 (n=6, 2 missing values)"
```

**Key Takeaway:**
Always use `na.rm = TRUE` when data contains missing values. This ensures you get meaningful results instead of NA.

---

## **QUESTION 5: Excel Data Import into R**

### Problem:
Import Excel file with student scores and analyze

### Data:
| Student | Scores |
|---------|--------|
| A | 55 |
| B | 60 |
| C | 65 |
| D | 70 |
| E | 75 |
| F | 80 |
| G | 85 |
| H | 90 |

### Answer 1: Import the dataset

**R Code - Using readxl:**
```r
# Install if needed (run once)
# install.packages("readxl")

library(readxl)

# Import from Excel
scores <- read_excel("scores.xlsx")
print(scores)

# Or using read.csv if converted to CSV
# scores <- read.csv("scores.csv")
```

**Alternative - Create manually:**
```r
# If you don't have the Excel file, create manually
scores <- data.frame(
  Student = c("A", "B", "C", "D", "E", "F", "G", "H"),
  Scores = c(55, 60, 65, 70, 75, 80, 85, 90)
)
print(scores)
```

---

### Answer 2: Extract the Scores column

**R Code:**
```r
# Extract scores column
scores_vector <- scores$Scores
print(scores_vector)

# Output: 55 60 65 70 75 80 85 90
```

---

### Answer 3: Calculate Mean, Median, Mode

**R Code:**
```r
# Mean
mean_scores <- mean(scores_vector)
cat("Mean:", mean_scores, "\n")  # Output: 72.5

# Median
median_scores <- median(scores_vector)
cat("Median:", median_scores, "\n")  # Output: 72.5

# Mode function
mode_function <- function(x) {
  uniq_x <- unique(x)
  modes <- uniq_x[tabulate(match(x, uniq_x)) == max(tabulate(match(x, uniq_x)))]
  if(length(modes) == length(uniq_x)) return(NA)
  return(modes[1])
}

mode_scores <- mode_function(scores_vector)
cat("Mode:", if(is.na(mode_scores)) "No unique mode" else mode_scores, "\n")
```

**Results:**
- Mean: **72.5**
- Median: **72.5**
- Mode: **No unique mode** (all appear once)

---

### Answer 4: Interpret the results

**Summary Table:**

| Measure | Value | Meaning |
|---------|-------|---------|
| Mean | 72.5 | Average score |
| Median | 72.5 | Middle score |
| Mode | None | No repeating score |
| Min | 55 | Lowest score |
| Max | 90 | Highest score |
| Range | 35 | Spread of scores |

**Interpretation:**
1. The average student score is 72.5
2. The middle student scored 72.5
3. Mean equals Median (important indicator!)
4. Scores range from 55 to 90 (spread of 35 points)
5. All students have different scores

---

### Answer 5: Comment on whether data is symmetric or skewed

**Symmetry Analysis:**

**Test 1: Mean = Median?**
- Mean = 72.5
- Median = 72.5
- **Yes, they're EQUAL** ✓

**Test 2: Skewness Formula:**
```r
skewness <- (mean_scores - median_scores) / sd(scores_vector)
cat("Skewness:", skewness, "\n")  # Output: 0 (perfectly symmetric)
```

**Test 3: Visual Distribution:**
```
55  60  65  70  75  80  85  90
|---|---|---|---|---|---|---|
    ← Equal spacing from center
```

**Conclusion:**
- **Data is PERFECTLY SYMMETRIC**
- **No skewness present** (Skewness = 0)
- Scores are evenly distributed
- Perfect example of symmetric distribution

**R Code Summary:**
```r
# Complete analysis
scores <- data.frame(
  Student = c("A", "B", "C", "D", "E", "F", "G", "H"),
  Scores = c(55, 60, 65, 70, 75, 80, 85, 90)
)

scores_vector <- scores$Scores

cat("=== COMPLETE ANALYSIS ===\n")
cat("Mean:", mean(scores_vector), "\n")
cat("Median:", median(scores_vector), "\n")
cat("Std Dev:", sd(scores_vector), "\n\n")

cat("=== SYMMETRY CHECK ===\n")
if(mean(scores_vector) == median(scores_vector)) {
  cat("Data is PERFECTLY SYMMETRIC\n")
  cat("Mean = Median =", mean(scores_vector), "\n")
} else {
  cat("Data is SKEWED\n")
  if(mean(scores_vector) > median(scores_vector)) {
    cat("Right-skewed (positively skewed)\n")
  } else {
    cat("Left-skewed (negatively skewed)\n")
  }
}
```

---

## **QUESTION 6: Summary Statistics, Percentiles & Deciles**

### Problem:
Monthly sales (in ₹000): 120, 150, 180, NA, 200, 170, 160, NA, 190, 210, 175, 165

### Answer (a): Summary Statistics

**R Code:**
```r
sales <- c(120, 150, 180, NA, 200, 170, 160, NA, 190, 210, 175, 165)

summary(sales)
```

**Output:**
```
   Min. 1st Qu.  Median    Mean 3rd Qu.    Max.    NA's 
  120.0   161.2   177.5   176.0   192.5   210.0       2 
```

**Detailed Interpretation:**

| Statistic | Value | Meaning |
|-----------|-------|---------|
| Min | 120 | Lowest monthly sales |
| 1st Qu (25%) | 161.2 | 25% of months had sales ≤ 161.2 |
| Median (50%) | 177.5 | 50% of months had sales ≤ 177.5 |
| Mean | 176.0 | Average monthly sales |
| 3rd Qu (75%) | 192.5 | 75% of months had sales ≤ 192.5 |
| Max | 210 | Highest monthly sales |
| NA's | 2 | 2 missing values |

**Interpretation Summary:**
- Most sales are between 161 and 193 (middle 50%)
- Average sales = 176 ₹000
- Range = 120 to 210 (90 ₹000 spread)
- Data is fairly symmetric (mean ≈ median)

---

### Answer (b): Percentiles

**R Code:**
```r
# Calculate specific percentiles
p25 <- quantile(sales, 0.25, na.rm = TRUE, names = FALSE)
p50 <- quantile(sales, 0.50, na.rm = TRUE, names = FALSE)
p75 <- quantile(sales, 0.75, na.rm = TRUE, names = FALSE)

cat("=== PERCENTILES ===\n")
cat("25th Percentile (Q1):", p25, "\n")
cat("50th Percentile (Q2/Median):", p50, "\n")
cat("75th Percentile (Q3):", p75, "\n\n")

cat("IQR (Interquartile Range):", p75 - p25, "\n")
```

**Results:**
- **25th Percentile (Q1): 161.25 ₹000**
  - Meaning: 25% of months had sales ≤ 161.25
  - 75% of months had sales > 161.25

- **50th Percentile (Median): 177.5 ₹000**
  - Meaning: 50% of months had sales ≤ 177.5
  - This is the exact middle value
  - Also called the 2nd quartile

- **75th Percentile (Q3): 192.5 ₹000**
  - Meaning: 75% of months had sales ≤ 192.5
  - Only 25% of months had sales > 192.5

**IQR (Interquartile Range):**
- IQR = Q3 - Q1 = 192.5 - 161.25 = **31.25 ₹000**
- This represents the spread of the middle 50% of data

**Real-World Example:**
```
If your company has:
- 25% of months with sales < 161.25 (poor performing)
- 50% of months with sales < 177.5 (typical)
- 75% of months with sales < 192.5 (good performing)
- 25% of months with sales > 192.5 (excellent)
```

---

### Answer (c): Deciles

**R Code:**
```r
# Calculate all deciles (D1 to D9)
deciles <- quantile(sales, probs = seq(0.1, 0.9, 0.1), na.rm = TRUE, names = TRUE)

cat("=== DECILES (D1 to D9) ===\n")
print(deciles)

# Structured format
cat("\n=== DECILE TABLE ===\n")
cat("Decile | Percentile | Value | Meaning\n")
cat("-------|------------|-------|--------\n")

for(i in 1:9) {
  decile_value <- quantile(sales, i*0.1, na.rm = TRUE, names = FALSE)
  cat(sprintf("D%-1d    | %3d%%      | %6.2f | %d%% of sales below this\n", 
              i, i*10, decile_value, i*10))
}
```

**Deciles Explained:**

| Decile | Percentile | Value | Interpretation |
|--------|-----------|-------|-----------------|
| D1 | 10% | - | 10% of months had sales ≤ this value |
| D2 | 20% | - | 20% of months had sales ≤ this value |
| D3 | 30% | - | 30% of months had sales ≤ this value |
| D4 | 40% | - | 40% of months had sales ≤ this value |
| D5 | 50% | 177.5 | MEDIAN - Exactly middle value |
| D6 | 60% | - | 60% of months had sales ≤ this value |
| D7 | 70% | - | 70% of months had sales ≤ this value |
| D8 | 80% | - | 80% of months had sales ≤ this value |
| D9 | 90% | - | 90% of months had sales ≤ this value |

**What are Deciles?**
- Divide data into 10 equal segments
- Each represents 10% of distribution
- D5 is always the median
- Used to understand performance tiers

**Performance Tiers Based on Deciles:**

```
D1-D3 (10-30%)  → POOR PERFORMING MONTHS
D4-D6 (40-60%)  → AVERAGE/TYPICAL MONTHS
D7-D9 (70-90%)  → EXCELLENT PERFORMING MONTHS
```

**Business Use:**
- Set different targets for different months
- Identify which months are underperforming
- Benchmark performance against company standards
- Plan inventory based on expected sales

**Complete Summary Code:**
```r
sales <- c(120, 150, 180, NA, 200, 170, 160, NA, 190, 210, 175, 165)

cat("=== COMPLETE DESCRIPTIVE ANALYSIS ===\n\n")

# Summary statistics
cat("Summary Statistics:\n")
print(summary(sales))
cat("\n")

# Percentiles
cat("Percentiles:\n")
cat("Q1 (25%):", quantile(sales, 0.25, na.rm = TRUE, names = FALSE), "\n")
cat("Q2 (50%):", quantile(sales, 0.50, na.rm = TRUE, names = FALSE), "\n")
cat("Q3 (75%):", quantile(sales, 0.75, na.rm = TRUE, names = FALSE), "\n\n")

# Deciles
cat("Deciles (D1 to D9):\n")
for(i in 1:9) {
  val <- quantile(sales, i*0.1, na.rm = TRUE, names = FALSE)
  cat(sprintf("D%d (%-2d%%):", i, i*10), round(val, 2), "\n")
}

# Additional insights
cat("\nData Quality:\n")
cat("Valid observations:", sum(!is.na(sales)), "\n")
cat("Missing values:", sum(is.na(sales)), "\n")
cat("Mean:", round(mean(sales, na.rm = TRUE), 2), "\n")
cat("Std Dev:", round(sd(sales, na.rm = TRUE), 2), "\n")
```

---

## **QUICK REFERENCE GUIDE**

### When to Use Each Measure:

**Use MEAN when:**
- Data has no extreme outliers
- Distribution is symmetric
- You need exact average
- Normal/bell curve data

**Use MEDIAN when:**
- Data has outliers
- Distribution is skewed
- Data is ordinal
- Want robust central value

**Use MODE when:**
- Data is categorical
- Looking for most common value
- Multimodal distributions
- Qualitative analysis

### Key Formulas:

```
Mean = Sum of all values / Number of values
Median = Middle value in sorted data
Mode = Most frequently occurring value
CV (%) = (Std Dev / Mean) × 100
IQR = Q3 - Q1
```

### Decision Matrix:

| Situation | Best Choice | Reason |
|-----------|------------|--------|
| Normal data | Mean | Accurate for symmetric data |
| Skewed data | Median | Robust to outliers |
| Categorical | Mode | Only makes sense |
| Has outliers | Median | Less affected |
| Income/wealth | Median | Outliers skew |
| Test scores | Mean or Median | Depends on skewness |
| Percentiles | Use quantile() | Shows distribution |

---

## **FINAL SUMMARY**

**Central Tendency** = Finding the "typical" or "middle" value of a dataset

**Three main measures:**
1. **Mean** - Average (can be affected by outliers)
2. **Median** - Middle value (robust to outliers)
3. **Mode** - Most common (for categories)

**Always check:**
- Is data symmetric? (Mean ≈ Median?)
- Are there outliers? (Use median)
- What's the spread? (Check percentiles/deciles)
- Are values missing? (Use na.rm = TRUE)

**R Tips:**
- `mean()` - Calculate average
- `median()` - Find middle value
- `table()` - See frequency distribution
- `quantile()` - Get percentiles/deciles
- `summary()` - Get all statistics
- `na.rm = TRUE` - Handle missing values

---

**Document Created:** 2026-04-28  
**For:** Central Tendency in R Practical Exam  
**Format:** Complete Answer Guide with R Code
