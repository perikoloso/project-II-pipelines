#EXPLORING FUNCTIONS
import pandas as dp
import numpy as np

#Check null values and delete rows with nulls
def check_null_values(df):
    v_dict = {}
    for col in df.columns:
        v_missed = np.mean(df[col].isna())
        v_dict[col]=str(round(v_missed*100))+"%"
    df.dropna(how="all",inplace=True)
    return v_dict