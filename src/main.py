# src/main.py

from analysis import load_and_clean, run_sql, save_outputs

def main():
    print("Loading dataset...")
    df = load_and_clean("data/leads_raw.xls")

    print("Running SQL analysis...")
    segments = run_sql(df)

    print("Saving outputs...")
    save_outputs(df, segments)

    print("\nAll results generated successfully in the outputs/ folder.")

if __name__ == "__main__":
    main()
