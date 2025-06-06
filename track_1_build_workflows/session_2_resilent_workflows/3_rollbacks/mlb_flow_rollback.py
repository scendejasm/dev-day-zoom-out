from prefect import flow, task, runtime
from prefect.artifacts import create_markdown_artifact
from prefect.transactions import transaction
from prefect_aws.s3 import S3Bucket
from prefect.blocks.system import Secret
from datetime import datetime
import statsapi
import json
import pandas as pd
import os
import time
import duckdb

@task
def get_recent_games(team_name, start_date, end_date):
    '''This task will fetch the schedule for the provided team and date range and return the game ids.'''
    team = statsapi.lookup_team(team_name)
    schedule = statsapi.schedule(team=team[0]["id"], start_date=start_date, end_date=end_date)
    for game in schedule:
        print(game['game_id'])
    return [game['game_id'] for game in schedule]


@task
def fetch_single_game_boxscore(game_id, start_date, end_date, team_name):
    '''This task will fetch the boxscore for a single game and return the game data.'''
    boxscore = statsapi.boxscore_data(game_id)
    
    # Extract relevant data
    home_score = boxscore['home']['teamStats']['batting']['runs']
    away_score = boxscore['away']['teamStats']['batting']['runs']
    home_team = boxscore['teamInfo']['home']['teamName']
    away_team = boxscore['teamInfo']['away']['teamName']
    time_value = next(item['value'] for item in boxscore['gameBoxInfo'] if item['label'] == 'T')
    
    #Create a dictionary with the game data
    game_data = {
        'search_start_date': start_date,
        'search_end_date': end_date,
        'chosen_team_name': team_name,
        'game_id': game_id,
        'home_team': home_team,
        'away_team': away_team,
        'home_score': home_score,
        'away_score': away_score,
        'score_differential': abs(home_score - away_score),
        'game_time': time_value,
    }
    
    print(game_data)
    return game_data

@task
def save_raw_data_to_file(game_data, file_name):
    '''This task will save the raw data to a file.'''
    
    with open(file_name, "w") as outfile:
        json.dump(game_data, outfile, indent=4, sort_keys=True)
    
    print(file_name)
    return file_name

@save_raw_data_to_file.on_rollback
def del_file(txn):
    "Deletes file."
    os.unlink(txn.get("filepath"))
    

@task
def quality_test(file_path):
    "Checks contents of file."
    with open(file_path, "r") as f:
        data = json.load(f)
        
    if len(data) < 5:
        raise ValueError(f"Not enough data! There are only {len(data)} games in the file.")

@task
def upload_raw_data_to_s3(file_path):
    '''This task will upload the raw data to s3.'''
    
    s3_bucket = S3Bucket.load("mlb-raw-data")
    s3_bucket_path = s3_bucket.upload_from_path(file_path)
    
    print(s3_bucket_path)
    return s3_bucket_path
    

@task
def download_raw_data_from_s3(s3_file_path):
    '''Download the raw data from s3.'''
    
    s3_bucket = S3Bucket.load("mlb-raw-data")
    local_file_path = f"./boxscore_analysis/{s3_file_path}"
    s3_bucket.download_object_to_path(s3_file_path, local_file_path)
    
    return local_file_path

@task
def clean_time_value(data_file_path):
    '''This task will clean the time value.'''
    
    try:
        with open(data_file_path, 'r') as f:
            game_data_list = json.load(f)
    except FileNotFoundError:
        raise ValueError(f"File not found: {data_file_path}") 
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON file: {data_file_path}")
    
    # Process each game in the list
    for game_data in game_data_list:
        # Remove any extra text like '(1:16 delay)'
        if '(' in game_data['game_time']:
            game_data['game_time'] = game_data['game_time'].split('(')[0]
        
        # Remove any non-digit, non-colon characters
        game_data['game_time'] = ''.join(char for char in game_data['game_time'] if char.isdigit() or char == ':')
        
        hours, minutes = map(int, game_data['game_time'].split(':'))
        game_data['game_time_in_minutes'] = hours * 60 + minutes
    
    # Save the modified data back to the file
    with open(data_file_path, 'w') as f:
        json.dump(game_data_list, f, indent=4, sort_keys=True)
    
    return data_file_path

@task
def analyze_games(data_file_path):
    '''This task will analyze the game data and return the analysis.'''
    
    try:
        with open(data_file_path, 'r') as f:
            game_data = json.load(f)
    except FileNotFoundError:
        raise ValueError(f"File not found: {data_file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON file: {data_file_path}")
    
    # Convert to DataFrame
    df = pd.DataFrame(game_data)
    
    #Get the search parameters
    start_date = df['search_start_date'].unique()[0]
    end_date = df['search_end_date'].unique()[0]
    team_name = df['chosen_team_name'].unique()[0]
    
    # Calculate average, median, max, and min differential
    avg_differential = float(df['score_differential'].mean())
    median_differential = float(df['score_differential'].median())
    max_differential = float(df['score_differential'].max())
    min_differential = float(df['score_differential'].min())

    
    # Calculate average, median, max, and min game time
    avg_game_time = float(df['game_time_in_minutes'].mean())
    median_game_time = float(df['game_time_in_minutes'].median())
    max_game_time = float(df['game_time_in_minutes'].max())
    min_game_time = float(df['game_time_in_minutes'].min())
    
    # Calculate correlation between game time and score differential
    correlation = float(df['game_time_in_minutes'].corr(df['score_differential']))
    
    game_analysis = {
        'search_start_date': start_date,
        'search_end_date': end_date,
        'chosen_team_name': team_name,
        'max_game_time': max_game_time,
        'min_game_time': min_game_time,
        'median_game_time': median_game_time,
        'average_game_time': avg_game_time,
        'max_differential': max_differential,
        'min_differential': min_differential,
        'median_differential': median_differential,
        'average_differential': avg_differential,
        'time_differential_correlation': correlation,
    }
    print(game_analysis)
    return game_analysis

@task
def save_analysis_to_file(game_analysis, file_name):
    '''This task will save the analysis to a file.'''
    
    # Method 1: Single row format
    df = pd.DataFrame([game_analysis])
    df.to_parquet(file_name)
    
    print(file_name)
    return file_name

@task
def game_analysis_artifact(game_analysis, game_data_path):
    '''This task will create an artifact with the game analysis.'''
    
    # First read the JSON data from the file
    with open(game_data_path, 'r') as f:
        game_data = json.load(f)
    
    # Now create the DataFrame from the loaded data
    df = pd.DataFrame(game_data)
    
    # Create the markdown report
    markdown_report=f""" # Game Analysis Report
## Search Parameters
Search Start Date: {game_analysis['search_start_date']}
Search End Date: {game_analysis['search_end_date']}
Chosen Team Name: {game_analysis['chosen_team_name']}

## Summary Statistics
Max game time: {game_analysis['max_game_time']:.2f}
Min game time: {game_analysis['min_game_time']:.2f}
Median game time: {game_analysis['median_game_time']:.2f}
Average game time: {game_analysis['average_game_time']:.2f}
Max differential: {game_analysis['max_differential']:.2f}
Min differential: {game_analysis['min_differential']:.2f}
Median differential: {game_analysis['median_differential']:.2f}
Average differential: {game_analysis['average_differential']:.2f}
Correlation between game time and score differential: {game_analysis['time_differential_correlation']:.2f}

## Raw Data
{df.to_markdown(index=False)}

"""
    create_markdown_artifact(
        key="game-analysis",
        markdown=markdown_report,
        description="Game analysis report"
    )
    
@task
def load_parquet_to_duckdb(parquet_file_path, team_name):
    '''This task will load the parquet file to duckdb.'''
    
    #Connect to duckdb
    secret_block = Secret.load("mother-duck-test")
    # Access the stored secret
    duck_token = secret_block.get()
    duckdb_conn = duckdb.connect(f"md:?motherduck_token={duck_token}")
    
    #Create a table in duckdb
    duckdb_conn.execute(f"""CREATE TABLE IF NOT EXISTS boxscore_analysis_{team_name} (
        search_start_date TEXT, 
        search_end_date TEXT, 
        chosen_team_name TEXT, 
        max_game_time FLOAT, 
        min_game_time FLOAT, 
        median_game_time FLOAT, 
        average_game_time FLOAT, 
        max_differential FLOAT, 
        min_differential FLOAT, 
        median_differential FLOAT, 
        average_differential FLOAT, 
        time_differential_correlation FLOAT)""")
    
    # Use the COPY command to load the Parquet file into MotherDuck
    duckdb_conn.execute(f"COPY boxscore_analysis FROM '{parquet_file_path}' (FORMAT 'parquet')")



@flow
def mlb_flow_rollback(team_name, start_date, end_date):
    # Get recent games
    game_ids = get_recent_games(team_name, start_date, end_date)
    
    # Fetch boxscore for each game
    game_data = [fetch_single_game_boxscore(game_id, start_date, end_date, team_name) for game_id in game_ids]
    
    #Define file path for raw data
    today = datetime.now().strftime("%Y-%m-%d") #YYYY-MM-DD
    flow_run_name = runtime.flow_run.name
    raw_file_path = f"./raw_data/{today}-{team_name}-{flow_run_name}-boxscore.json"
    #Create transaction which will be used to rollback if the data quality test fails
    with transaction() as txn:
        txn.set("filepath", raw_file_path)
        # Save raw data to a file
        save_raw_data_to_file(game_data, raw_file_path)
        time.sleep(10) # sleeping to give you a chance to see the file
        quality_test(raw_file_path)
        # Upload raw data to s3
        s3_file_path = upload_raw_data_to_s3(raw_file_path)
    
    
    #Download raw data from s3
    raw_data = download_raw_data_from_s3(s3_file_path)
    
    # Clean the time value
    clean_data = clean_time_value(raw_data)
    
    # Analyze the results
    results = analyze_games(clean_data)
    
    # Save the results to a parquet file
    parquet_file_path = f"./boxscore_parquet/{today}-{team_name}-{flow_run_name}-game-analysis.parquet"
    save_analysis_to_file(results, parquet_file_path)
    
    # Load the results to duckdb
    load_parquet_to_duckdb(parquet_file_path, team_name)
    
    # Save the results to an artifact
    game_analysis_artifact(results, raw_data)
    
    
if __name__ == "__main__":
    #This flow will succeed
    #mlb_flow_rollback("marlins", '06/01/2024', '06/30/2024')
    #This flow will fail the quality test
    mlb_flow_rollback("marlins", '06/01/2024', '06/02/2024')