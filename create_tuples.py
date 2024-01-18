'''
This script creates list of tuples based on datafame
    input: dataframe
    output: list
'''
import pandas as pd

def create_list_of_tuples(df):
    list_of_tuples = []

    for i in range(len(df)):
        x = list(df.iloc[i])
        for j in range(len(x)):
            if pd.isna(x[j]):
                x[j] = None
            else:
                try:
                    x[j] = x[j].item()
                except:
                    pass
        x = tuple(x)
        list_of_tuples.append(x)
    return list_of_tuples