import pandas as pd
import numpy as np
import re
from collections import defaultdict

def extract_data(file_path):
    """
    Extracts data corresponding to Wikipedia Admin Elections from corresponding text file.
    
    Parameters:
    - file_path (str): The path to the text file.

    Returns:
    - df (pandas.DataFrame): A DataFrame containing the parsed data with the specified columns.
    """
    
    data = []
    data_dict = defaultdict(list)
    
    with open(file_path, encoding ='utf-8') as data_file:
        for line in data_file: 
            formatted_line = line.strip()
            if formatted_line:
                # parsing the line 
                parsed_line = formatted_line.split(':', 1)
                data_dict[parsed_line[0]].append(parsed_line[1])
                
    df = pd.DataFrame(data_dict)
    return df


def process_dataframe(df):
    """
    Processes a DataFrame in place by performing the following operations:
    
    1. Replaces empty strings with NaN.
    2. Converts specified numeric columns ('VOT', 'RES', 'YEA') to numeric, handling errors with NaN.
    3. Converts 'RES' column values to 1 if the value is 1, else 0.
    4. Converts 'DAT' column to datetime.
    5. Updates specific values in 'DAT' column to predefined datetime values.
    
    Parameters:
    - df (pd.DataFrame): The input DataFrame to be processed in place.
    """
    df.replace('', np.nan, inplace=True)
    
    # Convert specified columns to numeric
    numeric_columns = ['VOT', 'RES', 'YEA']
    df[numeric_columns] = df[numeric_columns].apply(lambda x: pd.to_numeric(x, errors='coerce'))
    
    # Convert 'RES' column to 1 if value is 1, else 0
    df['RES'] = df['RES'].apply(lambda x: 1 if x == 1 else 0)
    
    # Convert 'DAT' column to datetime with specified format
    df['DAT'] = pd.to_datetime(df['DAT'], format='mixed', errors='coerce')
    
    # Update specific values in 'DAT' column
    df.at[6821, 'DAT'] = pd.to_datetime('2012-07-01 14:47')
    df.at[27608, 'DAT'] = pd.to_datetime('2010-01-03 20:44')
    df.at[116963, 'DAT'] = pd.to_datetime('2007-05-26 14:47')
    df.at[70591, 'DAT'] = pd.to_datetime('2008-05-24 03:29')