# Retail Analytics & Sales Forecasting: ML Capstone

## 📌 Project Overview
Retail environments are incredibly dynamic and sensitive to dozens of localized external features, ranging from local holiday spikes to macroeconomic inflation. The primary objective of this project is to build an end-to-end regression Machine Learning framework to accurately forecast weekly sales across different departments and stores. 

By strategically anticipating demand spikes with a high degree of precision, stakeholders and operations management can significantly optimize inventory scaling, reduce the financial overhead of dead stock, and accurately plan localized staffing—especially during business-critical Q4 holiday weeks.

## 📊 Dataset Description
The project leverages a robust historical corporate dataset merged from three different tables, representing over **400,000 recorded weeks** across 45 flagship and standard retail stores.
- `stores data-set.csv`: Anonymized physical footprint sizes and categorical Store Types (A, B, C)
- `Features data set.csv`: Macroeconomic and environmental factors, including regional Temperature, localized Fuel Prices, CPI (Consumer Price Index), Unemployment metrics, and active promotional MarkDown statuses.
- `sales data-set.csv`: Granular weekly sales metrics tracked individually per department and store.

## 🛠 Project Workflow

### 1. Data Wrangling & Feature Engineering
- **Temporal Engineering**: Extracted critical `Year`, `Month`, and `Week` features from string dates to allow algorithms to map specific micro-seasonality mathematically.
- **Null Imputation**: Deterministically imputed missing promotional `MarkDown` metrics with 0 (no promotion) and managed sparse baseline economic values through robust median imputation.
- **Join Architecture**: Dynamically merged the three independent structural datasets based on `Store` and `Date` indices into a unified, deployment-ready Dataframe.

### 2. Exploratory Data Analysis (EDA)
Over **15 comprehensive visualizations** and statistical evaluations were conducted to demystify complex variables.
- **Distribution Analysis**: Mapped severe right-skew distributions within Weekly Sales targets using customized KDE histograms. 
- **Bivariate Analysis**: Evaluated categorical performance anchors (e.g., Type A vs Type C stores) utilizing robust IQR boxplots.
- **Macro-Factor Tracking**: Generated low-alpha scatterplots mapping sales variance cleanly against seemingly unpredictable global metrics (Fuel, Temp, CPI).
- **Multivariate Correlation**: Deployed specialized numerical heatmaps and complex pair plots to isolate linear inter-feature collinearity without distorting algorithm metrics.

### 3. Hypothesis Testing
Deployed unbiased, mathematically rigorous tests to validate our visual assumptions prior to ML implementation:
- **ANOVA (F-Test)**: Formally validated significant mean differences originating distinctly between Store Types (A, B, C).
- **Two-Sample T-Test**: Proved statistically that average `Weekly_Sales` spikes dramatically across denoted Holiday weeks.
- **Pearson Coefficient**: Verified absolute linear strengths chaining localized physical Store Size against final absolute sales parameters.

### 4. Machine Learning Implementation
Three dedicated predictive Regressor models were engineered, moving from simplistic structural baselines to robust non-linear aggregations:
1. **Linear Regression (Baseline)**: Established floor-level numerical predictions.
2. **Decision Tree Regressor**: Bridged linear baseline floors into highly complex categorical modeling structures.
3. **Random Forest Regressor**: Minimized heavy singular tree variance utilizing multi-threaded ensemble logic (`n_estimators=50`, `max_depth=10`). 

## 🚀 Key Outcomes & Business Impact

Through comprehensive modeling, several foundational insights were mathematically realized:
- **Footprint Over Macro-Economics**: Localized macroeconomic distress parameters (`CPI`, `Fuel Price`, `Unemployment`) surprisingly held minimal direct linear correlations with overall product demand. Conversely, the absolute physical `Size` of the store alongside precise micro-seasonality (`Week` metrics) completely dominated the sales pipeline.
- **The "Breadwinner" Sectors**: Departments like `92`, `95`, and `38` single-handedly drive the enterprise revenue floor, proving that any supply disruptions to these hubs will irreparably crash profitability.
- **Ultimate Model Deployment**: The **Random Forest Regressor** dramatically outperformed all baseline metrics by effectively handling localized, dense, non-linear holiday sales spikes. The resulting robust architecture accurately minimizes overstock and ensures agile reactions to demand, securely locking the enterprise against massive opportunity losses.

## 📁 Repository Structure
- `Final_Retail_Analytics_Project.ipynb`: The complete, deployment-ready Jupyter Notebook containing the full execution, EDA graphs, and active ML training arrays without a single logged runtime error.
- `build.py`: A unique parsing environment architected to dynamically construct and populate the final notebook.
- `final_rf_model.pkl`: The serialized, deployment-ready Random Forest ML model, ready for localized unseen data.
- Initial CSV datasets (`sales data-set.csv`, `stores data-set.csv`, `Features data set.csv`).

---
**Author**: Jiya Sadaria  
**Type**: Supervised Machine Learning Capstone - Regression Analysis
