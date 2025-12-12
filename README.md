# Lead Quality Analysis

This project analyzes ~3,000 marketing leads to understand **lead quality trends**, identify **key performance drivers**, and recommend **strategies to improve lead outcomes**. The analysis uses **Python**, **DuckDB SQL**, and **Machine Learning** to deliver actionable business insights.

---

## Objectives
- Measure **lead quality over time** (trend analysis).
- Identify **drivers of quality**: widget, partner, debt level, contactability.
- Understand funnel performance and where leads drop off.
- Explore opportunities to **increase lead quality by 20%**, enabling a higher CPL.
- Produce charts, segmentation tables, and ML-driven feature importance.

---

## Key Insights
- **PhoneScore and AddressScore** are the strongest predictors of lead quality.  
- Certain **widgets** and **partners** consistently outperform others.  
- Higher **debt levels** are associated with increased qualification likelihood.  
- Most funnel drop-offs occur between **EP Sent → EP Received**.  
- Mix-shifting away from low-performing sources yields **>20% improvement**.

---

## Project Structure

```plaintext
LeadQualityAnalysis/
├── data/
│   └── leads_raw.xls               # Raw dataset
│
├── outputs/
│   ├── tables/                     # All tables (CSV + PNG)
│   ├── charts/                     # All charts (PNG)
│   └── derived_data/               # Feature importance, etc.
│
├── src/
│   ├── analysis.py                 # Full analysis workflow
│   ├── sql_queries.py              # DuckDB SQL queries
│   ├── utils.py                    # Helper functions for charts/tables
│   └── main.py                     # Runs the entire pipeline
│
└── notebooks/
    └── LeadQualityAnalysis.ipynb   # EDA notebook (optional)

```

## How to Run the Project

### Install dependencies:
```bash
pip install -r requirements.txt
```
```bash
python src/main.py
```

## Technologies Used

- **Python:** Pandas, NumPy, Matplotlib, Seaborn  
- **SQL:** DuckDB (embedded analytics engine)  
- **Machine Learning:** Random Forest (Scikit-learn)  
- **Jupyter Notebook** for analysis and visualization 

