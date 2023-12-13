import requests
from bs4 import BeautifulSoup
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import json
import csv

from datetime import datetime as dt

import requests
import json
import unittest
import os
import sqlite3
import matplotlib.pyplot as plt
import csv
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.patches as mpatches

#### FIRST RUN THROUGH ####

url = "https://stats.nba.com/stats/teamgamelog"

headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    "Referer": "https://stats.nba.com/team/1610612747/gamelog/",
    "Accept-Language": "en-US,en;q=0.9",
}

params = {
    "Season": "2022-23",
    "SeasonType": "Regular Season",
    "TeamID": "1610612747"  # Team ID for Los Angeles Lakers
}

response = requests.get(url, headers=headers, params=params)
data = json.loads(response.text)
team_log = data['resultSets'][0]['rowSet']


for log in team_log:
    opponent = log[3]
    assists = log[-6]
    result = log[4] 
    id= log[1]
    date =log[2]

    print(f"Opponent: {opponent}, Assists: {assists}, Result: {result} date: {date}")

    opponents = []
    assists = []
    colors = []

    for log in team_log:
        opponent = log[3]
        opponents.append(opponent[7:])
        assists.append(log[-6])
        result = log[4]
        colors.append('g' if result == 'W' else 'r')  # green for win, red for loss
    with open("gamestats_database_2022.csv", 'w', newline='') as csvfile:
        fieldnames = ['id', 'date', 'opponent', 'result', 'assists']
        
        # Create a writer object and write the header (fieldnames)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    # Loop through the logs and write each row to the CSV
        for log in team_log:
            id = log[1]
            date = log[2]
            opponent = log[3]
            result = log[4]
            assists = log[-6]
            date_object = dt.strptime(date, '%b %d, %Y')

            formatted_date = date_object.strftime('%m-%d-%Y')
            # Write this row to the CSV
            writer.writerow({'id': id, 'date': formatted_date, 'opponent': opponent, 'result': result, 'assists': assists})
#this is the part that is iffy


df = pd.read_csv("gamestats_database_2022.csv")

# Plot the assists data
plt.figure(figsize=(10, 6))
plt.bar(df['opponent'], df['assists'], color= 'pink')
plt.xlabel('Opponent')
plt.ylabel('Assists')
plt.title('Number of assists the Lakers made in each game in the season')
plt.xticks(rotation=90)  
plt.show()

### SECOND RUN THROUGH ###

url = "https://stats.nba.com/stats/teamgamelog"

headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    "Referer": "https://stats.nba.com/team/1610612747/gamelog/",
    "Accept-Language": "en-US,en;q=0.9",
}

params = {
    "Season": "2021-22",
    "SeasonType": "Regular Season",
    "TeamID": "1610612747"  # Team ID for Los Angeles Lakers
}

response = requests.get(url, headers=headers, params=params)
data = json.loads(response.text)
team_log = data['resultSets'][0]['rowSet']


for log in team_log:
    opponent = log[3]
    assists = log[-6]
    result = log[4] 
    id= log[1]
    date =log[2]

    print(f"Opponent: {opponent}, Assists: {assists}, Result: {result} date: {date}")

    opponents = []
    assists = []
    colors = []

    for log in team_log:
        opponent = log[3]
        opponents.append(opponent[7:])
        assists.append(log[-6])
        result = log[4]
        colors.append('g' if result == 'W' else 'r')  # green for win, red for loss
    with open("gamestats_database_2021.csv", 'w', newline='') as csvfile:
        fieldnames = ['id', 'date', 'opponent', 'result', 'assists']
        
        # Create a writer object and write the header (fieldnames)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    # Loop through the logs and write each row to the CSV
        for log in team_log:
            id = log[1]
            date = log[2]
            opponent = log[3]
            result = log[4]
            assists = log[-6]
            date_object = dt.strptime(date, '%b %d, %Y')

            formatted_date = date_object.strftime('%m-%d-%Y')
            # Write this row to the CSV
            writer.writerow({'id': id, 'date': formatted_date, 'opponent': opponent, 'result': result, 'assists': assists})
#this is the part that is iffy

df = pd.read_csv("gamestats_database_2021.csv")

# Plot the assists data
plt.figure(figsize=(10, 6))
plt.bar(df['opponent'], df['assists'], color = 'hotpink')
plt.xlabel('Opponent')
plt.ylabel('Assists')
plt.title('Number of assists the Lakers made in each game in the season')
plt.xticks(rotation=90)  
plt.show()


df1 = pd.read_csv("gamestats_database_2021.csv")
df2 = pd.read_csv("gamestats_database_2022.csv")

# Add a 'year' column to each DataFrame
df1['year'] = '2021'
df2['year'] = '2022'

# Concatenate the dataframes
df = pd.concat([df1, df2])

# Create a color map
color_map = {'2021': 'hotpink', '2022': 'pink'}

# Now you can plot the combined data
plt.figure(figsize=(10, 6))
plt.bar(df['opponent'], df['assists'], color=df['year'].map(color_map))
plt.xlabel('Opponent')
plt.ylabel('Assists')
plt.title('Number of assists the Lakers made in each game in the season')
plt.xticks(rotation=90) 

handles = [mpatches.Patch(color=color, label=year) for year, color in color_map.items()]
plt.legend(handles=handles, title='Year')

plt.show()





# Plot the assists data
plt.figure(figsize=(10, 6))
plt.bar(df['opponent'], df['assists'])
plt.xlabel('Opponent')
plt.ylabel('Assists')
plt.title('Number of assists the Lakers made in each game in the season')
plt.xticks(rotation=90)  
plt.show()



df.to_csv(os.path.join("/Users/andrewbonnah/Desktop/ML_NBA_Prediction", 'final_chart.csv'), index=False)
