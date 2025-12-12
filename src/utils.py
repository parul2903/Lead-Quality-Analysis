# src/utils.py

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# ---------------------------------------------------------
# Create Output Directories
# ---------------------------------------------------------
def ensure_output_dirs():
    os.makedirs("outputs/tables", exist_ok=True)
    os.makedirs("outputs/charts", exist_ok=True)
    os.makedirs("outputs/derived_data", exist_ok=True)

# ---------------------------------------------------------
# Global Style for Charts
# ---------------------------------------------------------
def set_chart_style():
    rcParams.update({
        "figure.dpi": 200,
        "savefig.dpi": 300,
        "font.size": 11,
        "axes.titlesize": 15,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10
    })

# ---------------------------------------------------------
# Save DataFrame as PNG (professionally formatted)
# ---------------------------------------------------------
def save_table_as_png(df, filepath, header_color="#1f77b4"):
    """
    Saves a dataframe as a clean PNG with:
    - Colored header
    - Zebra rows
    - Word-friendly formatting
    """

    fig, ax = plt.subplots(figsize=(12, 0.35 * len(df) + 1))
    ax.axis("off")

    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc="center",
        loc="center"
    )

    table.auto_set_font_size(False)
    table.set_fontsize(9)

    # Header styling
    for j in range(len(df.columns)):
        cell = table[0, j]
        cell.set_facecolor(header_color)
        cell.set_text_props(color="white", weight="bold")

    # Zebra striping
    for i in range(1, len(df) + 1):
        for j in range(len(df.columns)):
            cell = table[i, j]
            if i % 2 == 0:
                cell.set_facecolor("#f2f3f4")

    table.scale(1, 1.25)
    plt.savefig(filepath, bbox_inches="tight")
    plt.close()

# ---------------------------------------------------------
# Save Chart
# ---------------------------------------------------------
def save_chart(fig, path):
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)

# ---------------------------------------------------------
# Bucket Scores (Phone & Address)
# ---------------------------------------------------------
def bucket_scores(df):
    df["PhoneScore"] = pd.to_numeric(df.get("PhoneScore", 0), errors="coerce").fillna(0)
    df["AddressScore"] = pd.to_numeric(df.get("AddressScore", 0), errors="coerce").fillna(0)

    df["PhoneBucket"] = pd.cut(df["PhoneScore"], [-1, 2, 3, 5], labels=["Low", "Medium", "High"])
    df["AddressBucket"] = pd.cut(df["AddressScore"], [-1, 2, 3, 5], labels=["Low", "Medium", "High"])

    return df
