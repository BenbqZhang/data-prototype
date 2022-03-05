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

def load_df_loc1_fivemins():
    df = pd.read_csv('dataset/processed_data/loc1_fivemins.csv', index_col='ChipTime', parse_dates=True)
    return df

def load_df_loc7_fivemins():
    df = pd.read_csv('dataset/processed_data/loc7_fivemins.csv', index_col='ChipTime', parse_dates=True)
    return df

def load_df_loc1_fivemins_acc():
    df = pd.read_csv('dataset/processed_data/loc1_fivemins_acc.csv', index_col='ChipTime', parse_dates=True)
    return df

def load_df_loc7_fivemins_acc():
    df = pd.read_csv('dataset/processed_data/loc7_fivemins_acc.csv', index_col='ChipTime', parse_dates=True)
    return df

def load_df_No2_loc8_fivemins():
    df = pd.read_csv('dataset/processed_data/D20210102-No2/loc8_fivemins.csv', index_col='ChipTime', parse_dates=True)
    return df

def load_df_No2_loc14_fivemins():
    df = pd.read_csv('dataset/processed_data/D20210102-No2/loc14_fivemins.csv', index_col='ChipTime', parse_dates=True)
    return df

WINDOW_SIZE=256
