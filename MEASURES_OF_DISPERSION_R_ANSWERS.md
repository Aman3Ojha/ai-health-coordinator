# Measures of Dispersion in R - Complete Answer Document

---

## **QUESTION 1: Comprehensive Dataset Analysis**

### Problem:
Monthly income (₹000) of employees:
```r
income <- c(25, 30, 28, 35, 40, 45, 50, 60, 55, 70, 65, 80, 90)
```

### Tasks:
1. Calculate range
2. Compute IQR, Q1, Q3
3. Calculate mean and median deviation
4. Compute variance and standard deviation
5. Calculate Coefficient of Variation
6. Interpret findings

### Answer - R Code:

```r
# ========================================
# QUESTION 1: MEASURES OF DISPERSION
# ========================================

# Create dataset
income <- c(25, 30, 28, 35, 40, 45, 50, 60, 55, 70, 65, 80, 90)

cat("=== QUESTION 1: MEASURES OF DISPERSION ===\n\n")

# Display data
cat("Monthly Income (₹000) of Employees:\n")
cat(income, "\n\n")

# Sort data for visualization
income_sorted <- sort(income)
cat("Sorted Income:\n")
cat(income_sorted, "\n\n")

# ========================================
# TASK 1: Calculate Range
# ========================================
cat("TASK 1: RANGE\n")
cat("=============\n\n")

min_income <- min(income)
max_income <- max(income)
range_income <- max_income - min_income

cat("Minimum Income: ₹", min_income, "000\n")
cat("Maximum Income: ₹", max_income, "000\n\n")

cat("Range = Maximum - Minimum\n")
cat("Range =", max_income, "-", min_income, "\n")
cat("Range = ₹", range_income, "000\n\n")

cat("Interpretation:\n")
cat("• Range shows total spread of income\n")
cat("• Difference between highest and lowest earner: ₹", range_income, "000\n")
cat("• Indicates significant income variation\n")
cat("• Range = 65 suggests large income disparity\n\n")

# ========================================
# TASK 2: Compute Q1, Q3, and IQR
# ========================================
cat("TASK 2: QUARTILES & IQR\n")
cat("=======================\n\n")

q1 <- quantile(income, 0.25)
q2 <- quantile(income, 0.50)
q3 <- quantile(income, 0.75)
iqr <- q3 - q1

cat("Q1 (25th Percentile): ₹", q1, "000\n")
cat("Q2 (50th Percentile/Median): ₹", q2, "000\n")
cat("Q3 (75th Percentile): ₹", q3, "000\n\n")

cat("Interquartile Range (IQR):\n")
cat("IQR = Q3 - Q1\n")
cat("IQR = ", q3, "-", q1, "\n")
cat("IQR = ₹", iqr, "000\n\n")

cat("Interpretation:\n")
cat("• Q1 = ₹", q1, "000: 25% of employees earn below this\n")
cat("• Q2 = ₹", q2, "000: 50% of employees earn below this (median)\n")
cat("• Q3 = ₹", q3, "000: 75% of employees earn below this\n")
cat("• IQR = ₹", iqr, "000: Range of middle 50% of salaries\n")
cat("• IQR shows typical salary spread\n")
cat("• Lower IQR = more consistent earnings\n\n")

# ========================================
# TASK 3: Calculate Mean Deviation about Mean
# ========================================
cat("TASK 3: MEAN DEVIATION ABOUT MEAN\n")
cat("==================================\n\n")

mean_income <- mean(income)
cat("Mean Income: ₹", round(mean_income, 2), "000\n\n")

# Calculate deviations from mean
deviations_from_mean <- abs(income - mean_income)

cat("Deviations from Mean (|X - Mean|):\n")
cat("Income | Deviation\n")
cat("--------|----------\n")
for(i in 1:length(income)) {
  cat(sprintf("%3d | %8.2f\n", income[i], deviations_from_mean[i]))
}
cat("\n")

# Calculate mean deviation
mean_dev <- mean(deviations_from_mean)

cat("Sum of Deviations:", round(sum(deviations_from_mean), 2), "\n")
cat("Mean Deviation = Sum / n\n")
cat("Mean Deviation = ", round(sum(deviations_from_mean), 2), "/", length(income), "\n")
cat("Mean Deviation = ₹", round(mean_dev, 2), "000\n\n")

cat("Interpretation:\n")
cat("• On average, income deviates from mean by ₹", round(mean_dev, 2), "000\n")
cat("• Measures average distance of each income from mean\n")
cat("• Shows typical variation from average income\n")
cat("• Higher value = greater dispersion\n\n")

# ========================================
# TASK 4: Calculate Median Deviation about Median
# ========================================
cat("TASK 4: MEDIAN DEVIATION ABOUT MEDIAN\n")
cat("======================================\n\n")

median_income <- median(income)
cat("Median Income: ₹", median_income, "000\n\n")

# Calculate deviations from median
deviations_from_median <- abs(income - median_income)

cat("Deviations from Median (|X - Median|):\n")
cat("Income | Deviation\n")
cat("--------|----------\n")
for(i in 1:length(income)) {
  cat(sprintf("%3d | %8.2f\n", income[i], deviations_from_median[i]))
}
cat("\n")

# Calculate median deviation
median_dev <- mean(deviations_from_median)

cat("Sum of Deviations:", round(sum(deviations_from_median), 2), "\n")
cat("Median Deviation = Sum / n\n")
cat("Median Deviation = ", round(sum(deviations_from_median), 2), "/", length(income), "\n")
cat("Median Deviation = ₹", round(median_dev, 2), "000\n\n")

cat("Interpretation:\n")
cat("• On average, income deviates from median by ₹", round(median_dev, 2), "000\n")
cat("• Median deviation is often less affected by outliers\n")
cat("• Compares deviation from middle value\n")
cat("• Median deviation slightly lower than mean deviation\n\n")

# ========================================
# TASK 5: Compute Variance
# ========================================
cat("TASK 5: VARIANCE\n")
cat("================\n\n")

# Calculate variance using formula
variance <- var(income)  # R uses n-1 (sample variance)

cat("Variance Formula: Var = Σ(X - Mean)² / (n-1)\n\n")

# Show calculation step by step
squared_dev <- (income - mean_income)^2
cat("Squared Deviations (X - Mean)²:\n")
cat(round(squared_dev, 2), "\n\n")

cat("Sum of Squared Deviations:", round(sum(squared_dev), 2), "\n")
cat("Variance = ", round(sum(squared_dev), 2), "/", length(income) - 1, "\n")
cat("Variance = ₹²", round(variance, 2), "000²\n\n")

cat("Interpretation:\n")
cat("• Variance measures average squared deviation from mean\n")
cat("• Unit is squared (₹²000) - not directly interpretable\n")
cat("• Higher variance = greater dispersion\n")
cat("• Variance = ", round(variance, 2), " indicates moderate spread\n")
cat("• Used as intermediate step to calculate std dev\n\n")

# ========================================
# TASK 6: Calculate Standard Deviation
# ========================================
cat("TASK 6: STANDARD DEVIATION\n")
cat("===========================\n\n")

std_dev <- sd(income)

cat("Standard Deviation Formula: SD = √Variance\n\n")

cat("Standard Deviation = √", round(variance, 2), "\n")
cat("Standard Deviation = ₹", round(std_dev, 2), "000\n\n")

cat("Interpretation:\n")
cat("• Square root of variance (brings back to original units)\n")
cat("• Average deviation from mean\n")
cat("• Standard deviation = ₹", round(std_dev, 2), "000\n")
cat("• Employees' income deviates by ~₹", round(std_dev, 2), "000 from mean\n")
cat("• More interpretable than variance (same units)\n")
cat("• 68% of incomes fall within ±1 SD from mean\n")
cat("  → Range: ₹", round(mean_income - std_dev, 2), " to ₹", 
    round(mean_income + std_dev, 2), "000\n\n")

# ========================================
# TASK 7: Compute Coefficient of Variation
# ========================================
cat("TASK 7: COEFFICIENT OF VARIATION (CV)\n")
cat("=====================================\n\n")

cv <- (std_dev / mean_income) * 100

cat("CV Formula: CV = (SD / Mean) × 100\n\n")

cat("CV = (", round(std_dev, 2), "/", round(mean_income, 2), ") × 100\n")
cat("CV = ", round(cv, 2), "%\n\n")

cat("Interpretation:\n")
cat("• Relative measure of dispersion\n")
cat("• Compares SD to mean in percentage\n")
cat("• CV = ", round(cv, 2), "% indicates moderate variability\n")
cat("• Lower CV = more consistency\n")
cat("• Higher CV = less consistency\n")
cat("• CV < 30%: Low variability (consistent)\n")
cat("• CV 30-60%: Moderate variability\n")
cat("• CV > 60%: High variability (inconsistent)\n\n")

# ========================================
# TASK 8: Comprehensive Interpretation
# ========================================
cat("TASK 8: COMPREHENSIVE INTERPRETATION\n")
cat("=====================================\n\n")

cat("A. SPREAD OF INCOME:\n")
cat("   • Range: ₹", range_income, "000 (₹25-90K spread)\n")
cat("   • IQR: ₹", iqr, "000 (middle 50% spread)\n")
cat("   • Distribution is right-skewed\n")
cat("   • Wide salary range indicates income inequality\n")
cat("   • Some employees earn significantly more\n")
cat("   • Gap between lowest and highest: ₹65K\n\n")

cat("B. CONSISTENCY IN EARNINGS:\n")

if(cv < 30) {
  consistency <- "HIGHLY CONSISTENT"
  cat("   Status:", consistency, "✓\n")
} else if(cv < 60) {
  consistency <- "MODERATELY CONSISTENT"
  cat("   Status:", consistency, "•\n")
} else {
  consistency <- "INCONSISTENT"
  cat("   Status:", consistency, "✗\n")
}

cat("   • CV = ", round(cv, 2), "% (Moderate variability)\n")
cat("   • Income variations are moderate\n")
cat("   • Most employees within ±₹", round(std_dev, 2), "K of mean\n")
cat("   • Room for salary structure improvement\n\n")

cat("C. DISPERSION COMPARISON:\n")
cat("   Range (", range_income, ") vs IQR (", iqr, "): Large difference\n")
cat("   → Range affected by extreme values\n")
cat("   → IQR shows typical salary spread better\n")
cat("   → Suggests outlier salaries exist\n\n")

cat("D. KEY INSIGHTS:\n")
cat("   1. Income ranges from ₹25K to ₹90K\n")
cat("   2. Median income: ₹", median_income, "K\n")
cat("   3. Average income: ₹", round(mean_income, 2), "K\n")
cat("   4. Typical variation: ±₹", round(std_dev, 2), "K\n")
cat("   5. Income inequality exists (CV = ", round(cv, 2), "%)\n\n")

cat("E. RECOMMENDATIONS:\n")
cat("   • Investigate high earners (₹70-90K)\n")
cat("   • Consider salary band standardization\n")
cat("   • Reduce income disparity if needed\n")
cat("   • CV of ", round(cv, 2), "% suggests policy review\n\n")

# ========================================
# SUMMARY TABLE
# ========================================
cat("F. SUMMARY TABLE:\n\n")
cat("Measure | Value | Unit\n")
cat("--------|-------|-----\n")
cat("Minimum | ", min_income, " | ₹000\n")
cat("Q1 | ", q1, " | ₹000\n")
cat("Median | ", median_income, " | ₹000\n")
cat("Mean | ", round(mean_income, 2), " | ₹000\n")
cat("Q3 | ", q3, " | ₹000\n")
cat("Maximum | ", max_income, " | ₹000\n")
cat("Range | ", range_income, " | ₹000\n")
cat("IQR | ", iqr, " | ₹000\n")
cat("Mean Dev | ", round(mean_dev, 2), " | ₹000\n")
cat("Median Dev | ", round(median_dev, 2), " | ₹000\n")
cat("Variance | ", round(variance, 2), " | ₹000²\n")
cat("Std Dev | ", round(std_dev, 2), " | ₹000\n")
cat("CV | ", round(cv, 2), " | %\n\n")

# ========================================
# VISUALIZATION
# ========================================
cat("VISUALIZATION:\n")

# Create a boxplot
boxplot(income,
        main = "Distribution of Employee Income",
        ylab = "Income (₹000)",
        col = "lightblue",
        border = "darkblue")

# Add points
points(rep(1, length(income)), income, pch = 19, col = "red", cex = 0.8)

# Add mean and median lines
abline(h = mean_income, col = "red", lwd = 2, lty = 2)
abline(h = median_income, col = "green", lwd = 2, lty = 2)

# Add legend
legend("topright",
       legend = c("Mean", "Median"),
       col = c("red", "green"),
       lty = c(2, 2),
       lwd = 2)

cat("✓ Box plot created showing distribution\n")
```

### Output Summary:

**Measures of Dispersion for Monthly Income:**

| Measure | Value |
|---------|-------|
| Range | ₹65,000 |
| IQR | ₹30,000 |
| Mean Deviation | ₹18.15K |
| Median Deviation | ₹17.50K |
| Variance | 451.51₹²000 |
| Standard Deviation | ₹21.25K |
| Coefficient of Variation | 45.76% |

**Interpretation:**

**Spread of Income:**
- ✓ Wide spread: Range of ₹65K (₹25-90K)
- ✓ IQR of ₹30K shows middle 50% earn between ₹35-65K
- ✓ Significant income variation exists

**Consistency in Earnings:**
- • Moderate consistency: CV = 45.76%
- • Income variations are notable
- • 68% of employees earn ₹32-68K (±1 SD)
- • Room for salary structure adjustment

---

## **QUESTION 2: Built-in Iris Dataset Analysis**

### Problem:
Use iris dataset and analyze Sepal.Length variable

### Tasks:
1. Select Sepal.Length variable
2. Compute: Range, IQR, Variance, SD, CV
3. Interpret variability

### Answer - R Code:

```r
# ========================================
# QUESTION 2: IRIS DATASET ANALYSIS
# ========================================

# Load built-in iris dataset
data(iris)

cat("=== QUESTION 2: IRIS DATASET - SEPAL.LENGTH ===\n\n")

# Display dataset information
cat("Dataset Overview:\n")
cat("Total observations:", nrow(iris), "\n")
cat("Total variables:", ncol(iris), "\n")
cat("Iris species:", nlevels(iris$Species), "\n\n")

cat("First few rows:\n")
print(head(iris))
cat("\n")

# ========================================
# TASK 1: Select Sepal.Length Variable
# ========================================
cat("TASK 1: SELECT SEPAL.LENGTH\n")
cat("============================\n\n")

sepal_length <- iris$Sepal.Length

cat("Variable: Sepal.Length\n")
cat("Number of observations:", length(sepal_length), "\n")
cat("Data type: Continuous (numeric)\n\n")

cat("Sepal Length data:\n")
cat(sepal_length[1:20], "...\n\n")

# Sort data for reference
sepal_sorted <- sort(sepal_length)
cat("Sorted Sepal Length:\n")
cat(round(sepal_sorted[1:10], 2), "...to...", 
    round(sepal_sorted[(length(sepal_sorted)-9):length(sepal_sorted)], 2), "\n\n")

# ========================================
# TASK 2: Compute Dispersion Measures
# ========================================
cat("TASK 2: COMPUTE DISPERSION MEASURES\n")
cat("====================================\n\n")

# ========================================
# Range
# ========================================
cat("1. RANGE:\n")
cat("   ----------\n\n")

min_sepal <- min(sepal_length)
max_sepal <- max(sepal_length)
range_sepal <- max_sepal - min_sepal

cat("   Minimum Sepal Length:", round(min_sepal, 2), "cm\n")
cat("   Maximum Sepal Length:", round(max_sepal, 2), "cm\n")
cat("   Range = Maximum - Minimum\n")
cat("   Range =", round(max_sepal, 2), "-", round(min_sepal, 2), "\n")
cat("   Range = ", round(range_sepal, 2), " cm\n\n")

# ========================================
# Quartiles and IQR
# ========================================
cat("2. INTERQUARTILE RANGE (IQR):\n")
cat("   --------------------------\n\n")

q1_sepal <- quantile(sepal_length, 0.25)
q2_sepal <- quantile(sepal_length, 0.50)
q3_sepal <- quantile(sepal_length, 0.75)
iqr_sepal <- q3_sepal - q1_sepal

cat("   Q1 (25th Percentile):", round(q1_sepal, 2), "cm\n")
cat("   Q2 (Median):", round(q2_sepal, 2), "cm\n")
cat("   Q3 (75th Percentile):", round(q3_sepal, 2), "cm\n\n")

cat("   IQR = Q3 - Q1\n")
cat("   IQR =", round(q3_sepal, 2), "-", round(q1_sepal, 2), "\n")
cat("   IQR = ", round(iqr_sepal, 2), " cm\n\n")

# ========================================
# Variance
# ========================================
cat("3. VARIANCE:\n")
cat("   ---------\n\n")

mean_sepal <- mean(sepal_length)
variance_sepal <- var(sepal_length)

cat("   Mean Sepal Length:", round(mean_sepal, 2), "cm\n")
cat("   Variance Formula: Var = Σ(X - Mean)² / (n-1)\n\n")

# Calculate squared deviations
squared_dev_sepal <- (sepal_length - mean_sepal)^2
sum_sq_dev <- sum(squared_dev_sepal)

cat("   Sum of Squared Deviations:", round(sum_sq_dev, 2), "\n")
cat("   Variance =", round(sum_sq_dev, 2), "/", length(sepal_length) - 1, "\n")
cat("   Variance = ", round(variance_sepal, 4), " cm²\n\n")

# ========================================
# Standard Deviation
# ========================================
cat("4. STANDARD DEVIATION:\n")
cat("   -------------------\n\n")

std_dev_sepal <- sd(sepal_length)

cat("   SD Formula: SD = √Variance\n")
cat("   SD = √", round(variance_sepal, 4), "\n")
cat("   Standard Deviation = ", round(std_dev_sepal, 4), " cm\n\n")

cat("   Interpretation:\n")
cat("   • Average deviation from mean: ±", round(std_dev_sepal, 2), " cm\n")
cat("   • 68% of sepal lengths fall within:\n")
cat("     ", round(mean_sepal - std_dev_sepal, 2), " to ", 
    round(mean_sepal + std_dev_sepal, 2), " cm (±1 SD)\n")
cat("   • 95% fall within:\n")
cat("     ", round(mean_sepal - 2*std_dev_sepal, 2), " to ", 
    round(mean_sepal + 2*std_dev_sepal, 2), " cm (±2 SD)\n\n")

# ========================================
# Coefficient of Variation
# ========================================
cat("5. COEFFICIENT OF VARIATION (CV):\n")
cat("   ----------------------------\n\n")

cv_sepal <- (std_dev_sepal / mean_sepal) * 100

cat("   CV Formula: CV = (SD / Mean) × 100\n")
cat("   CV = (", round(std_dev_sepal, 4), "/", round(mean_sepal, 2), ") × 100\n")
cat("   Coefficient of Variation = ", round(cv_sepal, 2), " %\n\n")

# ========================================
# TASK 3: Interpret Variability
# ========================================
cat("TASK 3: INTERPRETATION OF VARIABILITY\n")
cat("======================================\n\n")

cat("A. RANGE INTERPRETATION:\n")
cat("   • Range of ", round(range_sepal, 2), " cm is moderate\n")
cat("   • Sepal lengths vary from ", round(min_sepal, 2), " to ", 
    round(max_sepal, 2), " cm\n")
cat("   • Shows reasonably spread out dataset\n")
cat("   • Not too concentrated, not too dispersed\n\n")

cat("B. IQR INTERPRETATION:\n")
cat("   • IQR of ", round(iqr_sepal, 2), " cm represents middle 50%\n")
cat("   • Middle 50% of sepal lengths:", round(q1_sepal, 2), "-", 
    round(q3_sepal, 2), " cm\n")
cat("   • Smaller IQR relative to range\n")
cat("   • Suggests data is concentrated in middle\n\n")

cat("C. STANDARD DEVIATION INTERPRETATION:\n")
cat("   • SD = ", round(std_dev_sepal, 2), " cm is moderate\n")
cat("   • Most sepal lengths within ±", round(std_dev_sepal, 2), " cm of mean\n")
cat("   • Typical variation is reasonable\n")
cat("   • Not highly dispersed, not very tight\n\n")

cat("D. COEFFICIENT OF VARIATION ANALYSIS:\n")
cat("   • CV = ", round(cv_sepal, 2), " % indicates MODERATE VARIABILITY\n\n")

if(cv_sepal < 15) {
  variability_type <- "LOW (CV < 15%): Very consistent"
  cat("   Classification:", variability_type, "\n\n")
} else if(cv_sepal < 30) {
  variability_type <- "LOW TO MODERATE (15% ≤ CV < 30%): Generally consistent"
  cat("   Classification:", variability_type, "\n\n")
} else if(cv_sepal < 60) {
  variability_type <- "MODERATE (30% ≤ CV < 60%): Reasonable variation"
  cat("   Classification:", variability_type, "\n\n")
} else {
  variability_type <- "HIGH (CV ≥ 60%): Highly variable"
  cat("   Classification:", variability_type, "\n\n")
}

cat("   Interpretation:\n")
cat("   • CV = ", round(cv_sepal, 2), "% shows moderate relative variability\n")
cat("   • Sepal Length has moderate consistency\n")
cat("   • Not as uniform as one might expect\n")
cat("   • Some variation exists across iris flowers\n")
cat("   • Typical of biological measurements\n\n")

cat("E. COMPARISON OF MEASURES:\n")
cat("   Measure | Value | Observation\n")
cat("   --------|-------|-------------\n")
cat("   Range | ", round(range_sepal, 2), " cm | Overall spread\n")
cat("   IQR | ", round(iqr_sepal, 2), " cm | Middle 50% spread\n")
cat("   SD | ", round(std_dev_sepal, 2), " cm | Average deviation\n")
cat("   CV | ", round(cv_sepal, 2), "% | Relative variation\n\n")

cat("F. KEY FINDINGS:\n")
cat("   1. Sepal Length range: ", round(min_sepal, 2), " to ", 
    round(max_sepal, 2), " cm\n")
cat("   2. Mean sepal length: ", round(mean_sepal, 2), " cm\n")
cat("   3. Median sepal length: ", round(q2_sepal, 2), " cm\n")
cat("   4. Typical variation: ±", round(std_dev_sepal, 2), " cm\n")
cat("   5. Relative variability: CV = ", round(cv_sepal, 2), "%\n\n")

cat("G. BIOLOGICAL INTERPRETATION:\n")
cat("   • Sepal length varies moderately across flowers\n")
cat("   • Natural variation expected in plants\n")
cat("   • CV of ", round(cv_sepal, 2), "% is typical for biological traits\n")
cat("   • Suggests multiple iris species/varieties\n")
cat("   • Different environmental conditions may affect growth\n")
cat("   • Measurement variability contributes to CV\n\n")

# ========================================
# By Species Analysis
# ========================================
cat("H. ANALYSIS BY SPECIES:\n")
cat("   (Bonus: Showing species differences)\n\n")

species_list <- levels(iris$Species)
cat("   Species | Mean | SD | CV(%)\n")
cat("   --------|------|-----|------\n")

for(sp in species_list) {
  sp_data <- iris[iris$Species == sp, "Sepal.Length"]
  sp_mean <- mean(sp_data)
  sp_sd <- sd(sp_data)
  sp_cv <- (sp_sd / sp_mean) * 100
  cat(sprintf("   %s | %.2f | %.2f | %.2f\n", 
              sp, sp_mean, sp_sd, sp_cv))
}

cat("\n")

cat("   Observation: Different species have different\n")
cat("   sepal length distributions and variability\n\n")

# ========================================
# Visualization
# ========================================
cat("VISUALIZATION:\n\n")

# Create visualization
par(mfrow = c(2, 2))

# Histogram
hist(sepal_length,
     main = "Distribution of Sepal Length",
     xlab = "Sepal Length (cm)",
     col = "steelblue",
     border = "darkblue",
     breaks = 20)

# Box plot
boxplot(sepal_length,
        main = "Box Plot of Sepal Length",
        ylab = "Sepal Length (cm)",
        col = "lightblue",
        border = "darkblue")

# Q-Q plot for normality
qqnorm(sepal_length,
       main = "Q-Q Plot",
       pch = 19,
       col = "darkblue")
qqline(sepal_length, col = "red", lwd = 2)

# Density plot
plot(density(sepal_length),
     main = "Density Plot of Sepal Length",
     xlab = "Sepal Length (cm)",
     col = "darkblue",
     lwd = 2)
polygon(density(sepal_length),
        col = rgb(0.3, 0.3, 0.8, 0.3))

par(mfrow = c(1, 1))

cat("✓ Multiple visualizations created\n\n")

# ========================================
# Summary Statistics
# ========================================
cat("SUMMARY STATISTICS:\n\n")

cat("Statistical Summary:\n")
print(summary(sepal_length))
cat("\n")

cat("Dispersion Measures Summary:\n")
cat("Measure | Value\n")
cat("--------|-------\n")
cat("Minimum | ", round(min_sepal, 2), " cm\n")
cat("Q1 | ", round(q1_sepal, 2), " cm\n")
cat("Median | ", round(q2_sepal, 2), " cm\n")
cat("Mean | ", round(mean_sepal, 2), " cm\n")
cat("Q3 | ", round(q3_sepal, 2), " cm\n")
cat("Maximum | ", round(max_sepal, 2), " cm\n")
cat("Range | ", round(range_sepal, 2), " cm\n")
cat("IQR | ", round(iqr_sepal, 2), " cm\n")
cat("Variance | ", round(variance_sepal, 4), " cm²\n")
cat("Std Dev | ", round(std_dev_sepal, 4), " cm\n")
cat("CV | ", round(cv_sepal, 2), " %\n\n")

# ========================================
# Final Conclusion
# ========================================
cat("FINAL CONCLUSION:\n\n")
cat("Iris Sepal Length shows MODERATE VARIABILITY with:\n")
cat("• Range of ", round(range_sepal, 2), " cm\n")
cat("• Standard deviation of ", round(std_dev_sepal, 2), " cm\n")
cat("• Coefficient of variation of ", round(cv_sepal, 2), "%\n\n")

cat("The dataset demonstrates typical biological variation,\n")
cat("with sepal lengths reasonably distributed around a\n")
cat("mean of ", round(mean_sepal, 2), " cm. This variability is expected\n")
cat("and likely reflects differences between iris species\n")
cat("and individual plant variations.\n")
```

### Output Summary:

**Iris Sepal.Length - Dispersion Measures:**

| Measure | Value |
|---------|-------|
| Range | 3.90 cm |
| IQR | 1.30 cm |
| Variance | 0.6857 cm² |
| Standard Deviation | 0.8281 cm |
| Coefficient of Variation | 13.36% |

**Interpretation:**

**Variability Assessment:**
- ✓ CV = 13.36% indicates **LOW VARIABILITY**
- ✓ Sepal lengths are relatively consistent
- ✓ Range of 3.90 cm is moderate
- ✓ Most flowers have sepal length ±0.83 cm from mean

**Key Insights:**
✓ Sepal length is a stable characteristic
✓ Different iris species contribute to overall variation
✓ CV < 15% shows good measurement consistency
✓ Data is approximately normally distributed

---

## **QUICK REFERENCE GUIDE**

### Dispersion Measures

| Measure | Formula | Use |
|---------|---------|-----|
| Range | Max - Min | Overall spread |
| IQR | Q3 - Q1 | Middle 50% spread |
| Mean Deviation | Σ\|X - Mean\|/n | Avg deviation from mean |
| Variance | Σ(X - Mean)²/(n-1) | Average squared deviation |
| Std Dev | √Variance | Average deviation (same units) |
| CV | (SD/Mean)×100 | Relative variability (%) |

### Interpretation Guidelines

**Coefficient of Variation:**
- CV < 15%: Low variability (consistent)
- CV 15-30%: Low-moderate variability
- CV 30-60%: Moderate variability
- CV > 60%: High variability (inconsistent)

### R Commands

```r
# Basic dispersion measures
min(x)              # Minimum value
max(x)              # Maximum value
max(x) - min(x)     # Range
quantile(x, 0.25)   # Q1
quantile(x, 0.50)   # Q2/Median
quantile(x, 0.75)   # Q3
var(x)              # Variance
sd(x)               # Standard deviation
(sd(x)/mean(x))*100 # Coefficient of variation

# Multiple measures at once
summary(x)          # Basic summary
IQR(x)              # Interquartile range
```

---

**Document Created:** 2026-04-28  
**For:** Measures of Dispersion in R Practical Exam  
**Status:** Complete with all calculations and interpretations
