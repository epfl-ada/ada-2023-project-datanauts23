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
    - df: DataFrame containing election data with columns 'TGT', 'ELECTION_ID', 'RES', 'VOT', 'TXT'.

    Returns:
    - candidates_df: Summary DataFrame with information about candidates.
    """
    # Calculate Total Votes, Positive Votes, Negative Votes, Neutral Votes, and Average Length
    grouped_df = df.groupby(['TGT', 'ELECTION_ID', 'RES'])
    counts = grouped_df['VOT'].count()
    positive_votes = grouped_df['VOT'].apply(lambda x: (x == 1).sum())
    negative_votes = grouped_df['VOT'].apply(lambda x: (x == -1).sum())
    neutral_votes = grouped_df['VOT'].apply(lambda x: (x == 0).sum())
    average_length = grouped_df['TXT'].apply(lambda x: x.str.len().mean())

    # Create a DataFrame with calculated values
    elections_df = pd.DataFrame({
        'TGT': grouped_df['TGT'].first(),
        'ELECTION_ID': grouped_df['ELECTION_ID'].first(),
        'RES': grouped_df['RES'].first(),
        'Total Votes': counts,
        'Positive Votes': positive_votes,
        'Negative Votes': negative_votes,
        'Neutral Votes': neutral_votes,
        'Average Length': average_length
    }).reset_index(drop=True)

    # Aggregate data by 'TGT' for final candidate statistics
    grouped_candidates = elections_df.groupby('TGT')
    candidates_df = pd.DataFrame({
        'USER': grouped_candidates['TGT'].first(),
        'Number of Elections': grouped_candidates['ELECTION_ID'].nunique(),
        'Won Elections': grouped_candidates['RES'].apply(lambda x: (x == 1).sum()),
        'Lost Elections': grouped_candidates['RES'].apply(lambda x: (x == 0).sum()),
        'Votes Received': grouped_candidates['Total Votes'].sum(),
        'Positive Percentage': grouped_candidates['Positive Votes'].sum() / grouped_candidates['Total Votes'].sum(),
        'Negative Percentage': grouped_candidates['Negative Votes'].sum() / grouped_candidates['Total Votes'].sum(),
        'Neutral Percentage': grouped_candidates['Neutral Votes'].sum() / grouped_candidates['Total Votes'].sum(),
        'Average Length Received': grouped_candidates['Average Length'].mean()
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



def remove_wiki_markup(txt):
    
    """
    Removes the wiki markup from the given text.
    
    Parameters:
    - txt (string): containing markup to be removed
    
    Returns:
    - cleaned_txt (string): text without markup
    """
    
    cleaned_txt = re.sub(r"\[\[.*?\]\]", "", txt) # internal links like: '[[WP:NETPOS]]'
    cleaned_txt = re.sub(r"&[a-zA-Z]+;|&#[0-9]+;", "", cleaned_txt) # html entities like: '&nbsp;–&nbsp';
    cleaned_txt = re.sub(r"'''(.*?)'''", r"\1", cleaned_txt) # bold
    cleaned_txt = re.sub(r"''(.*?)''", r"\1", cleaned_txt) # italic
    cleaned_txt = re.sub(r"<.*?>", "", cleaned_txt) # html
    cleaned_txt = re.sub(r"\[\[.*?\|([^\]]*?)\]\]", r"\1", cleaned_txt) # links
    cleaned_txt = re.sub(r"\[http[^\]]*?\]", "", cleaned_txt) # external links 
    cleaned_txt = re.sub(r"\{\{.*?\}\}", "", cleaned_txt) # templates 
    cleaned_txt = re.sub(r"==([^=]+)==", r"\1", cleaned_txt) # header 
    cleaned_txt = re.sub(r"==([^=]+)==", r"\1", cleaned_txt) # dash
    cleaned_txt = re.sub(r'--', ' ', cleaned_txt)
    cleaned_txt = re.sub(r"'''", ' ', cleaned_txt)
    return cleaned_txt



def parse_other_datasets(file_path):
    data = []
    row_data = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line[:2] == '| ':
                row_data.append(line[2:])
            else:
                if row_data:
                    data.append(row_data)
                    row_data = []

    if row_data:
        data.append(row_data)

    column_names = data[0] if data else None
    df = pd.DataFrame(data[1:], columns=column_names)
    return df


def format_authors_df(df):
    """
    Modifies the input DataFrame with specific transformations.

    - For indexes 0 to 100, it takes the value in the column 'NB_ARTICLES' of the 101st index and adds 1 to those values.
    - Sets the 'RANK' column to 1 for first 100 rows.
    - Converts 'RANK' column to numeric, 'NB_ARTICLES' to integer, and 'USER' to string data types.
    - Cleans the 'USER' column to retain only the username without the "User:..." prefix.

    Args:
    - df (pandas DataFrame): Input DataFrame to be modified.

    Returns:
    - None (modifies the DataFrame in place).
    """

    df.loc[:100, 'NB_ARTICLES'] = str(int(df.loc[101, 'NB_ARTICLES'].replace(',', '')) + 1)
    df.loc[:100, 'RANK'] = 1
    df['RANK'] = pd.to_numeric(df['RANK'])
    df['NB_ARTICLES'] = df['NB_ARTICLES'].str.replace(',', '').astype(int)
    df['USER'] = df['USER'].astype(str)
    to_format = df['USER'].str.match(r'\[\[User:[^\|]+\|([^\]]+)\]\]', na=False)
    df.loc[to_format, 'USER'] = df.loc[to_format, 'USER'].str.extract(r'\[\[User:[^\|]+\|([^\]]+)\]\]', expand=False)
    
    
    
def format_editors_df(df):
    """
    Modifies the input DataFrame with specific transformations.

    - Converts 'RANK' column to numeric, 'NB_ARTICLES' to integer, and 'USER' to string data types.
    - Cleans the 'USER' column to retain only the username without the "User:..." prefix.

    Args:
    - df (pandas DataFrame): Input DataFrame to be modified.

    Returns:
    - None (modifies the DataFrame in place).
    """

    df['RANK'] = pd.to_numeric(df['RANK'])
    df['NB_EDITS'] = df['NB_EDITS'].str.replace(',', '').astype(int)
    df['USER'] = df['USER'].astype(str)
    to_format = df['USER'].str.match(r'\[\[User:[^\|]+\|([^\]]+)\]\]', na=False)
    df.loc[to_format, 'USER'] = df.loc[to_format, 'USER'].str.extract(r'\[\[User:[^\|]+\|([^\]]+)\]\]', expand=False)
    
    
def format_creators_df(df):
    """
    Modifies the input DataFrame with specific transformations.

    - Converts 'RANK' column to numeric, 'NB_ARTICLES' to integer, and 'USER' to string data types.
    - Cleans the 'USER' column to retain only the username without the "User:..." prefix.

    Args:
    - df (pandas DataFrame): Input DataFrame to be modified.

    Returns:
    - None (modifies the DataFrame in place).
    """

    df['RANK'] = pd.to_numeric(df['RANK'])
    df['NB_PAGES'] = df['NB_PAGES'].str.replace(',', '').astype(int)
    df['USER'] = df['USER'].astype(str)
    to_format = df['USER'].str.match(r'\[\[User:[^\|]+\|([^\]]+)\]\]', na=False)
    df.loc[to_format, 'USER'] = df.loc[to_format, 'USER'].str.extract(r'\[\[User:[^\|]+\|([^\]]+)\]\]', expand=False)