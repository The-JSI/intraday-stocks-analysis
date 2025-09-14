import pandas as pd

gapler_url = "https://docs.google.com/spreadsheets/d/1q-GXwfQ7NsgcBU6vYPtDsK5tkef9ndRVTM3qGcORvvY/export?format=csv"
gapler = pd.read_csv(gapler_url)

gapler["date"] = pd.to_datetime(gapler["date"], dayfirst=True, errors="coerce")

all_list = (gapler.groupby("date")["symbol"].apply(list).reset_index())
#print(all_list.to_string())


def datefind():
    while True:
        query_str = input("enter the date: ")
        try:
            query = pd.to_datetime(query_str, format="%d/%m/%y", errors="raise")
        except Exception as e:
            print(f"Invalid date format: {e}")
            continue

        datefind = gapler.loc[gapler['date'] == query, ['symbol','gap_status','close_status']]
        print(datefind if not datefind.empty else f"No stocks found for {query.date()}")

                        
def stockfind(): #also returns the total number of stocks including the query that opened at a gap up or down
    query = input("enter the stock: ").upper()
    stockfind = gapler.loc[gapler['symbol'] == query, ['date','gap_status','close_status']]
    all_counts = gapler.groupby("date")["symbol"].count().reset_index(name=f"total stocks including {query}")
    result = stockfind.merge(all_counts, on="date", how="left")
    cols = ['date', f"total stocks including {query}",'gap_status','close_status'] #push close_status to the right
    result = result[cols]
    print(result.to_string(index=False))

def countfind():  # also returns the stocks that had the required intraday momentum
    try:
        n = int(input("Enter the number of stocks: "))
    except ValueError:
        print("Please enter a valid integer.")
        return

    # Ensure date columns are real datetimes (date-only)
    if not pd.api.types.is_datetime64_any_dtype(gapler["date"]):
        gapler["date"] = pd.to_datetime(gapler["date"], errors="coerce", dayfirst=True)

    # Count how many stocks gapped per date
    all_counts = gapler.groupby("date")["symbol"].count().reset_index(name="total_stocks")

    # Filter dates where total_stocks == n
    target_dates = all_counts.loc[all_counts["total_stocks"] == n, "date"]

    if target_dates.empty:
        print(f"No dates found where exactly {n} stocks gapped.")
        return

    # Make the target dates into a list
    target_dates_list = list(pd.to_datetime(target_dates))

    # Get gapped stocks (plain list) for those dates
    result = (
        gapler.loc[gapler["date"].isin(target_dates_list)]
        .groupby("date")["symbol"]
        .apply(list)
        .reset_index(name="gapped_stocks")
    )

    green = (
        gapler.loc[gapler["close_status"] == "green"]
        .groupby("date")["symbol"]
        .apply(list)
        .reset_index(name="closed green")
    )

    red = (
        gapler.loc[gapler["close_status"] == "red"]
        .groupby("date")["symbol"]
        .apply(list)
        .reset_index(name="closed red")
    )

    up = (
        gapler.loc[gapler["gap_status"] == "up"]
        .groupby("date")["symbol"]
        .apply(list)
        .reset_index(name="gap up")
    )

    down = (
        gapler.loc[gapler["gap_status"] == "down"]
        .groupby("date")["symbol"]
        .apply(list)
        .reset_index(name="gap down")
    )

    # Merge green/red/up/down lists onto the result dates while preserving order from result
    momentum_result = result[["date"]].merge(green, on="date", how="left").merge(red, on="date", how="left").merge(up, on="date", how="left").merge(down, on="date", how="left")

    # create lists of column values and repalce empty ones with a []
    for col in ["closed green", "closed red", "gap up", "gap down"]:
        momentum_result[col] = momentum_result[col].apply(lambda x: x if isinstance(x, list) else [])

    # Final join with the original gapped stock lists
    final = result.merge(momentum_result, on="date", how="left")

    # Reorder columns
    final = final[["date", "gapped_stocks", "gap up", "gap down", "closed green", "closed red"]]

    counts = len(final)
    print(final.to_string(index=False))
    print()
    print(f"total- {counts}")

#stockfind()
#datefind()
#countfind()

#---------------------------------------------------------------------
#---------------------------------------------------------------------
