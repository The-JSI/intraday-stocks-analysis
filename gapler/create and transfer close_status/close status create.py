#gives the complete list of all stocks with close status from 2 separate lists with all green and red stocks with the momentum
import pandas as pd

# Load the data
all_list = pd.read_excel('fut 5 complete.xlsx')
green = pd.read_excel('in the green.xlsx')
red = pd.read_excel('in the red.xlsx')

# Ensure column names are consistent
all_list.columns = all_list.columns.str.strip().str.lower()
green.columns = green.columns.str.strip().str.lower()
red.columns = red.columns.str.strip().str.lower()

# Convert 'date' column to datetime and strip the time part
all_list['date'] = pd.to_datetime(all_list['date']).dt.date
green['date'] = pd.to_datetime(green['date']).dt.date
red['date'] = pd.to_datetime(red['date']).dt.date

# Add a tuple column for easier lookup
all_list['key'] = list(zip(all_list['date'], all_list['symbol']))
green_keys = set(zip(green['date'], green['symbol']))
red_keys = set(zip(red['date'], red['symbol']))

# Map the close status
def get_close_status(row):
    if row['key'] in green_keys:
        return 'green'
    elif row['key'] in red_keys:
        return 'red'
    else:
        return 'unknown'  # Optional: you can drop this if you're sure all are covered

all_list['close_status'] = all_list.apply(get_close_status, axis=1)

# Drop the helper 'key' column if not needed
all_list.drop(columns='key', inplace=True)

# Optional: save result
all_list.to_excel('fut_5_complete_with_status.xlsx', index=False)
