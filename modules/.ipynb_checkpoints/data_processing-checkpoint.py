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
    6. Marks distinct elections with 'ELECTION_ID' column
    
    Parameters:
    - df (pd.DataFrame): The input DataFrame to be processed in place.
    """
    df['DAT'].replace('', np.nan, inplace=True)
    df['SRC'].replace('', np.nan, inplace=True)
    
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
    
    
    df['ELECTION_ID'] = 0
    current_id = 1

    for index, row in df.iterrows():
        tgt_value = row['TGT']

        # Check if the 'TGT' value is different from the previous row
        if index > 0 and df.at[index - 1, 'TGT'] != tgt_value:
            current_id += 1  # Increment ELECTION_ID for a new 'TGT' value

        df.at[index, 'ELECTION_ID'] = current_id
        
        
def create_elections_df(df):
    """
    Create a summary DataFrame for elections.

    Parameters:
    - df: DataFrame containing election data with columns 'ELECTION_ID', 'TGT', 'RES', 'VOT', and 'DAT'.

    Returns:
    - elections_df: Summary DataFrame with columns 'ELECTION_ID', 'TGT', 'RES', 'Total Votes', 'Positive Votes',
      'Negative Votes', 'Neutral Votes', 'Positive Percentage', 'Negative Percentage', 'Neutral Percentage',
      'Earliest Voting Date', 'Latest Voting Date'.
    """
    # Group by 'ELECTION_ID', 'TGT', 'RES'
    grouped_df = df.groupby(['ELECTION_ID', 'TGT', 'RES'])

    # Calculate counts and percentages
    counts = grouped_df['VOT'].count()
    positive_votes = grouped_df['VOT'].apply(lambda x: (x == 1).sum())
    negative_votes = grouped_df['VOT'].apply(lambda x: (x == -1).sum())
    neutral_votes = grouped_df['VOT'].apply(lambda x: (x == 0).sum())
    total_votes = counts.sum()

    # Calculate percentages
    positive_percentage = (positive_votes / counts) * 100
    negative_percentage = (negative_votes / counts) * 100
    neutral_percentage = (neutral_votes / counts) * 100

    # Get earliest and latest voting dates
    earliest_date = grouped_df['DAT'].min()
    latest_date = grouped_df['DAT'].max()

    # Create the summary DataFrame
    elections_df = pd.DataFrame({
        'Total Votes': counts,
        'Positive Votes': positive_votes,
        'Negative Votes': negative_votes,
        'Neutral Votes': neutral_votes,
        'Positive Percentage': positive_percentage,
        'Negative Percentage': negative_percentage,
        'Neutral Percentage': neutral_percentage,
        'Earliest Voting Date': earliest_date,
        'Latest Voting Date': latest_date
    }).reset_index()

    return elections_df


def create_candidates_df(df):
    """
    Create a summary DataFrame for candidates based on 'TGT' (candidate).

    Parameters:
    - df: DataFrame containing election data with columns 'TGT', 'ELECTION_ID', 'TXT'.

    Returns:
    - candidates_df: Summary DataFrame with information about candidates.
    """
    # Group by 'TGT' (candidate) and calculate candidate-related statistics
    candidate_grouped = df.groupby('TGT')
    candidates_df = pd.DataFrame({
        'USER': candidate_grouped['TGT'].first(),
        'Number of Elections': candidate_grouped['ELECTION_ID'].nunique(),
        'Average Text Length': candidate_grouped['TXT'].apply(lambda x: x.str.len().mean())
    }).reset_index(drop=True)

    return candidates_df

def create_voters_df(df):
    """
    Create a summary DataFrame for voters based on 'SRC' (voter).

    Parameters:
    - df: DataFrame containing election data with columns 'SRC', 'YEA', 'VOT', 'RES'.

    Returns:
    - voters_df: Summary DataFrame with information about voters.
    """
    # Group by 'SRC' (voter) and calculate voter-related statistics
    voter_grouped = df[df['SRC'].notna()].groupby('SRC')
    voters_df = pd.DataFrame({
        'USER': voter_grouped['SRC'].first(),
        'Active Years': voter_grouped['YEA'].unique(),
        'Votes Count': voter_grouped['VOT'].count(),
        'Positive Percentage': voter_grouped['VOT'].apply(lambda x: (x == 1).mean() * 100),
        'Negative Percentage': voter_grouped['VOT'].apply(lambda x: (x == -1).mean() * 100),
        'Neutral Percentage': voter_grouped['VOT'].apply(lambda x: (x == 0).mean() * 100),
        'Voted Differently': voter_grouped.apply(lambda group: (group['VOT'] != group['RES']).mean() * 100),
        'Voted Similarly': voter_grouped.apply(lambda group: (group['VOT'] == group['RES']).mean() * 100)
    }).reset_index(drop=True)

    return voters_df
