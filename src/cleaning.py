
import pandas as dp

def fix_cols(df):
    clean_lst = []
    for c in df.columns:
        c = c.strip().upper()
        c= re.sub('^STR', '', c)
        clean_lst.append(c)
    df.columns = clean_lst
    return df.columns

def change_col(df,old,new):
    df.rename(columns={old:str.upper(new)},inplace = True)