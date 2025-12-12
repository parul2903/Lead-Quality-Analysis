# src/utils.py

import os
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Create output directories
# ---------------------------------------------------------
def ensure_output_dirs():
    os.makedirs("outputs/tables", exist_ok=True)
    os.makedirs("outputs/charts", exist_ok=True)
    os.makedirs("outputs/derived_data", exist_ok=True)

# ---------------------------------------------------------
# Save df as PNG
# ---------------------------------------------------------
def save_table_as_png(df, filepath):
    fig, ax = plt.subplots(figsize=(12, 0.25 * len(df) + 1))
    ax.axis("off")

    tbl = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc="center",
        loc="center"
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8)
    tbl.scale(1, 1.2)

    plt.savefig(filepath, bbox_inches="tight")
    plt.close()

# ---------------------------------------------------------
# Save charts easily
# ---------------------------------------------------------
def save_chart(fig, path):
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)

# ---------------------------------------------------------
# Create Score Buckets
# ---------------------------------------------------------
def bucket_scores(df):
    df["PhoneScore"] = pd.to_numeric(df.get("PhoneScore", 0), errors="coerce").fillna(0)
    df["AddressScore"] = pd.to_numeric(df.get("AddressScore", 0), errors="coerce").fillna(0)

    df["PhoneBucket"] = pd.cut(df["PhoneScore"], [-1, 2, 3, 5], labels=["Low", "Medium", "High"])
    df["AddressBucket"] = pd.cut(df["AddressScore"], [-1, 2, 3, 5], labels=["Low", "Medium", "High"])

    return df
