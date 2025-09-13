import pandas as pd

# Load files
trading_days = pd.read_csv("https://docs.google.com/spreadsheets/d/1SkkML9xiylt3mij4e68UYTV7UU9bBZoiRRJJc-kDp6g/export?format=csv")
gapler = pd.read_csv("https://docs.google.com/spreadsheets/d/1q-GXwfQ7NsgcBU6vYPtDsK5tkef9ndRVTM3qGcORvvY/export?format=csv")

# Normalize dates
for df in [trading_days, gapler]:
    df["date"] = pd.to_datetime(df["date"],dayfirst=True, errors="coerce")

# Unique sets
trading_dates = set(trading_days["date"].unique())
gapler_dates = set(gapler["date"].unique())

# Mark trading days with/without gap
all_days = pd.DataFrame({"date": sorted(trading_dates)})
all_days["month"] = all_days["date"].dt.to_period("M")
all_days["gap_occurred"] = all_days["date"].isin(gapler_dates)

# Group by month
monthly_summary = (
    all_days.groupby("month")
    .agg(
        total_trading_days=("date", "count"),
        gap_days=("gap_occurred", "sum"),
        sit_out_days=("gap_occurred", lambda x: (~x).sum()),
        sit_out_dates=("date", lambda d: [dt.strftime("%Y-%m-%d") for dt in sorted(d[~all_days.loc[d.index, "gap_occurred"]])])
    )
    .reset_index()
)

print(monthly_summary.to_string(index=False))
