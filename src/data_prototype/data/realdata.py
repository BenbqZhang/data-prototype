import pandas as pd

def load_df_head():
    dataframe_head = pd.read_csv('dataset/processed_data/loc1_head5002.csv', index_col='ChipTime', parse_dates=True)
    return dataframe_head

def load_df_range_1_2():
    dataframe_range_1_2 = pd.read_csv('dataset/processed_data/loc1_line_57600_to_115201.csv', index_col='ChipTime', parse_dates=True)
    return dataframe_range_1_2

def load_df_range_3_4():
    dataframe_range_3_4 = pd.read_csv('dataset/processed_data/loc1_line_172802_to_230403.csv', index_col='ChipTime', parse_dates=True)
    return dataframe_range_3_4
