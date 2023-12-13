import requests
import datetime
import json
import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

def get_api_team_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an exception if the status code is not 200
        return response.json()["data"]  # If successful, return the data as a Python dictionary
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
    return None




def game_data_by_year(year):


    base_url = f"https://www.balldontlie.io/api/v1/games?seasons[]={year}&per_page=100"
    data_list = []
    page = 0
    new_dict = {}
    result_dict = {}
    while True:
        url = f"{base_url}&page={page}"
        try:
            response = requests.get(url)
            
            
            data = response.json()
            
            # Stop if 'data' field is empty
            if not data['data']:
                break
            
            data_list.append(data)  # If successful, add the data to data list
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
        except requests.exceptions.RequestException as err:
            print(f"Error occurred: {err}")
        
        page += 1  # Go to next page
    return data_list

def write_to_csv(data, filename):
    # Extract the keys from the first dictionary and use them as the csv headers
    headers = list(data[0].keys())

    with open(filename, 'w', newline='') as csvfile:
        # Create a CSV writer
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write the header to the CSV file
        writer.writeheader()

        # Write all the data to the CSV file
        for game in data:
            writer.writerow(game)
def write_to_csv_game(data, filename):
        # Extract the keys from the first dictionary and use them as the csv headers
    headers = ["id", "date","period", "season", "status", "postseason", "home_team", "home_team_score", "visitor_team", "visitor_team_score", "time"]

    with open(filename, 'w', newline='') as csvfile:
        # Create a CSV writer
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write the header to the CSV file
        writer.writeheader()

        # Write all the data to the CSV file
        for game in data:
            for dict_ in game["data"]:
                writer.writerow(dict_)
def convert_date_format(csv_file):
    # Load CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Convert date strings to datetime objects, then reformat them
    df.iloc[:,1] = pd.to_datetime(df.iloc[:,1]).dt.strftime('%m-%d-%Y')

    # Save the DataFrame back to the CSV file
    df.to_csv(csv_file, index=False)
def plot_from_data(filename):
    df = pd.read_csv(filename)

    # Parsing columns which hold JSON-like string but single quoted
    df['home_team'] = df['home_team'].apply(eval)
    df['visitor_team'] = df['visitor_team'].apply(eval)

    # Extracting full team name from the parsed dict
    df['home_team_name'] = df['home_team'].apply(lambda x: x['full_name'])
    df['visitor_team_name'] = df['visitor_team'].apply(lambda x: x['full_name'])

    # Sum up scores for each team
    home_team_scores = df.groupby('home_team_name')['home_team_score'].sum()
    visitor_team_scores = df.groupby('visitor_team_name')['visitor_team_score'].sum()

    # Adding scores from both columns for each team
    score_sums = home_team_scores.add(visitor_team_scores, fill_value=0)

    # Sorting scores in ascending order so the color would correspond to the score
    score_sums = score_sums.sort_values(ascending=True)
    
    # Generate gradient of colors from pink to neon green
    cmap = LinearSegmentedColormap.from_list(name='grad', colors=['#FF1493', '#39FF14'])
    colors = [cmap(i) for i in np.linspace(0, 1, len(score_sums))]

    # Create pie chart
    plt.figure(figsize=(10, 10))
    plt.pie(score_sums, labels=score_sums.index, autopct='%1.1f%%', colors=colors, textprops={'fontsize': 8})
    plt.title('Total points by team')
    plt.show()





# Call the function with a specified year
year = 2022
year_data = game_data_by_year(2022)

# Use the function with your URL
team_url = "https://www.balldontlie.io/api/v1/teams"
team_data = get_api_team_data(team_url)
write_to_csv(team_data, 'teams1.csv')

write_to_csv_game(year_data, "games2.csv")

convert_date_format('games2.csv')
plot_from_data('games2.csv')

