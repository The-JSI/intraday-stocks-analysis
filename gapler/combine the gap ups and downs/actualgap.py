import pandas as pd

glaper = pd.read_excel('glaper.xlsx')
up = pd.read_excel('up.xlsx')
down = pd.read_excel('down.xlsx')

glaper['date'] = pd.to_datetime(glaper['date']).dt.date
up['date'] = pd.to_datetime(up['date']).dt.date
down['date'] = pd.to_datetime(down['date']).dt.date

up["gap_status"] = "up"
down["gap_status"] = "down"

merged = (glaper.merge(up[["date","symbol","gap_status"]],on=["date","symbol"], how="left").merge(down[["date","symbol","gap_status"]], on=["date","symbol"], how="left"))

merged["gap_status"] = merged["gap_status_x"].combine_first(merged["gap_status_y"])
merged = merged.drop(columns=["gap_status_x","gap_status_y"])

merged.to_excel('glaper.xlsx', index = False)