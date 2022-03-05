import pandas as pd
from datetime import timedelta
from datetime import datetime

loc1_df = pd.read_csv('dataset/processed_data/loc1_fivemins_acc.csv', index_col='ChipTime', parse_dates=True)
loc2_df = pd.read_csv('dataset/processed_data/loc7_fivemins_acc.csv', index_col='ChipTime', parse_dates=True)

loc1_index = ""
loc2_index = ""
timefmt = '%Y-%m-%d %H:%M:%S.%f'

with open('dataset/processed_data/sync_index.txt', 'r') as f:
    for line in f:
        loc1_index, loc2_index = line.strip().split(',')

loc1_index = datetime.strptime(loc1_index, timefmt)
loc2_index = datetime.strptime(loc2_index, timefmt)

origin_offset = (loc2_df.index[0] - loc1_df.index[0]).to_pytimedelta()
origin_offset = int(origin_offset / (timedelta(milliseconds=1)))
manual_sync_offset = int((loc2_index - loc1_index) / (timedelta(milliseconds=1)))

offset = manual_sync_offset - ((manual_sync_offset%10) - (origin_offset%10))

loc2_df.index = loc2_df.index.shift(-offset, freq='ms')

trun_start = max(loc1_df.index[0], loc2_df.index[0])
trun_end = min(loc1_df.index[-1], loc2_df.index[-1])

loc1_df = loc1_df.truncate(before=trun_start, after=trun_end)
loc2_df = loc2_df.truncate(before=trun_start, after=trun_end)

loc1_df.to_csv('dataset/processed_data/loc1_fivemins_acc_sync.csv')
loc2_df.to_csv('dataset/processed_data/loc7_fivemins_acc_sync.csv')
