# src/analysis.py

import pandas as pd
import duckdb
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from utils import (
    ensure_output_dirs, 
    save_table_as_png, 
    save_chart, 
    bucket_scores, 
    set_chart_style
)
from sql_queries import (
    MONTHLY_TREND,
    WIDGET_PERFORMANCE,
    PARTNER_PERFORMANCE,
    DEBTLEVEL_PERFORMANCE,
    CONTACTABILITY_MATRIX,
    FUNNEL_STATUS,
    WIDGET_PARTNER_CROSS
)

sns.set(style="whitegrid")

# ---------------------------------------------------------
# Load + Clean
# ---------------------------------------------------------
def load_and_clean(path):
    df = pd.read_excel(path)
    df["LeadCreated"] = pd.to_datetime(df["LeadCreated"], errors="coerce")
    df["Month"] = df["LeadCreated"].dt.strftime("%Y-%m")

    good = ["Closed", "EP Sent", "EP Received", "EP Confirmed"]
    bad = [
        "Unable to contact - Bad Contact Information",
        "Contacted - Invalid Profile",
        "Contacted - Doesn't Qualify"
    ]

    df["GoodLeadFlag"] = df["CallStatus"].isin(good).astype(int)
    df["BadLeadFlag"] = df["CallStatus"].isin(bad).astype(int)
    df["ClosedFlag"] = (df["CallStatus"] == "Closed").astype(int)

    df = bucket_scores(df)
    return df


# ---------------------------------------------------------
# SQL Segments
# ---------------------------------------------------------
def run_sql(df):
    con = duckdb.connect()
    con.register("leads", df)

    return {
        "monthly": con.execute(MONTHLY_TREND).df(),
        "widget": con.execute(WIDGET_PERFORMANCE).df(),
        "partner": con.execute(PARTNER_PERFORMANCE).df(),
        "debt": con.execute(DEBTLEVEL_PERFORMANCE).df(),
        "matrix": con.execute(CONTACTABILITY_MATRIX).df(),
        "funnel": con.execute(FUNNEL_STATUS).df(),
        "widget_partner": con.execute(WIDGET_PARTNER_CROSS).df()
    }


# ---------------------------------------------------------
# Save Outputs (Charts + Tables)
# ---------------------------------------------------------
def save_outputs(df, seg):

    ensure_output_dirs()
    set_chart_style()

    # -----------------------------
    # Save All Tables
    # -----------------------------
    for name, t in seg.items():
        t.to_csv(f"outputs/tables/{name}.csv", index=False)
        save_table_as_png(t, f"outputs/tables/{name}.png")

    # -----------------------------
    # Chart 1: Monthly Trend
    # -----------------------------
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=seg["monthly"], x="Month", y="good_rate", marker="o", color="#1f77b4", ax=ax)
    ax.set_title("Monthly Good Lead Rate")
    plt.xticks(rotation=45)
    save_chart(fig, "outputs/charts/monthly_good_rate.png")

    # -----------------------------
    # Chart 2: Widget Performance
    # -----------------------------
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(data=seg["widget"].head(15), y="WidgetName", x="good_rate", palette="Set2", ax=ax)
    ax.set_title("Top Widgets by Good Lead Rate")

    # Add annotations
    for p in ax.patches:
        ax.annotate(f"{p.get_width():.1%}",
                    (p.get_width(), p.get_y() + p.get_height()/2),
                    ha="left", va="center")

    save_chart(fig, "outputs/charts/widget_quality.png")

    # -----------------------------
    # Chart 3: Partner Quality
    # -----------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=seg["partner"], y="Partner", x="good_rate", palette="Set3", ax=ax)
    ax.set_title("Partner Lead Quality Comparison")

    for p in ax.patches:
        ax.annotate(f"{p.get_width():.1%}",
                    (p.get_width(), p.get_y() + p.get_height()/2),
                    ha="left", va="center")

    save_chart(fig, "outputs/charts/partner_quality.png")

    # -----------------------------
    # Chart 4: Contactability Heatmap
    # -----------------------------
    pivot = df.groupby(["PhoneBucket","AddressBucket"])["GoodLeadFlag"].mean().unstack()

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(pivot, annot=True, fmt=".1%", cmap="YlGnBu", linewidths=0.5, ax=ax)
    ax.set_title("Heatmap: Lead Quality by Contactability")
    save_chart(fig, "outputs/charts/contactability_heatmap.png")

    # -----------------------------
    # Chart 5: Funnel Chart
    # -----------------------------
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(data=seg["funnel"], x="CallStatus", y="leads", palette="coolwarm", ax=ax)
    plt.xticks(rotation=45)
    ax.set_title("Lead Funnel Distribution")

    save_chart(fig, "outputs/charts/funnel_distribution.png")

    # -----------------------------
    # Chart 6: Partner × Widget
    # -----------------------------
    cross = seg["widget_partner"].pivot(index="Partner", columns="WidgetName", values="good_rate")

    fig, ax = plt.subplots(figsize=(16, 8))
    sns.heatmap(cross, cmap="viridis", ax=ax)
    ax.set_title("Partner × Widget Lead Quality")
    save_chart(fig, "outputs/charts/partner_widget_heatmap.png")

    # -----------------------------
    # Chart 7: Debt Quality
    # -----------------------------
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=seg["debt"], x="DebtLevel", y="good_rate", palette="Pastel2", ax=ax)
    ax.set_title("Good Lead Rate by Debt Level")
    plt.xticks(rotation=45)

    for p in ax.patches:
        ax.annotate(f"{p.get_height():.1%}", 
                    (p.get_x() + p.get_width()/2, p.get_height()),
                    ha="center", va="bottom")

    save_chart(fig, "outputs/charts/debt_level_quality.png")

    # -----------------------------
    # ML Feature Importance
    # -----------------------------
    importance = calculate_feature_importance(df)
    importance.to_csv("outputs/derived_data/feature_importance.csv")

    fig, ax = plt.subplots(figsize=(8, 10))
    sns.barplot(x=importance.head(20), y=importance.head(20).index, palette="Spectral", ax=ax)
    ax.set_title("Top 20 Feature Importances")

    save_chart(fig, "outputs/charts/feature_importance.png")



# ---------------------------------------------------------
# ML Feature Importance
# ---------------------------------------------------------
def calculate_feature_importance(df):
    model_df = df[[
        "GoodLeadFlag", "State", "DebtLevel", "Partner", 
        "WidgetName", "PhoneScore", "AddressScore"
    ]].dropna()

    X = pd.get_dummies(model_df.drop(columns=["GoodLeadFlag"]), drop_first=True)
    y = model_df["GoodLeadFlag"]

    rf = RandomForestClassifier(n_estimators=250, random_state=42)
    rf.fit(X, y)

    return pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
